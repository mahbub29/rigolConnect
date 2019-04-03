import threading
import tkinter as tk
import socket # for sockets
import select
import sys # for exit
import time # for sleep


remote_ip = "169.254.1.5" #Siglent = "10.0.0.69" #"192.168.0.17" # should match the instrument's IP address
port = 5555 #5024 # the port number of the instrument service
count = 0


# class TkRepeatingTask():
#
#     def __init__( self, tkRoot, taskFuncPointer, freqencyMillis ):
#         self.__tk_   = tkRoot
#         self.__func_ = taskFuncPointer
#         self.__freq_ = freqencyMillis
#         self.__isRunning_ = False
#
#     def isRunning( self ) : return self.__isRunning_
#
#     def start( self ) :
#         self.__isRunning_ = True
#         self.__onTimer()
#
#     def stop( self ) : self.__isRunning_ = False
#
#     def __onTimer( self ):
#         if self.__isRunning_ :
#            self.__func_()
#            self.__tk_.after( self.__freq_, self.__onTimer )
#
#
# class BackgroundTask():
#
#     def __init__(self, taskFuncPointer):
#         self.__taskFuncPointer_ = taskFuncPointer
#         self.__workerThread_ = None
#         self.__isRunning_ = False
#
#     def taskFuncPointer( self ) : return self.__taskFuncPointer_
#
#     def isRunning( self ) :
#         return self.__isRunning_ and self.__workerThread_.isAlive()
#
#     def start( self ):
#         if not self.__isRunning_ :
#             self.__isRunning_ = True
#             self.__workerThread_ = self.WorkerThread( self )
#             self.__workerThread_.start()
#
#     def stop( self ) : self.__isRunning_ = False
#
#     class WorkerThread( threading.Thread ):
#         def __init__( self, bgTask ):
#             threading.Thread.__init__( self )
#             self.__bgTask_ = bgTask
#
#         def run( self ):
#             try :
#                 self.__bgTask_.taskFuncPointer()( self.__bgTask_.isRunning )
#             except Exception as e: print (repr(e))
#             self.__bgTask_.stop()
#


def tkThreadingTest():

    class UnitTestGUI(tk.Tk):
        def __init__(self, master):
            self.master = master
            master.title("RIGOL DP832A Control")

            b = tk.Button
            e = tk.Entry
            l = tk.Label

            self.ch1b = b(self.master, text="Channel 1", command=self.ch1_select)
            self.ch1b.grid(row=1, column=0, sticky="EW")
            self.ch1b.config(height=2, width=10)

            self.ch2b = b(self.master, text="Channel 2", command=self.ch2_select)
            self.ch2b.grid(row=1, column=1, sticky="EW")
            self.ch2b.config(height=2, width=10)

            self.ch3b = b(self.master, text="Channel 3", command=self.ch3_select)
            self.ch3b.grid(row=1, column=2, sticky="EW")
            self.ch3b.config(height=2, width=10)

            l(self.master, text="Enter Voltage :")\
                .grid(row=2, sticky="W", columnspan=2)

            self.entry_volt = e(self.master)
            self.entry_volt.grid(row=3, column=0, sticky="EW", columnspan=3)

            l(self.master, text="Enter Current Limit :")\
                .grid(row=4, sticky="W", columnspan=2)

            self.entry_curr = e(self.master)
            self.entry_curr.grid(row=5, column=0, sticky="EW", columnspan=3)

            self.submit = b(self.master, text="Submit", command=self.submit_entry)
            self.submit.grid(row=6, column=1, sticky="EW")
            self.submit.config(height=2, width=10)

            # l(self.master, text="Voltage :").grid(row=7, column=0, sticky="W", columnspan=2)
            # l(self.master, textvariable=self.volt_meas()).grid(row=7, column=2, sticky="E")
            #
            # l(self.master, text="Current :").grid(row=8, column=0, sticky="W", columnspan=2)
            # l(self.master, textvariable=self.volt_meas()).grid(row=8, column=2, sticky="E")
            #
            # l(self.master, text="Power :").grid(row=9, column=0, sticky="W", columnspan=2)
            # l(self.master, textvariable=self.volt_meas()).grid(row=9, column=2, sticky="E")

            self.LAN_qStr = tk.StringVar()
            l(self.master, textvariable=self.volt_meas) \
                .grid(row=7, column=0, sticky="W", columnspan=2)
            self.TimerInterval = 5000

            self.volt_meas()

        def SocketConnect(self):
            try:
                # create an AF_INET, STREAM socket (TCP)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            except socket.error:
                print('Failed to create socket.')
                sys.exit()
            try:
                # Connect to remote server
                s.connect((remote_ip, port))
                r, _, _ = select.select([s], [], [], 0.5)
                if r:
                    info = s.recv(4096)
                    print(info)
            except socket.error:
                print('failed to connect to ip ' + remote_ip)
                print(socket.error)
            return s

        def SocketQuery(self, Sock, cmd):
            reply = None
            try:
                # Send cmd string
                Sock.sendall(cmd)
                print(time.time())
                time.sleep(1)
            except socket.error:
                # Send failed
                print('Send failed')
                sys.exit()
            r, _, _ = select.select([Sock], [], [], 0.5)
            if r:
                reply = Sock.recv(4096)
            return reply

        def SocketClose(self, Sock):
            # close the socket
            Sock.shutdown(1)
            time.sleep(5)
            Sock.close()
            time.sleep(.300)

        def rigol_run(self):
            try:
                so = self.SocketConnect()
                self.SocketQuery(so, b'*IDN?\n')
                # if 1:
                LAN_SCPI_Code = ("APPL " + ch_in + "," + self.volt_entry()\
                                 + "," + self.curr_entry())
                LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
                LAN_qStr = self.SocketQuery(so, LAN_SCPI_Code)
                print(time.time())
                print("RIG Says: " + str(LAN_qStr))

                self.SocketClose(so)
            except KeyboardInterrupt:
                print("Program Interrupted and Closed")
                sys.exit()

            # except NameError:
            #     no_ch_select()


        def ch1_select(self):
            global ch_in
            ch_in = "CH1"
            print(ch_in + " selected...")
            self.print_channel()
            return ch_in

        def ch2_select(self):
            global ch_in
            ch_in = "CH2"
            print(ch_in + " selected...")
            self.print_channel()
            return ch_in

        def ch3_select(self):
            global ch_in
            ch_in = "CH3"
            print(ch_in + " selected...")
            self.print_channel()
            return ch_in

        def volt_entry(self):
            global volt_in
            volt_in = self.entry_volt.get()
            print("Voltage = " + volt_in + "V")
            return volt_in

        def curr_entry(self):
            global curr_in
            curr_in = self.entry_curr.get()
            print("Current = " + curr_in + "A")
            return curr_in

        def submit_entry(self):
            self.rigol_run()

        def print_channel(self):
            global ch_label
            ch_label = tk.Label(self.master, text=(ch_in + " selected"))\
                .grid(row=10, sticky="W", columnspan=2)

        def volt_meas(self):
            # so = SocketConnect()
            # if 1:
            #     LAN_SCPI_Code = (":MEAS:ALL:DC?")
            #     LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
            #     self.LAN_qStr = SocketQuery(so, LAN_SCPI_Code)
            #     self.after(self.TimerInterval, self.volt_meas)

            global LAN_SCPI_code
            so = self.SocketConnect()
            # SocketQuery(so, b'*IDN?\n')
            if 1:
                LAN_SCPI_Code = (":MEAS:ALL:DC?")
                LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
                LAN_qStr = self.SocketQuery(so, LAN_SCPI_Code)
                self.master.after(1000, self.volt_meas)
                print(LAN_qStr)
                return str(LAN_qStr)

    root = tk.Tk()
    gui = UnitTestGUI(root)
    # root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()


if __name__ == "__main__":
    tkThreadingTest()


