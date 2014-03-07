from Queue import Queue
import numpy as np
import serial
from pyfirmata import Arduino, util
from collections import deque
import time
from matplotlib import animation 
from matplotlib import pyplot as pl
import threading

PORT = '/dev/tty.usbserial-A700ewsy'
#PORT = '/dev/tty.usbserial-A6004p1X'
board = Arduino(PORT)
it = util.Iterator(board)
it.start()
analog_in = board.get_pin('a:1:i')
digital_out = board.get_pin('d:3:o')
digital_out.write(0)
pl.rcParams['toolbar'] = 'None'
fig = pl.figure()
ax = pl.axes(xlim=(0,50), ylim=(-20,150))
#ax = pl.axes(xlim=(0,50), ylim=(-2,5))
line, = ax.plot([],[])
voltage = deque([0],30)
eventcue = Queue() 
pl.ion()


def main():

 voltplot(eventcue)
 shockthread = threading.Thread(target = shock, args = (eventcue,))
 shockthread.daemon = True
 shockthread.start()


def shock(cue):


# while True:

  time.sleep(1)

  for i in range(5):
             
    print('shock')
    eventcue.put(('write',1))
    time.sleep(.5)
    eventcue.put(('write',0))
    time.sleep(.5)


  board.exit()
 # exit()

def voltplot(cue):


 def init():

   line.set_data([],[])
   return line,#still return line?
  
 def animate(i):
   
   a = time.time()
   eventcue.put('read')
   volt = execute(eventcue)
   voltage.append(volt*5*(1000/33.3))
  # voltage.append(volt*5)
 #  if i == 1:
 
   line.set_data(range(1,len(voltage)+1),voltage)
   pl.hold(False)
 
    
   interval = ((time.time() - a) *1000)
   pl.title('Scalebar: 20 samples =' + str(int(interval*20)) + 'ms')
   return voltage, #probably don't need to return voltage


 print('just before anim')
 anim = animation.FuncAnimation(fig, animate,init_func = init,frames= 10, interval = 1, blit = False)

 pl.show()
 
 print('after show')


def execute(eventcue):
 
#make this a class that's init value is board. 
#analog_in and digital out. only method is execute. 
  
  if not eventcue.empty():

    z = eventcue.get()
    volts = analog_in.read()
   

    if z == 'read':

      return volts

    else:

      c,value = z
      digital_out.write(value)
      return volts

#function returns a new voltage if read, previous voltage if not  


main()
