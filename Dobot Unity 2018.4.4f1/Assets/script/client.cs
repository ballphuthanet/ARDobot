using System;
using System.Collections;
using System.Collections.Generic;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using UnityEngine;
using UnityEngine.UI;

public class client : MonoBehaviour
{
    public Text Xval, Yval, Zval, Rval, J1val, J2val, J3val, J4val;
    public Text J1val1, J2val1, J3val1, J4val1;
    public Toggle toggleswitch;
    public GameObject inputfieldX;
    public GameObject inputfieldY;
    public GameObject inputfieldZ;

    /*public InputField X;
    public InputField Y;
    public InputField Z;*/



    //#region private members 	
    private TcpClient socketConnection;
    private Thread clientReceiveThread;
    private Thread HoldThread;
    private bool connectcon = false;
    private bool exitcon = false;
    private string onedata;
    //private bool upbreak;
    private string control;
    

    //private string A = "[A:REG]";
    //private string B = "[B:yaa connect laew]";

    //#endregion
    // Use this for initialization 	
    void Start()
    {
        ConnectToTcpServer();

        Xval.text = "0";

        Yval.text = "0";

        Zval.text = "0";

        Rval.text = "0";

        J1val.text = "0";
        J1val1.text = J1val.text;
        J2val.text = "0";
        J2val1.text = J2val.text;
        J3val.text = "0";
        J3val1.text = J3val.text;
        J4val.text = "0";
        J4val1.text = J4val.text;
        control = "[Dobot:Hold]";

    }
    // Update is called once per frame
    void Update()
    {   
        
        if (onedata.Contains("[Dobot:X="))
        {
            Xval.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'X', '=', ']');

        }
        else if (onedata.Contains("[Dobot:Y="))
        {
            Yval.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'Y', '=', ']');


        }
        else if (onedata.Contains("[Dobot:Z="))
        {
            Zval.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'Z', '=', ']');


        }
        else if (onedata.Contains("[Dobot:R="))
        {
            Rval.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'R', '=', ']');


        }
        else if (onedata.Contains("[Dobot:Ji="))
        {
            J1val.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'X', '=', ']', 'i', 'J');
            J1val1.text = J1val.text;

        }
        else if (onedata.Contains("[Dobot:Jii="))
        {
            J2val.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'X', '=', ']', 'i', 'J');
            J2val1.text = J2val.text;

        }
        else if (onedata.Contains("[Dobot:Jiii="))
        {
            J3val.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'X', '=', ']', 'i', 'J');
            J3val1.text = J3val.text;
        }
        else if (onedata.Contains("[Dobot:Jiv="))
        {
            J4val.text = onedata.Trim('[', 'D', 'o', 'b', 'o', 't', ':', 'X', '=', ']', 'i', 'v', 'J');
            J4val1.text = J4val.text;
        }

        if (exitcon == true)
        {
            Application.Quit();
        }
    }

    //---------------------connect------------------------

    
    public void connect()
    {

        if (connectcon == false)
        {
            SendMessage("[Unity:REG]");
            SendMessage("[Dobot:CONNECT]");
            connectcon = true;
        }
        else
        {

            SendMessage("[Dobot:DISCONNECT]");
            connectcon = false;
        }

    }

    //----------------------XYZR---------------------------
    public void Xpos()
    {

        //control = "[Dobot:Xpos]";
        SendMessage("[Dobot:Xpos]");
        
    }
    public void Xneg()
    {
        //control = "[Dobot:Xneg]";
        SendMessage("[Dobot:Xneg]");
    }
    public void Ypos()
    {    
        //control = "[Dobot:Ypos]";
        SendMessage("[Dobot:Ypos]");
    }
    public void Yneg()
    { 
        //control = "[Dobot:Yneg]";
        SendMessage("[Dobot:Yneg]");

    }
    public void Zpos()
    {
         
        //control = "[Dobot:Zpos]";
        SendMessage("[Dobot:Zpos]");
    }
    public void Zneg()
    {   
        //control = "[Dobot:Zneg]";
        SendMessage("[Dobot:Zneg]");

    }
    public void Rpos()
    {
   
        //control = "[Dobot:Rpos]";
        SendMessage("[Dobot:Rpos]");

    }
    public void Rneg()
    {   
        //control = "[Dobot:Rneg]";
        SendMessage("[Dobot:Rneg]");

    }

    //----------------------Joint---------------------
    public void J1pos()
    {
     
        //control = "[Dobot:J1pos]";
        SendMessage("[Dobot:J1pos]");

    }
    public void J1neg()
    {
   
        //control = "[Dobot:J1neg]";
        SendMessage("[Dobot:J1neg]");

    }
    public void J2pos()
    {
    
        //control = "[Dobot:J2pos]";
        SendMessage("[Dobot:J2pos]");

    }
    public void J2neg()
    {
    
        //control = "[Dobot:J2neg]";
        SendMessage("[Dobot:J2neg]");

    }
    public void J3pos()
    {
 
        //control = "[Dobot:J3pos]";
        SendMessage("[Dobot:J3pos]");

    }
    public void J3neg()
    {

        //control = "[Dobot:J3neg]";
        SendMessage("[Dobot:J3neg]");
    }
    public void J4pos()
    {   
        //control = "[Dobot:J4pos]";
        SendMessage("[Dobot:J4pos]");

    }
    public void J4neg()
    {
   
        //control = "[Dobot:J4neg]";
        SendMessage("[Dobot:J4neg]");

    }

    //--------------------------------Home---------------------------------------------------------

    public void Home()
    {

        SendMessage("[Dobot:Home]");

    }

    //--------------------------------Command---------------------------------------------------------

    public void ForceStop()
    {

        SendMessage("[Dobot:Stop]");

    }

    //--------------------------------EXIT---------------------------------------------------------

    public void EXIT()
    {

        SendMessage("[Dobot:EXIT]");
        exitcon = true;

    }


    //------------------------------------test-----------------------------------------------------

    /*public void UpBreak()
    {
        upbreak = true;

    }*/


    //----------------------------------------------------------------------------
    //---------------------------------toggle------------------------------------
    public void toggle()
    {


        if (toggleswitch.isOn)
        {
            SendMessage("[Dobot:ONCUP]");
            Debug.Log("ONCUP");
            Console.WriteLine("ONCUP");
        }else{
            SendMessage("[Dobot:OFFCUP]");
            Debug.Log("OFFCUP");
            Console.WriteLine("OFFCUP");
        }



    }
    //----------------------------------run-----------------------------------------
    public void MOV()
    {
        string x = inputfieldX.GetComponent<Text>().text;
        string y = inputfieldY.GetComponent<Text>().text;
        string z = inputfieldZ.GetComponent<Text>().text;

        /*string x = X.text;
        string y = Y.text;
        string z = Z.text;*/

        if ((x != "") && (y != "") && (z != ""))
        {
            SendMessage("[Dobot:MOV," + x + "!" + y + "@" + z + "]");
        }

        

       /* Debug.Log("x=" + x);
        Debug.Log("y=" + y);
        Debug.Log("z=" + z);
        Console.WriteLine("x=" + x);
        Console.WriteLine("y=" + y);
        Console.WriteLine("z=" + z);*/
        
    }

    public void JUMP()
    {

        string x = inputfieldX.GetComponent<Text>().text;
        string y = inputfieldY.GetComponent<Text>().text;
        string z = inputfieldZ.GetComponent<Text>().text;
        /*string x = X.text;
        string y = Y.text;
        string z = Z.text;*/


        if ((x != "") && (y != "") && (z != ""))
        {
            SendMessage("[Dobot:JUMP," + x + "!" + y + "@" + z + "]");
        }

        /*Debug.Log("x=" + x);
        Debug.Log("y=" + y);
        Debug.Log("z=" + z);
        Console.WriteLine("x=" + x);
        Console.WriteLine("y=" + y);
        Console.WriteLine("z=" + z);*/

    }
    //-----------------------------------------------------------------------------
    /// <summary> 	
    /// Setup socket connection. 	
    /// </summary> 	
    public void ConnectToTcpServer()
    {
        try
        {
            clientReceiveThread = new Thread(new ThreadStart(ListenForData));
            HoldThread = new Thread(new ThreadStart(Hold));
            clientReceiveThread.IsBackground = true;
            HoldThread.IsBackground = true;
            clientReceiveThread.Start();
            HoldThread.Start();
        }
        catch (Exception e)
        {
            Debug.Log("On client connect exception " + e);
        }
    }
    /// <summary> 	
    /// Runs in background clientReceiveThread; Listens for incomming data. 	
    /// </summary>     
    private void ListenForData()
    {
        
        try
        {
            socketConnection = new TcpClient("192.168.1.235", 1150);
            Byte[] bytes = new Byte[1024];
            while (true)
            {
                // Get a stream object for reading 				
                using (NetworkStream stream = socketConnection.GetStream())
                {
                    int length;
                    // Read incomming stream into byte arrary. 					
                    while ((length = stream.Read(bytes, 0, bytes.Length)) != 0)
                    {
                        var incommingData = new byte[length];
                        Array.Copy(bytes, 0, incommingData, 0, length);
                        // Convert byte array to string message. 						
                        string serverMessage = Encoding.ASCII.GetString(incommingData);
                        Debug.Log("server message received as: " + serverMessage);
                        Console.WriteLine("server message received as: " + serverMessage);
                        string alldata = serverMessage;
                        Console.WriteLine(alldata);

                        while (alldata.IndexOf(']') != -1)
                        {
                            onedata = alldata.Substring(alldata.IndexOf('['), alldata.IndexOf(']') + 1);
                            alldata = alldata.Substring(alldata.IndexOf(']') + 1, alldata.Length - (alldata.IndexOf(']') + 1));



                            if (exitcon == true)
                            {
                                break;
                            }
                        }
                        if (exitcon == true)
                        {
                            break;
                        }
                    }
                }
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }
    /// <summary> 	
    /// Send message to server using socket connection. 	
    /// </summary> 	
    private void SendMessage(string msg)
    {
        if (socketConnection == null)
        {
            return;
        }
        try
        {
            // Get a stream object for writing. 			
            NetworkStream stream = socketConnection.GetStream();
            if (stream.CanWrite)
            {
                string clientMessage = msg;
                // Convert string message to byte array.                 
                byte[] clientMessageAsByteArray = Encoding.ASCII.GetBytes(clientMessage);
                // Write byte array to socketConnection stream.                 
                stream.Write(clientMessageAsByteArray, 0, clientMessageAsByteArray.Length);
                Debug.Log("Client sent his message - should be received by server");
            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }


    private void Hold()
    {
        try
        {
            while (true)
            {
                /*if (upbreak == true)
                {
                    control = "[Dobot:Hold]";
                    upbreak = false;
                }

                SendMessage(control);*/

                SendMessage("Hold");
                Thread.Sleep(10000);

                if (exitcon == true)
                {
                    break;
                }

            }
        }
        catch (SocketException socketException)
        {
            Debug.Log("Socket exception: " + socketException);
        }
    }


}
