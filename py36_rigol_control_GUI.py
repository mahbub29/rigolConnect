import tkinter as tk
from py36RigolControl import rigol_run

remote_ip = "169.254.1.5" #Siglent = "10.0.0.69" #"192.168.0.17" # should match the instrument's IP address
port = 5555 #5024 # the port number of the instrument service
count = 0


def ch1_select():
    global ch_in
    ch_in = "CH1"
    print_channel()
    print(ch_in + " selected...")
    return ch_in

def ch2_select():
    global ch_in
    ch_in = "CH2"
    print_channel()
    print(ch_in + " selected...")
    return ch_in

def ch3_select():
    global ch_in
    ch_in = "CH3"
    print_channel()
    print(ch_in + " selected...")
    return ch_in

def submit_entry():
    global volt_in
    volt_in = entry.get()
    print("Voltage = " + volt_in + " V")
    rigol_run()

def print_channel():
    global ch_label
    ch_label = tk.Label(window, text=(ch_in + " selected"))\
        .grid(row=5, sticky="W", columnspan=2)


window = tk.Tk()
window.title("Rigol DP832A Control Tool")

tk.Label(window, text="Select a Channel:").grid(row=0, sticky="W", columnspan=2)

b = tk.Button
e = tk.Entry

ch1b = b(window, text="Channel 1", command=ch1_select)
ch2b = b(window, text="Channel 2", command=ch2_select)
ch3b = b(window, text="Channel 3", command=ch3_select)
entry = e(window)
submit = b(window, text="Submit", command=submit_entry)

ch1b.grid(row=1, column=0, sticky="EW")
ch2b.grid(row=1, column=1, sticky="EW")
ch3b.grid(row=1, column=2, sticky="EW")

tk.Label(window, text="Enter Voltage:").grid(row=2, sticky="W", columnspan=2)

entry.grid(row=3, column=0, sticky="EW", columnspan=3)

submit.grid(row=4, column=1, sticky="EW")

window.mainloop()