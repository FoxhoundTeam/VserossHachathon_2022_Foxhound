#include <iostream>
#include "QuadrotorDynamics.h"
#include "TrajectoryKeeper.h"
#include "ControlSystem.h"
#include "PID.h"
#include <Eigen/Dense>
#define _USE_MATH_DEFINES
#include <math.h>
#include "Network.h"
#include <list>
#include <fstream>
#include <vector>

void tokenize(std::string const& str, const char delim,
    std::vector<std::string>& out)
{
    size_t start;
    size_t end = 0;

    while ((start = str.find_first_not_of(delim, end)) != std::string::npos)
    {
        end = str.find(delim, start);
        out.push_back(str.substr(start, end - start));
    }
}

double Constrain(const double val, double min, double max)
{
    if (val > max) return max;
    if (val < min) return min;
    return val;
}


__declspec(dllexport)
double* cppfunc(double xDrone, double zDrone, double hDrone, double finalTime, double *x, double *z, int pointsSize, double xCar, double zCar, double vxCar, double vzCar)
{

    double *retArr = (double*)malloc(10*1000*sizeof(double));

    /*НАЧАЛЬНЫЕ ПАРАМЕТРЫ СОСТОЯНИЯ*/
    Quaterniond quaternion = Quaterniond(1, 0, 0, 0);

    Quaterniond quaternionTarget = Quaterniond(1, 0, 0, 0);

    //Vector3d position = Vector3d(std::stod(state[0]), std::stod(state[1]), std::stod(state[2]));
    Vector3d position = Vector3d(xDrone, hDrone, zDrone);

    Vector3d velocity = Vector3d::Zero();
    Vector3d angularVelocity = Vector3d::Zero();

    QuadrotorDynamics quadcopter = QuadrotorDynamics(position, velocity, angularVelocity, quaternion);

    ControlSystem controller = ControlSystem(15E6, 1.2E6,
        100E5, 100E5, 0.00,
        15, 75, 0,
        15, 75, 0);

    Vector3d targetPosition = Vector3d(4, 1, 1);

    //НОМИНАЛЬНАЯ ВЫСОТА ПОЛЁТА
    double h_nom = 32;

    /*ШАБЛОН ДВИЖЕНИЯ ВОКРУГ ЦЕЛИ*/
    const int tPCoint = 4;
    Vector3d tPs[tPCoint];
    double atps = 10;
    tPs[0] = Vector3d(-atps, h_nom, atps);
    tPs[0] = Vector3d(atps, h_nom, atps);
    tPs[0] = Vector3d(atps, h_nom, -atps);
    tPs[0] = Vector3d(-atps, h_nom, -atps);
    int tPs_iterator = 0;

    /*ТОЧКИ ПУТИ*/
    int pathNumber = 1;
    
   ///// TODO /////
    Vector3d Points[1000]; ///!!!

    for (int k = 0; k < pointsSize; k++)
    {
        Points[k] = Vector3d(x[k], h_nom, z[k]);
    }



    int counter = 0;
    //std::string timeStates = "";

    double targetXinit = xCar, targetYinit =  zCar;
    double targetVX = vxCar, targetVY = vzCar;
    double targetX, targetY;

    bool isCapture = false;
    /*ОСНОВНОЙ ЦИКЛ РАСЧЁТА*/

    int recIterator = 0;

    while (quadcopter.GetTime() < finalTime)
    {

        /*ДВИЖЕНИЕ ЦЕЛИ*/
        targetX = targetXinit + targetVX * quadcopter.GetTime();
        targetY = targetYinit + targetVY * quadcopter.GetTime();

        Vector3d pos2d = Vector3d(quadcopter.GetPosition().x(), 0, quadcopter.GetPosition().z());

        if ((pos2d - Vector3d(targetX, 0, targetY)).norm() < 60)
        {
            isCapture = true;// DEEEEEBUG!!!
        }

        Quaterniond targetQuaternion;

        if (!isCapture)
        {

            //targetQuaternion = controller.getPosControlQuaternionInvariantPsi(quaternionTarget, quadcopter.GetPosition(), Points[pathNumber], quadcopter.GetVelocity(), 0.1, 1);

            //добавил скорость в регулятор, чтобы не тормозить на каждой точке
            Vector3d VelReg = quadcopter.GetVelocity() + (quadcopter.GetPosition() - Points[pathNumber]).normalized() * 3;

            targetQuaternion = controller.getPosControlQuaternionInvariantPsi(quaternionTarget, quadcopter.GetPosition(), Points[pathNumber], VelReg, 0.1, 3);

        }
        if (isCapture)
        {
            Vector3d e = quadcopter.GetPosition();


            Vector3d targetPoint = Vector3d(targetX, h_nom, targetY) + tPs[0];
            if ((quadcopter.GetPosition() - targetPoint).norm() < 3)
            {
                if (tPs_iterator == tPCoint - 1)
                    tPs_iterator = 0;
                else
                    tPs_iterator++;
            }

            targetQuaternion = controller.getPosControlQuaternionInvariantPsi(quaternionTarget, quadcopter.GetPosition(), targetPoint, quadcopter.GetVelocity(), 0.5, 2);

        }
        Vector3d M = controller.getControlMomentStabilize(targetQuaternion, quadcopter.GetQuaternion(), quadcopter.GetAngularVelocity());

        double vy_g = quadcopter.GetVelocity().y();
        double AltControl = controller.getAltitudeControl(quadcopter.GetPosition().y(), h_nom, vy_g);

        double kAlt = 1;
        Vector4d control = Vector4d(
            Constrain(2015 + M(0) + M(1) + kAlt * AltControl, 100, 5000), //1
            Constrain(2015 + M(2) - M(1) + kAlt * AltControl, 100, 5000),   //2
            Constrain(2015 - M(0) + M(1) + kAlt * AltControl, 100, 5000), //3
            Constrain(2015 - M(2) - M(1) + kAlt * AltControl, 100, 5000)    //4
        );

        //std::cout << quadcopter.GetVelocity().norm() << std::endl;

        if ((quadcopter.GetPosition() - Points[pathNumber]).norm() < 3)
        {
            if (pathNumber == pointsSize - 1)
                pathNumber = 0;
            else
                pathNumber++;
        }


        if (counter % 4 == 0)
        {
            //std::string data = std::to_string(quadrotor.getStateVector()[9]) + " " +
            //    std::to_string(quadrotor.getStateVector()[10]) + " " +
            //    std::to_string(quadrotor.getStateVector()[11]) + " " +
            //    std::to_string(quadrotor.getStateVector()[12]) + " " +
            //    std::to_string(0 + 1 * quadrotor.getStateVector()[0]) + " " +
            //    std::to_string(0 + 1 * quadrotor.getStateVector()[1]) + " " +
            //    std::to_string(0 + 1 * quadrotor.getStateVector()[2]) + " ";

            retArr[recIterator] = quadcopter.GetTime();
            recIterator++;

            retArr[recIterator] = quadcopter.GetPosition().x();
            recIterator++;
            retArr[recIterator] = quadcopter.GetPosition().y();
            recIterator++;
            retArr[recIterator] = quadcopter.GetPosition().z();
            recIterator++;

            retArr[recIterator] = quadcopter.GetQuaternion().w();
            recIterator++;
            retArr[recIterator] = quadcopter.GetQuaternion().x();
            recIterator++;
            retArr[recIterator] = quadcopter.GetQuaternion().y();
            recIterator++;
            retArr[recIterator] = quadcopter.GetQuaternion().z();

            recIterator++;
            retArr[recIterator] = targetX;
            recIterator++;
            retArr[recIterator] = targetY;

            recIterator++;
            //std::string data = quadcopter.GetData();

            //timeStates += std::to_string(quadcopter.GetTime()) + " " + quadcopter.GetData() + "" + std::to_string(targetX) + " " + std::to_string(targetY) + " \n";
        }

        quadcopter.SolveStep(control, 0.01);

        counter++;
    }

    return retArr;
    //std::cout << "Complete" << std::endl;
    //return timeStates;
}

int main()
{
    
    double xArr[] = { 0, 20, 40, 60, 80, 90, 100  };
    double zArr[] = { 0, 10, 0, 0, 0, 0, 10 };

    double* RECs = cppfunc(100, 0, 32, 50, xArr, zArr, 7, 100, 0, -5, -2);
    
    int tvr = 1;
}


