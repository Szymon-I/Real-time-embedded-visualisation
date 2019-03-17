# Classes provide communication with different protocols.
# Default values can be changed in Class __init__ function
# In Serial you need to provide COM port with baudrate
# In UDP and TCP you need to provide server ip from lan network
# with communication port
# All classes provides receive method which start listening for
# incoming data and return it for visualisation program

#Class for Serial port communication
class Serial:

    def __init__(self,com='COM3',speed=115200):
        import serial
        self.s = serial.Serial(com,speed)

    def recieve(self):
        line = self.s.readline()
        line = line.decode()
        line = line.rstrip("\n\r")
        words = line.split("/")
        return words

#Class for TCP communication
class UdpServer:

    def __init__(self, ip='192.168.1.101', port=1234):
        import socket
        self.specs=(ip,port)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_socket.bind(self.specs)

    def recieve(self):
        data, adress = self.server_socket.recvfrom(1024)
        return data.decode()

#Class for UDP communication
class TcpServer:

    def __init__(self,ip='192.168.1.101',port=1234):
        import socket
        self.specs=(ip,port)
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind(self.specs)
        self.s.listen(1)

    def recieve(self):
        conn, addr = s.accept()
        data = conn.recv(1024).decode()
        return data
# ------------------------------ #
