using System.Net;
using System.Net.Sockets;
using UnityEngine.UI;
using System.Text;
using UnityEngine;
using System.Collections;
using System.Threading;


public class UDPReciveScript : MonoBehaviour
{
    public GameObject quadrotorObject;

    static readonly object lockObject = new object();
    private bool precessData = false;

    public static UdpClient client;
    IPEndPoint ip = null;
    Quaternion quaternion;
    Vector3 position;
    

    void Start()
    {
        //System.Diagnostics.Process.Start(@"C:\Users\ßנמסכאג\Desktop\ָֽ׀ׁ\UDP_Examples\NDSolver\version-0.1.2\QuadrotorModel\");

        System.Threading.Thread.CurrentThread.CurrentCulture = new System.Globalization.CultureInfo("en-US");
        quaternion = new Quaternion();
        

        client = new UdpClient(8818);

        Thread thread = new Thread(new ThreadStart(ReciveUDPMessage));
        thread.Start();
    }


    void Update()
    {
        if (precessData)
        {

            lock (lockObject)
            {
                precessData = false;
                quadrotorObject.transform.rotation = quaternion;
                quadrotorObject.transform.position = position;
            }
        }
    }

    private void ReciveUDPMessage()
    {
        while (true)
        {
            byte[] data = client.Receive(ref ip);
            if (data.Length > 0)
            {
                string message = Encoding.UTF8.GetString(data);

                Debug.Log("message: " + message);

                try
                {
                    string[] pointStr = (message.Split());

                    quaternion.x = float.Parse(pointStr[0]);
                    quaternion.y = float.Parse(pointStr[1]);
                    quaternion.z = float.Parse(pointStr[2]);
                    quaternion.w = float.Parse(pointStr[3]);
                    position.z   = -float.Parse(pointStr[4]);
                    position.y   = float.Parse(pointStr[5]);
                    position.x   = float.Parse(pointStr[6]);

                    precessData = true;
                }
                catch{ }
            }
        }
        
    }
}
