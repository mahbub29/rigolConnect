import tkinter as tk
import socket # for sockets
import select
import sys # for exit
import time # for sleep

remote_ip = "169.254.1.5" #Siglent = "10.0.0.69" #"192.168.0.17" # should match the instrument's IP address
port = 5555 #5024 # the port number of the instrument service
count = 0



# def __init__(self, tkRoot, taskFuncPointer, freqencyMillis):
#     self.__tk_ = tkRoot
#     self.__func_ = taskFuncPointer
#     self.__freq_ = freqencyMillis
#     self.__isRunning_ = False
#
# def isRunning(self): return self.__isRunning_
#
# def start(self):
#     self.__isRunning_ = True
#     self.__onTimer()
#
# def stop(self): self.__isRunning_ = False
#
# def __onTimer(self):
#     if self.__isRunning_:
#         self.__func_()
#         self.__tk_.after(self.__freq_, self.__onTimer)
#
#
#
# def threadingtest():
#     from time import sleep
#
#     class UnitTestGUI:
#


def SocketConnect():
    try:
        #create an AF_INET, STREAM socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket.')
        sys.exit()
    try:
        #Connect to remote server
        s.connect((remote_ip , port))
        r, _, _ = select.select([s], [], [],0.5)
        if r:
            info = s.recv(4096)
            print(info)
    except socket.error:
        print('failed to connect to ip ' + remote_ip)
        print(socket.error)
    return s

def SocketQuery(Sock, cmd):
    reply = None
    try :
        #Send cmd string
        Sock.sendall(cmd)
        print(time.time())
        time.sleep(1)
    except socket.error:
        #Send failed
        print('Send failed')
        sys.exit()
    r, _, _ = select.select([Sock], [], [],0.5)
    if r:
       reply = Sock.recv(4096)
    return reply

def SocketClose(Sock):
    #close the socket
    Sock.shutdown(1)
    time.sleep(5)
    Sock.close()
    time.sleep(.300)

def rigol_run():
    try:
        so = SocketConnect()
        SocketQuery(so, b'*IDN?\n')
        if 1:
            LAN_SCPI_Code = ("APPL " + ch_in + "," + volt_entry() + "," + curr_entry())
            LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
            LAN_qStr = SocketQuery(so, LAN_SCPI_Code)
            print(time.time())
            print("RIG Says: " + str(LAN_qStr))

        SocketClose(so)
    # except KeyboardInterrupt:
    #     print("Program Interrupted and Closed")
    #     sys.exit()

    except NameError:
        no_ch_select()

def ch1_select():
    global ch_in
    ch_in = "CH1"
    print(ch_in + " selected...")
    print_channel()
    return ch_in

def ch2_select():
    global ch_in
    ch_in = "CH2"
    print(ch_in + " selected...")
    print_channel()
    return ch_in

def ch3_select():
    global ch_in
    ch_in = "CH3"
    print(ch_in + " selected...")
    print_channel()
    return ch_in

def volt_entry():
    global volt_in
    volt_in = entry_volt.get()
    print("Voltage = " + volt_in + "V")
    return volt_in

def curr_entry():
    global curr_in
    curr_in = entry_curr.get()
    print("Current = " + curr_in + "A")
    return curr_in

def submit_entry():
    rigol_run()

def print_channel():
    global ch_label
    ch_label = tk.Label(window, text=(ch_in + " selected"))\
        .grid(row=10, sticky="W", columnspan=2)

# def no_ch_select():
#     no_ch_label = tk.Label(window, text="Please select a channel")\
#         .grid(row=7, sticky="W", columnspan=2)

def volt_meas():
    global LAN_SCPI_code
    so = SocketConnect()
    # SocketQuery(so, b'*IDN?\n')
    if 1:
        LAN_SCPI_Code = (":MEAS:ALL:DC?")
        LAN_SCPI_Code = bytes(LAN_SCPI_Code + "\n", "utf-8")
        LAN_qStr = SocketQuery(so, LAN_SCPI_Code)
        #window.after(1000, volt_meas)
        print(LAN_qStr)
        return str(LAN_qStr)

# def volt_meas_update():
#     start_time = time.time()
#     interval = 1
#     for i in range(20):
#         time.sleep(start_time + i*interval - time.time())
#         volt_meas()


#############    G . U . I     C  O  D  E    ################

window = tk.Tk()
window.title("Rigol DP832A Control Tool")

# window.columnconfigure(3, {'minsize': 50})
# window.columnconfigure(4, {'minsize': 50})
# window.columnconfigure(5, {'minsize': 50})

tk.Label(window, text="Select a Channel:").grid(row=0, sticky="W", columnspan=2)

b = tk.Button
e = tk.Entry

ch1b = b(window, text="Channel 1", command=ch1_select)
ch2b = b(window, text="Channel 2", command=ch2_select)
ch3b = b(window, text="Channel 3", command=ch3_select)
entry_volt = e(window)
entry_curr = e(window)
submit = b(window, text="Submit", command=submit_entry)

ch1b.config(height=2, width=10)
ch2b.config(height=2, width=10)
ch3b.config(height=2, width=10)

ch1b.grid(row=1, column=0, sticky="EW")
ch2b.grid(row=1, column=1, sticky="EW")
ch3b.grid(row=1, column=2, sticky="EW")

tk.Label(window, text="Enter Voltage:").grid(row=2, sticky="W", columnspan=2)

entry_volt.grid(row=3, column=0, sticky="EW", columnspan=3)

curr_label = tk.Label(window, text="Enter Current Limit:").grid(row=4, sticky="W", columnspan=2)

entry_curr.grid(row=5, column=0, sticky="EW", columnspan=3)

submit.config(height=2, width=10)

submit.grid(row=6, column=1, sticky="EW")

tk.Label(window, text="Voltage:").grid(row=7, column=0, sticky="W", columnspan=2)
tk.Label(window, text="Current:").grid(row=8, column=0, sticky="W", columnspan=2)
tk.Label(window, text="Power:").grid(row=9, column=0, sticky="W", columnspan=2)
tk.Label(window, text=volt_meas()[2:8]).grid(row=7, column=2, sticky="E")
tk.Label(window, text=volt_meas()[9:15]).grid(row=8, column=2, sticky="E")
tk.Label(window, text=volt_meas()[16:21]).grid(row=9, column=2, sticky="E")

# tk.Label(window, text="No Channel selected").grid(row=5, sticky="W", columnspan=2)

window.mainloop()