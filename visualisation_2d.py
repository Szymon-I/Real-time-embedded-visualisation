import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import communication

# !!! Import Classes for communication from communication.py !!!

# __init__ function creates window with 9 axes for visualisating data
# incoming from 9-axis accelerometer (e.g. MPU-9250)
# Additional parameters:
# a,b: axes limit values
# n: number of samples
# interval: time between frame generation 


class visualisation2d():

    def __init__(self, a=-10, b=10, n=250, interval=2.0):
        self.a = a
        self.b = b
        self.n = n
        self.interval = interval
        self.x = np.arange(n) + 1
        self.f = np.zeros((9, n))
        self.fig, (self.ax1, self.ax2, self.ax3, self.ax4, self.ax5, self.ax6,
                   self.ax7, self.ax8, self.ax9) = plt.subplots(9, 1,
                    figsize=(12, 8), dpi=80, linewidth=1)
        self.fig.suptitle('Sensor', fontsize=16)

        self.ax1.set_ylabel('ax')
        self.ax2.set_ylabel('ay')
        self.ax3.set_ylabel('az')
        self.ax4.set_ylabel('gx')
        self.ax5.set_ylabel('gy')
        self.ax6.set_ylabel('gz')
        self.ax7.set_ylabel('mx')
        self.ax8.set_ylabel('my')
        self.ax9.set_ylabel('mz')

        self.line1, = self.ax1.plot([], [], linestyle='-', color='green')
        self.line2, = self.ax2.plot([], [], linestyle='-', color='blue')
        self.line3, = self.ax3.plot([], [], linestyle='-', color='khaki')
        self.line4, = self.ax4.plot([], [], linestyle='-', color='purple')
        self.line5, = self.ax5.plot([], [], linestyle='-', color='red')
        self.line6, = self.ax6.plot([], [], linestyle='-', color='violet')
        self.line7, = self.ax7.plot([], [], linestyle='-', color='aqua')
        self.line8, = self.ax8.plot([], [], linestyle='-', color='coral')
        self.line9, = self.ax9.plot([], [], linestyle='-', color='chartreuse')

        self.line = [self.line1, self.line2, self.line3, self.line4,
                     self.line5, self.line6, self.line7, self.line8, self.line9]

        self.ax = [self.ax1, self.ax2, self.ax3, self.ax4,
                   self.ax5, self.ax6, self.ax7, self.ax8, self.ax9]

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

    # start visualisation with NULL values
    def start(self):
        style.use('seaborn-bright')
        for i in range(len(self.ax)):
            self.ax[i].set_ylim(self.a, self.b + 1)
            self.ax[i].set_xlim(0, self.n)
            if (i is not len(self.ax) - 1):
                self.ax[i].set_xticklabels([])
        return self.line

    # real time generator for displayed data
    def generator(self):
        y = np.zeros(9)
        while True:
            words=self.recieve()
            for i in range(9):
                y[i]=words[i]
            yield y

    # update data on plot (shift and update)
    def update(self, data):
        for i in range(9):
            self.f[i] = np.roll(self.f[i], -1)
            self.f[i, -1] = data[i]
            self.line[i].set_data(self.x, self.f[i])
        return self.line

    # start matplotlib animation loop
    def animation(self):
        self.ani = animation.FuncAnimation(self.fig, self.update, self.generator,
        init_func=self.start,blit=True, interval=self.interval)
        plt.show()

# ------------------------------ #

# create visualisation instance and start animation with
# given parameters
if __name__ == '__main__':
    anim = visualisation2d()
    anim.com=anim.communication(comm_type="Serial",speed=115200)
    anim.animation()

