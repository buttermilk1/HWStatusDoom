import serial
import time
import clr # the pythonnet module.
import threading

from tkinter import *

###############################################
# Hey Reddit! some remarks here:
#a) doing this for fun so there are some points that could be handled smoother, sometimes im just lazy :)
#b) add the OpenHarwareMonitorLib.dll to the windows path
#c) execute this file with admin rights otherwise there will be no CPU temp
#d) you should inspect the hardware class and look for the identifiers of your hardware
#   i used e.g. '/amdcpu/0/temperature/0' because i have an amd CPU, same goes for GPU etc. 
#   It could be extended to work with more hardware but here goes remark a).
#e) Most Important: Have FUN! :) - buttermilk
###############################################


clr.AddReference(r'OpenHardwareMonitorLib')
from OpenHardwareMonitor.Hardware import Computer

# pyinstaller --onefile --windowed --uac-admin SerialTest.py

#GUI INIT
root = Tk()
root.title("Info Display Serial Server")
S = Scrollbar(root)
S.pack(side=RIGHT, fill=Y)
T = Text(root, height=50, width=100)
S.config(command=T.yview)
T.pack()
T.config(yscrollcommand=S.set)


#Configure Open Hardware Lib
c = Computer()
c.CPUEnabled = True # get the Info about CPU
c.GPUEnabled = True # get the Info about GPU
c.MainboardEnabled = True
c.FanControllerEnabled = True
c.HDDEnabled = True
c.RAMEnabled = True
c.Open()


#Message Send Delay, we could sent multiple commands with same message but we are lazy and only sent one command with every message, this is the time between the messages
#crappy com structure but works
MsgDelay = 0.15;


#Settings for Serial Interface
ser = serial.Serial()
ser.baudrate = 115200
ser.port = 'COM3'



def TK_print(out):
    T.insert(END, out)
    T.insert(END, "\n")

def ServerInit():
    Success = True;
    try: 
        ser.open()
    except:
        TK_print("Could Not Open Serial Connection")
        Success = False;

    if(Success): 
        root.after(0, ServerLoop) 
        TK_print("Opened Serial Connection")
    else: root.after(1000, ServerInit) 



def ServerLoop():

    for a in range(0,len(c.Hardware)):
        c.Hardware[a].Update()        

    for a in range(0, len(c.Hardware[1].Sensors)):
                if '/amdcpu/0/temperature/0' in str(c.Hardware[1].Sensors[a].Identifier):
                    ser.write((" A" + str(round(c.Hardware[1].Sensors[a].get_Value()))).encode())
                    TK_print("CPU TEMP")
                    TK_print(c.Hardware[1].Sensors[a].get_Value())
                    
    time.sleep(MsgDelay)
                    
    for a in range(0, len(c.Hardware[3].Sensors)):
                if '/nvidiagpu/0/temperature/0' in str(c.Hardware[3].Sensors[a].Identifier):
                    #print(c.Hardware[1].Sensors[a].get_Value())
                    ser.write((" B" + str(round(c.Hardware[3].Sensors[a].get_Value()))).encode())    
    time.sleep(MsgDelay)
            
    for a in range(0, len(c.Hardware[1].Sensors)):
                if '/amdcpu/0/load/0' in str(c.Hardware[1].Sensors[a].Identifier):
                    if(c.Hardware[1].Sensors[a].get_Value()!=None):
                        ser.write((" C" + str(round(c.Hardware[1].Sensors[a].get_Value()))).encode())
                        #print("LOAD")
                        #print(c.Hardware[1].Sensors[a].get_Value())
                        #ser.write((" C50").encode() )
                    else:
                        print("INVALID LOAD")

    time.sleep(MsgDelay)
                           
    for a in range(0, len(c.Hardware[3].Sensors)):
                if '/nvidiagpu/0/load/0' in str(c.Hardware[3].Sensors[a].Identifier):
                    #print(c.Hardware[1].Sensors[a].get_Value())
                    ser.write((" D" + str(round(c.Hardware[3].Sensors[a].get_Value()))).encode())   
                    #ser.write((" D50").encode() )
                                
    time.sleep(MsgDelay)

    for a in range(0,len(c.Hardware[0].SubHardware)):
        c.Hardware[0].SubHardware[a].Update();
        for b in range(0, len(c.Hardware[0].SubHardware[a].Sensors)):
            if '/lpc/nct6797d/temperature/1' in str(c.Hardware[0].SubHardware[a].Sensors[b].Identifier):
                    ser.write((" E" + str(round(c.Hardware[0].SubHardware[a].Sensors[b].get_Value()))).encode())
                    time.sleep(MsgDelay)
            if '/lpc/nct6797d/fan/3' in str(c.Hardware[0].SubHardware[a].Sensors[b].Identifier):
                    ser.write((" F" + str(round(c.Hardware[0].SubHardware[a].Sensors[b].get_Value()))).encode())
                    time.sleep(MsgDelay)
    
    for a in range(0, len(c.Hardware[2].Sensors)):
            if '/ram/load/0' in str(c.Hardware[2].Sensors[a].Identifier):
                #print(c.Hardware[1].Sensors[a].get_Value())
                ser.write((" G" + str(round(c.Hardware[2].Sensors[a].get_Value()))).encode()) 
                time.sleep(MsgDelay)
    
                        
    for a in range(0,len(c.Hardware)):
        c.Hardware[a].Update()
    
    root.after(300, ServerLoop)
           

root.after(0, ServerInit) 
mainloop()

    