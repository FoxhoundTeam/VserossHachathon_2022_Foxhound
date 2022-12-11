using System.IO;
using UnityEngine;
using UnityEngine.UI;
public class MenuScript : MonoBehaviour
{
    public static bool isDownload = false;
    public static bool isPlay = false;

    public static string[] states;
    public TxtStateReader initInput;
    public void ButtonEvent()
    {
        Debug.Log("Start calculation");

        //using (StreamWriter writer = new StreamWriter(@"C:\Users\ßנמסכאג\Desktop\ָֽ׀ׁ\UDP_Examples\NDSolver\version-0.1.2\QuadrotorModel\init.txt", false))
        //{
        //    writer.WriteLine(initInput.posX.text + " " + initInput.posY.text + " " + initInput.posZ.text + " " + initInput.pitch.text + " " + initInput.roll.text + " " + initInput.yaw.text);
        //}

        //System.Diagnostics.Process.Start(@"C:\Users\ßנמסכאג\Desktop\ָֽ׀ׁ\UDP_Examples\NDSolver\version-0.1.2\QuadrotorModel\Debug\QuadrotorModel.exe");

        isPlay = true;
    }

    public void ButtonDownload()
    {
        Debug.Log("Start loading results");

        using (StreamReader reader = new StreamReader(@"C:\Users\ßנמסכאג\Desktop\ָֽ׀ׁ\UDP_Examples\NDSolver\version-0.1.2\QuadrotorModel\state.txt" ))
        {
            string text = reader.ReadToEnd();
            states = text.Split('\n');
        }
        isDownload = true;
        isDownload = false;
    }
}
