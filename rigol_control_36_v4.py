import tkinter as tk
import socket # for sockets
import select
import sys # for exit
import time # for sleep


remote_ip = "169.254.1.5" #Siglent = "10.0.0.69" #"192.168.0.17" # should match the instrument's IP address
port = 5555 #5024 # the port number of the instrument service
count = 0


read_values = 0
read_values_string = str(read_values)

def application():

    class unitTestGUI(tk.Frame):

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

        def __init__(self, master):
            tk.Frame.__init__(self, master=None)
            master.title("RIGOL DP832A Control")
            self.grid()
            self.createWidgets()

        def createWidgets(self):
            self.read_values = tk.StringVar()
            self.read_values.set(read_values_string)

            b = tk.Button
            e = tk.Entry
            l = tk.Label

            self.ch1b = b(self, text="Channel 1", command=self.ch1_select)
            self.ch1b.grid(row=1, column=0, sticky="EW")
            self.ch1b.config(height=2, width=10)

            self.ch2b = b(self, text="Channel 2", command=self.ch2_select)
            self.ch2b.grid(row=1, column=1, sticky="EW")
            self.ch2b.config(height=2, width=10)

            self.ch3b = b(self, text="Channel 3", command=self.ch3_select)
            self.ch3b.grid(row=1, column=2, sticky="EW")
            self.ch3b.config(height=2, width=10)

            l(self, text="Enter Voltage :") \
                .grid(row=2, sticky="W", columnspan=2)

            self.entry_volt = e(self)
            self.entry_volt.grid(row=3, column=0, sticky="EW", columnspan=3)

            l(self, text="Enter Current Limit :") \
                .grid(row=4, sticky="W", columnspan=2)

            self.entry_curr = e(self)
            self.entry_curr.grid(row=5, column=0, sticky="EW", columnspan=3)

            self.submit = b(self, text="Submit", command=self.submit_entry)
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
            rigol_run()

        def print_channel(self):
            global ch_label
            ch_label = tk.Label(self.master, text=(ch_in + " selected")) \
                .grid(row=10, sticky="W", columnspan=2)

        def volt_meas(self):
            global LAN_SCPI_Code
            global read_values

            so = self.SocketConnect()
            LAN_SCPI_Code = (":MEAS:ALL:DC?")
            LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
            LAN_qStr = self.SocketQuery(so, LAN_SCPI_Code)
            read_values = LAN_qStr
            self.read_values.set(read_values_string)
            root.update_idletasks()
            print(read_values_string)
            self.after(1000, self.volt_meas)

    root = tk.Tk()
    gui = unitTestGUI(root)
    # root.protocol("WM_DELETE_WINDOW", gui.close)
    root.mainloop()


if __name__ == "__main__":
    application()

