using System.Collections;
using System.Collections.Generic;
using System.IO;
using UnityEngine;
using UnityEngine.UI;

public class TxtStateReader : MonoBehaviour
{
    public static List<Vector3> positions;
    public static List<Quaternion> quaternions;

    public GameObject quadrotorObject;
    public GameObject target;

    Quaternion quaternion;
    Vector3 position;

    Vector3 carPosition;

    public Slider slider;
    public Text text;

    public InputField posX;
    public InputField posY;
    public InputField posZ;
    public InputField pitch;
    public InputField roll;
    public InputField yaw;


    public static double selectedTime = 0;



    private void Start()
    {
        System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("en-US");
        //posX.text = "0";
        //posY.text = "0";
        //posZ.text = "0";
        //pitch.text = "0";
        //roll.text = "0";
        //yaw.text = "0";
    }
    public int i = 0;
    void Update()
    {
        if (MenuScript.isPlay)
        {
                
                string[] pointStr = (MenuScript.states[i].Split(' '));

                quaternion.x = float.Parse(pointStr[1]);
                quaternion.y = float.Parse(pointStr[2]);
                quaternion.z = float.Parse(pointStr[3]);
                quaternion.w = float.Parse(pointStr[4]);
                position.z = -float.Parse(pointStr[5]);
                position.y = float.Parse(pointStr[6]);
                position.x = float.Parse(pointStr[7]);

            carPosition.x = float.Parse(pointStr[9]);
            carPosition.y = 0f;
            carPosition.z = -float.Parse(pointStr[8]);


            target.transform.position = carPosition;
                quadrotorObject.transform.rotation = quaternion;
                quadrotorObject.transform.position = position;

                 i++;

            if (i >= MenuScript.states.Length - 1)
                i = 0;
        }

        if (MenuScript.isDownload)
        {
            string[] pointStr = (MenuScript.states[(int)slider.value*1].Split(' '));

            text.text = (float.Parse(pointStr[0])).ToString("N2");

            quaternion.x = float.Parse(pointStr[1]);
            quaternion.y = float.Parse(pointStr[2]);
            quaternion.z = float.Parse(pointStr[3]);
            quaternion.w = float.Parse(pointStr[4]);
            position.z = -float.Parse(pointStr[5]);
            position.y = float.Parse(pointStr[6]);
            position.x = float.Parse(pointStr[7]);


            quadrotorObject.transform.rotation = quaternion;
            quadrotorObject.transform.position = position;
        }
        else
        {
            using (StreamWriter writer = new StreamWriter(@"C:\Users\ßנמסכאג\Desktop\ָֽ׀ׁ\UDP_Examples\NDSolver\version-0.1.2\QuadrotorModel\init.txt", false))
            {
                 writer.WriteLine(posX.text + " " + posY.text + " " + posZ.text + " " + pitch.text + " " + roll.text + " " + yaw.text);
            }
        }
    }
}
