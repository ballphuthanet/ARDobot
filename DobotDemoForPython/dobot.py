
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

#เงื่อนไขที่จะเอาไว้หลุด loop
ExitCon=False
ConnectCon=False

#Load Dll ของ Dobot
api = dType.load()

#ให้ s แทน socket.socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    

#---------------------------------Thread ส่งข้อมูล--------------------------------------------------------------------------------
def Thread1():

    #บอกให้รู้ว่านี้คือตัวแปร global
    global api
    global s
    global J1angle
    global J2angle
    global J3angle

    global ExitCon
    global ConnectCon
    
    #ดักเวลากดออกจะได้หลุด Loop
    while ExitCon == False:  
        #ถ้ากด Connect ให้เริ่มส่งต่าตำแหน่งของ Dobot ไปยัง Unity
        if(ConnectCon==True) and (ExitCon==False):  

            time.sleep(5)
            while (ExitCon==False) and (ConnectCon==True): #วนให้ส่งเรื่อยๆจนกว่าจะกดออก

                #คำสั่งรับค่าจากจุดต่างๆ    
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

                #ส่งไปยัง Server ให้ส่งข้อมูลไปยัง Dobot
                s.sendall(bytes(('[Unity:X=' + str(Xpose) + ']').encode("utf-8")))                      
                s.sendall(bytes(('[Unity:Y=' + str(Ypose) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:Z=' + str(Zpose) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:R=' + str(Rpose) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:Ji=' + str(J1angle) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:Jii=' + str(J2angle) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:Jiii=' + str(J3angle) + ']').encode("utf-8")))
                s.sendall(bytes(('[Unity:Jiv=' + str(Rpose) + ']').encode("utf-8")))


                if(ExitCon==True) or (ConnectCon==False) :
                    break   
        if(ExitCon==True):
            break  
         

    print("Exit Thread 1")
    


    
#---------------------------------------Thread รับข้อความจาก server-----------------------------
def Thread2(): 

    #บอกให้รู้ว่านี้คือตัวแปร global
    global api
    global s

    global J1angle
    global J2angle
    global J3angle
    global alldata

    global ExitCon
    global ConnectCon

    #ดักเวลากดออกจะได้หลุด Loop
    while ExitCon==False:

        #วนดูทีละคำสั่งจากการ Steam ค่าจาก Server 1ครั้ง
        while(alldata.find(']')!=-1) and (ExitCon==False) and (ConnectCon==True):
                
            s.sendall(bytes('[Unity:Hold]'.encode("utf-8")))

            onedata = alldata[alldata.find('['):alldata.find(']')+1]

            x=250
            y=0
            z=0

            #เช็คคำสั่งต่างๆที่ได้รับมาจาก Server
             
            #ขยับแกน x,y,z   
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

            #ขยับ Joint
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

            #เปิด/ปิด ที่ดูด
            if(onedata=="[Unity:ONCUP]"):
                dType.SetEndEffectorSuctionCupEx(api, 1, 1)
            if(onedata=="[Unity:OFFCUP]"):
                dType.SetEndEffectorSuctionCupEx(api, 0, 1)

            #ขยับแบบ MOV โดยกรองค่า x,y,z
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

            #ขยับแบบ JUMP โดยกรองค่า x,y,z    
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

            #กลับไปที่ Home
            if(onedata=="[Unity:Home]"):
                dType.SetHOMECmdEx(api, 0, 1)

            alldata=alldata[alldata.find(']')+1:len(alldata)]

    print("Exit Thread 2")

            
                

#---------------------------------------thread stop--------------------------------------
def Thread3():

    #บอกให้รู้ว่านี้คือตัวแปร global
    global ExitCon
    global ConnectCon
    global alldata

    #ดักเวลากดออกจะได้หลุด Loop
    while ExitCon==False:

        #รับค่า จาก Server
        msg = s.recv(1024)
        alldata = msg.decode("utf-8")
        print('Received : ', alldata )

        if("[Unity:Stop]" in alldata): 

            dType.SetQueuedCmdForceStopExec(api)
            dType.SetQueuedCmdClear(api)
            dType.SetQueuedCmdStartExec(api)

            #continue

        if("[SERVER:CONNECTED]" in alldata):

            s.sendall(bytes('[Dobot:REG]'.encode("utf-8")))

        if("[Unity:CONNECT]" in alldata):

            ConnectCon=True

        
        if("[Unity:DISCONNECT]" in alldata): 

            ConnectCon=False

            
        if ("[Unity:EXIT]" in alldata):
            dType.SetQueuedCmdStopExec(api)
            dType.SetQueuedCmdForceStopExec(api)

            ExitCon=True

            break
        
    print("Exit Thread 3")



            
#----------------------------------------main thread-------------------------------------------

#กำหนดว่า ฟังก์ชั่นไหนเป็น Thread บ้าง
ThreadSend = Thread(target=Thread1)
ThreadRead = Thread(target=Thread2)
ThreadStop = Thread(target=Thread3)

#connect socket
HOST = 'localhost'  # The servers hostname or IP address
PORT = 1150        # The port used by the server
s.connect((HOST, PORT)) 

#เริ่ม Thread
ThreadStop.start()
ThreadRead.start()
ThreadSend.start()

#------------------------รอคำสั่ง connect จาก Unity------------------------------------

#ดักเวลากดออกจะได้หลุด Loop
while ExitCon==False:
    
    #เมื่อกด Connect
    while(ConnectCon==True) and (ExitCon==False):
        #เริ่มรับส่งข้อมูลกับ Unity
        #Connect Dobot
        dType.SearchDobot(api,  maxLen=1000)
        state = dType.ConnectDobot(api, "", 115200)[0] 
        print("Connect status:",CON_STR[state])


        if (state == dType.DobotConnect.DobotConnect_NoError):
                
            #Clean Command Queued
            dType.SetQueuedCmdClear(api)

            #Async Motion Params Setting เซ็ตค่า
            dType.SetEndEffectorSuctionCupEx(api, 0, 1)
            dType.SetHOMEParams(api, 250, 0, 50, 0, isQueued = 1)
            dType.SetPTPJointParams(api, 200, 100, 200, 100, 200, 100, 200, 100, isQueued = 1)
            dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

            #Async Home
            dType.SetHOMECmd(api, temp = 0, isQueued = 1)

            #Start to Execute Command Queued
            dType.SetQueuedCmdStartExec(api)

            #วนทำงานจนกว่าจะกดออก
            while True:
                if(ConnectCon==False) or (ExitCon==True):
                    #Stop to Execute Command Queued
                    dType.SetQueuedCmdStopExec(api)

                    #Disconnect Dobot
                    dType.DisconnectDobot(api)                     
                    break
    time.sleep(1)   
    
print("Exit mainThread")






