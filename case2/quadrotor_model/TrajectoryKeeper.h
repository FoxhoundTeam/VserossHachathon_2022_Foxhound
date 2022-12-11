#pragma once
#include <Eigen/Dense>
#include "PID.h"
#define _USE_MATH_DEFINES
#include <math.h>
#include <list>

using namespace Eigen;

class TrajectoryKeeper
{
	private:

		static double Sq(const double val)
		{
			return val * val;
		}

		std::list<Vector3d> trajectory;

	public:
		TrajectoryKeeper(std::list<Vector3d> trajectory)
		{
			this->trajectory = trajectory;
		}
		Quaterniond GetQuaternion(Vector3d position, double velocity, int i)
		{
			Vector3d targetPos, targetPos2;
			double targetVel, targetVel2;
			double Kp, Kd;

			double psi = atan2( targetPos.z() - position.z() , targetPos.x() - position.x());
			double th = Kp * (targetPos.norm() - position.norm()) + Kd * (targetVel - velocity);

			double Vcp0 = (velocity + targetVel) / 2;
			double Vcp1 = (targetVel2 + targetVel) / 2;

			double dt0 = (targetPos  -  position).norm()/Vcp0;
			double dt1 = (targetPos - targetPos2).norm() / Vcp1;

			double ax = ((targetPos2.x() - targetPos.x()) / dt1 - (targetPos.x() - position.x()) / dt0) / (dt1 + dt0);
			double az = ((targetPos2.z() - targetPos.z()) / dt1 - (targetPos.z() - position.z()) / dt0) / (dt1 + dt0);

			double fi = asin(az * cos(psi) + ax * sin(psi));

			//double dt = V/(Points[i + 1] - Points[i]).norm();
			//double ax = (Points[i + 2].x() - 2 * Points[i + 1].x() + Points[i].x()) / Sq(dt);
			//double az = (Points[i + 2].z() - 2 * Points[i + 1].z() + Points[i].z()) / Sq(dt);

			//double psi = atan2(, 1);		//TODO
			//double fi    = asin( az*cos(psi) + ax*sin(psi) );
			//double tetha = acos( az*sin(psi) - ax*cos(psi) );
		}
};
