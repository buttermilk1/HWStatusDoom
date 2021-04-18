# HWStatusDoom
Arduino Based Hardware Monitor


Arduino_DoomDisplay.ino

 *  Hey Reddit! Some Remarks here:
 *  a) doing this for fun, and there are a lot of points to improve/extend. Feel free to use and share!
 *  b) I used it with a 480*320 display on an Arduino Uno Clone
 *  c) Doom Guy wounded state just scales with the GPU Temp which is just a quick "hack" i will likely extend it and play around with it
 *  d) Most Important Have FUN! :) - buttermilk
 
 
SerialServer.py 

 Hey Reddit! some remarks here:
* a) doing this for fun so there are some points that could be handled smoother, sometimes im just lazy :)
* b) add the OpenHarwareMonitorLib.dll to the windows path
* c) execute this file with admin rights otherwise there will be no CPU temp
* d) you should inspect the hardware class and look for the identifiers of your hardware
   i used e.g. '/amdcpu/0/temperature/0' because i have an amd CPU, same goes for GPU etc. 
   It could be extended to work with more hardware but here goes remark a).
* e) Most Important: Have FUN! :) - buttermilk

 
