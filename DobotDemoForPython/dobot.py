 #-------------------------------------header------------------------------------------------------
from threading import Thread
import DobotDllType as dType
import socket
import os
import subprocess
import time
import struct

#--------------------------------------global var-------------------------------------------------

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

alldata=""
J1angle=0
J2angle=0
J3angle=0


ExitCon=False
ConnectCon=False

#Load Dll
api = dType.load()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    

#---------------------------------Thread ส่งข้อมูล--------------------------------------------------------------------------------
def Thread1():

    global api
    global s
    global J1angle
    global J2angle
    global J3angle

    global ExitCon
    global ConnectCon
    

    while ExitCon == False:  

        if(ConnectCon==True) and (ExitCon==False):  

            time.sleep(5)
            while (ExitCon==False) and (ConnectCon==True): 

                Xpose = dType.GetPoseEx(api, 1)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                Ypose = dType.GetPoseEx(api, 2)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                Zpose = dType.GetPoseEx(api, 3)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                Rpose = dType.GetPoseEx(api, 4)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                J1angle = dType.GetPoseEx(api, 5)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                J2angle = dType.GetPoseEx(api, 6)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   
                J3angle = dType.GetPoseEx(api, 7)
                if(ExitCon==True) or (ConnectCon==False) :
                    break   

                #s.sendall(bytes('[Unity:X='.encode("utf-8")) + bytes(str(Xpose).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:X=' + str(Xpose) + ']').encode("utf-8")))
                        
                
                #s.sendall(bytes('[Unity:Y='.encode("utf-8")) + bytes(str(Ypose).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Y=' + str(Ypose) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:Z='.encode("utf-8")) + bytes(str(Zpose).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Z=' + str(Zpose) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:R='.encode("utf-8")) + bytes(str(Rpose).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:R=' + str(Rpose) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:Ji='.encode("utf-8")) + bytes(str(J1angle).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Ji=' + str(J1angle) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:Jii='.encode("utf-8")) + bytes(str(J2angle).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Jii=' + str(J2angle) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:Jiii='.encode("utf-8")) + bytes(str(J3angle).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Jiii=' + str(J3angle) + ']').encode("utf-8")))

                
                #s.sendall(bytes('[Unity:Jiv='.encode("utf-8")) + bytes(str(J4angle).encode("utf-8")) + bytes(']'.encode("utf-8")))
                s.sendall(bytes(('[Unity:Jiv=' + str(Rpose) + ']').encode("utf-8")))


                if(ExitCon==True) or (ConnectCon==False) :
                    break   
        if(ExitCon==True):
            break  
         

    print("Exit Thread 1")
    


    
#---------------------------------------Thread รับข้อความจาก server-----------------------------
def Thread2(): 

    global api
    global s



    global J1angle
    global J2angle
    global J3angle
    global alldata

    global ExitCon
    global ConnectCon


    while ExitCon==False:


        #msg = s.recv(1024)
        #alldata = msg.decode("utf-8")
        #print('Received : ', alldata )
        #while (ExitCon==False) and (ConnectCon==False):
            #print("1")

        while(alldata.find(']')!=-1) and (ExitCon==False) and (ConnectCon==True):
                
            s.sendall(bytes('[Unity:Hold]'.encode("utf-8")))

            onedata = alldata[alldata.find('['):alldata.find(']')+1]

            x=250
            y=0
            z=0
                
            if(onedata=="[Unity:Xpos]"):
                dType.SetPTPCmdEx(api, 7, 200,  0,  0, 0, 1)
            if(onedata=="[Unity:Xneg]"):
                dType.SetPTPCmdEx(api, 7, (-200),  0,  0, 0, 1)
            if(onedata=="[Unity:Ypos]"):
                dType.SetPTPCmdEx(api, 7, 0,  200,  0, 0, 1)
            if(onedata=="[Unity:Yneg]"):
                dType.SetPTPCmdEx(api, 7, 0,  (-200),  0, 0, 1)
            if(onedata=="[Unity:Zpos]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  200, 0, 1)
            if(onedata=="[Unity:Zneg]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  (-200), 0, 1)
            if(onedata=="[Unity:Rpos]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  0, 200, 1)
            if(onedata=="[Unity:Rneg]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  0, (-200), 1)

            if(onedata=="[Unity:J1pos]"):
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 4, J1angle+90,  J2angle,  J3angle, current_pose[7], 1)
            if(onedata=="[Unity:J1neg]"):
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 4, J1angle-90,  J2angle,  J3angle, current_pose[7], 1)
            if(onedata=="[Unity:J2pos]"):
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 4, J1angle,  J2angle+90,  J3angle, current_pose[7], 1)
            if(onedata=="[Unity:J2neg]"):
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 4, J1angle,  J2angle-90,  J3angle, current_pose[7], 1)
            if(onedata=="[Unity:J3pos]"):
                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 4, J1angle,  J2angle,  J3angle+90, current_pose[7], 1)
            if(onedata=="[Unity:J3neg]"):
                dType.SetPTPCmdEx(api, 4, J1angle,  J2angle,  J3angle-90, current_pose[7], 1)
            if(onedata=="[Unity:J4pos]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  0, 200, 1)
            if(onedata=="[Unity:J4neg]"):
                dType.SetPTPCmdEx(api, 7, 0,  0,  0, (-200), 1)

            if(onedata=="[Unity:ONCUP]"):
                dType.SetEndEffectorSuctionCupEx(api, 1, 1)
            if(onedata=="[Unity:OFFCUP]"):
                dType.SetEndEffectorSuctionCupEx(api, 0, 1)

            if("[Unity:MOV," in onedata):
                                 
                x=onedata[onedata.find(',')+1:onedata.find('!')]
                y=onedata[onedata.find('!')+1:onedata.find('@')]
                z=onedata[onedata.find('@')+1:onedata.find(']')]

                print("x=",x)
                print("y=",y)
                print("z=",z)

                if((x=="")or(y=="")or(z=="")):
                    continue

                current_pose = dType.GetPose(api)
                dType.SetPTPCmdEx(api, 2, int(x),  int(y),  int(z), current_pose[3], 1)
                
            if("[Unity:JUMP," in onedata):  

                x=onedata[onedata.find(',')+1:onedata.find('!')]
                y=onedata[onedata.find('!')+1:onedata.find('@')]
                z=onedata[onedata.find('@')+1:onedata.find(']')]

                print("x=",x)
                print("y=",y)
                print("z=",z)

                if((x=="")or(y=="")or(z=="")):
                    continue

                dType.SetPTPCmdEx(api, 0, int(x),  int(y),  int(z), 0, 1)

            if(onedata=="[Unity:Home]"):
                dType.SetHOMECmdEx(api, 0, 1)

            alldata=alldata[alldata.find(']')+1:len(alldata)]

    print("Exit Thread 2")

            
                

#---------------------------------------thread stop--------------------------------------
def Thread3():

    global ExitCon
    global ConnectCon
    global alldata


    while ExitCon==False:

        msg = s.recv(1024)
        alldata = msg.decode("utf-8")
        print('Received : ', alldata )

        if("[Unity:Stop]" in alldata): 
            #dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdForceStopExec(api)
            #Clean Command Queued
            dType.SetQueuedCmdClear(api)
            #Start to Execute Command Queued
            dType.SetQueuedCmdStartExec(api)

            #continue

        if("[SERVER:CONNECTED]" in alldata):

            s.sendall(bytes('[Dobot:REG]'.encode("utf-8")))

        if("[Unity:CONNECT]" in alldata):

            #Start to Execute Command Queued
            #dType.SetQueuedCmdStartExec(api)

            ConnectCon=True

        
        if("[Unity:DISCONNECT]" in alldata): 
            #dType.SetQueuedCmdStopExec(api)
            #dType.SetQueuedCmdForceStopExec(api)
            #Clean Command Queued
            #dType.SetQueuedCmdClear(api)

            ConnectCon=False

            
        if ("[Unity:EXIT]" in alldata):
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdForceStopExec(api)

            ExitCon=True

            break
        
    print("Exit Thread 3")



            
#----------------------------------------main thread-------------------------------------------

ThreadSend = Thread(target=Thread1)
ThreadRead = Thread(target=Thread2)
ThreadStop = Thread(target=Thread3)

#connect socket
HOST = 'localhost'  # The servers hostname or IP address
PORT = 1150        # The port used by the server

s.connect((HOST, PORT)) 
ThreadStop.start()
ThreadRead.start()
ThreadSend.start()


#------------------------รอ connect server------------------------------------------
#while True:
    #if data == "[SERVER:CONNECTED]":
        #s.sendall(bytes('[Dobot:REG]'.encode("utf-8")))
        #break
    #else : 
        #print("Connecting....")
        #time.sleep(1)
        #s.connect((HOST, PORT)) 

#------------------------รอคำสั่ง connect จาก Unity------------------------------------
while ExitCon==False:
    

    while(ConnectCon==True) and (ExitCon==False):
        #เริ่มรับส่งข้อมูลกับ Unity
        #Connect Dobot
        dType.SearchDobot(api,  maxLen=1000)
        state = dType.ConnectDobot(api, "", 115200)[0] 
        print("Connect status:",CON_STR[state])


        if (state == dType.DobotConnect.DobotConnect_NoError):
                
            #Clean Command Queued
            dType.SetQueuedCmdClear(api)

            #Async Motion Params Setting
            dType.SetEndEffectorSuctionCupEx(api, 0, 1)
            dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
            dType.SetPTPJointParams(api, 200, 100, 200, 100, 200, 100, 200, 100, isQueued = 1)
            dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

            #Async Home
            dType.SetHOMECmd(api, temp = 0, isQueued = 1)

            #Start to Execute Command Queued
            dType.SetQueuedCmdStartExec(api)

            while True:
                if(ConnectCon==False) or (ExitCon==True):
                    #Stop to Execute Command Queued
                    dType.SetQueuedCmdStopExec(api)

                    #Disconnect Dobot
                    dType.DisconnectDobot(api)                     
                    break
    time.sleep(1)   
    
print("Exit mainThread")






