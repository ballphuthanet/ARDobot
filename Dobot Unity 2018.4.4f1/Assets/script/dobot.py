import threading
import DobotDllType as dType
import socket
import os
import subprocess

CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"}

#Load Dll
api = dType.load()

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
    dType.SetPTPJointParams(api, 200, 200, 200, 200, 200, 200, 200, 200, isQueued = 1)
    dType.SetPTPCommonParams(api, 100, 100, isQueued = 1)

    #Async Home
    dType.SetHOMECmd(api, temp = 0, isQueued = 1)

    #Start to Execute Command Queued
    dType.SetQueuedCmdStartExec(api)

    #connect server
    HOST = 'localhost'    # The remote host
    PORT = 1150              # The same port as used by the server

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    s.sendall('[Dobot:REG]')

    #main loop
    while True :

        data = s.recv(1024)
        #s.close()
        function = str(data)
        print('Received'+ function)

        
    
    

        

        
   
    #Stop to Execute Command Queued
    dType.SetQueuedCmdStopExec(api)
    
#Disconnect Dobot
dType.DisconnectDobot(api)


def xPos():


switcher={
    "X+": 1,
    "X-": 2,
    "Y+": 3
    "Y-": 1,
    "Z+": 2,
    "Z-": 1,
    "R+": 2,
    "R-": 1,
    "J1+": 2,
    "J1-": 1,
    "J2+": 2,
    "J2-": 1,
    "J3+": 2,
    "J3-": 1,
    "J4+": 2,
    "J4-": 1,
}

    #print(data[k])

