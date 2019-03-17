
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import numpy as np
import sys
import communication

# !!! Import Classes for communication from communication.py !!!

# __init__ function creates full hd (1920x1080)
# window along with spherical object

class visualisation3d():


    def __init__(self):
        
        self.traces = dict()
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.opts['distance'] = 50
        self.w.setWindowTitle('Animation 3D')
        self.w.setGeometry(0,0,1920,1080)
        self.w.setCameraPosition(distance=100)
        self.w.show()

        # create grid display
        gx = gl.GLGridItem()
        gx.rotate(90, 0, 1, 0)
        gx.translate(-20, 0,0)
        gx.scale(2,2,2)
        self.w.addItem(gx)
        gy = gl.GLGridItem()
        gy.rotate(90, 1, 0, 0)
        gy.translate(0, -20, 0)
        gy.scale(2, 2, 2)
        self.w.addItem(gy)
        gz = gl.GLGridItem()
        gz.translate(0, 0, -20)
        gz.scale(2, 2, 2)
        self.w.addItem(gz)

        # create yellow-orange spherical object 
        self.md = gl.MeshData.sphere(rows=30, cols=30, radius=4)
        self.colors = np.random.random(size=(self.md.faceCount(), 4))
        self.colors = np.ones((self.md.faceCount(), 4), dtype=float)
        self.colors[::, 2] = 0
        self.colors[:, 1] = np.linspace(0, 1, self.colors.shape[0])
        self.md.setFaceColors(self.colors)
        self.mx= gl.GLMeshItem(meshdata=self.md, smooth=False)

        self.w.addItem(self.mx)
        self.i=0
        self.cords=[0.0]*6
        self.sensitive=0.1

        self.com=communication(comm_type="Serial")

    # return instance of given communication type
    def communication(self,comm_type="Serial",ip='192.168.1.101',
                    port=1234,com='COM3',speed=115200):
        if(comm_type is "Serial"):
            return communication.Serial(com,speed)
        if(comm_type is "UDP"):
            return communication.UdpServer(ip,port)
        if(comm_type is "TCP"):
            return communication.TcpServer(ip,port)

    # recieve incoming data from given communication class
    def recieve(self):
        return self.com.recieve()

    # start app
    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    # filter small vibrations
    def vibration_filter(self):
        if(abs(self.cords[3]-self.cords[0])>self.sensitive or abs(self.cords[4]-self.cords[1])>self.sensitive
                or abs(self.cords[5]-self.cords[2])>self.sensitive):
            return True
        else:
            return False

    # update actual sphere position according to actual position and
    # input data from accelerometer
    def update(self):
        words = self.recieve()
        for i in range(3):
            self.cords[i]=self.cords[i+3]
            self.cords[i + 3]=float(words[i])

        if (self.vibration_filter() or self.i == 0):
            self.mx.translate((self.cords[3] - self.cords[0]), (self.cords[4] - self.cords[1]),
            (self.cords[5] - self.cords[2]), local=False)

        # print information packets counter 
        self.i+=1
        print(self.i)

    # start animation without timeout
    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(0)
        self.start()

# ------------------------------ #

# create visualisation instance and start animation with
# given parameters
if __name__ == '__main__':
    anim= visualisation3d()
    anim.com=anim.comunikacja(comm_type="Serial",speed=115200)
    anim.animation()