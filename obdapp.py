import tkinter as tk
from tkinter import ttk
import obd

has_connection = None
connection = None

def connect_to_car():
    global connection
    global has_connection
    global connection_status
    connection = obd.OBD()
    if connection.is_connected():
        has_connection = True
        connection_status.config(text="Connected", fg="green")
    else:
        has_connection = False
        connection_status.config(text="Failed to connect", fg="red")
        
def scan_for_dtcs():
    global connection
    global has_connection
    global tree
    global connection_status
    if has_connection:
        dtc_list = connection.query(obd.commands.GET_DTC).value
        for code in dtc_list:
            dtc_code = code[1][0]
            dtc_info = code[1][1]
            tree.insert("", "end", values=(dtc_code, dtc_info))
    else:
        connection_status.config(text="No car connected", fg="red")

def clear_dtcs():
    global connection
    global has_connection
    global connection_status
    if has_connection:
        connection.query(obd.commands.CLEAR_DTC)
        connection_status.config(text="DTCs cleared", fg="green")
    else:
        connection_status.config(text="No car connected", fg="red")

def disconnect_from_car():
    global connection
    global has_connection
    global connection_status
    if has_connection:
        connection.close()
        has_connection = False
        connection_status.config(text="Disconnected", fg="green")
    else:
        connection_status.config(text="No car connected", fg="red")


def clear_tree():
    global tree
    tree.delete(*tree.get_children())

# create the main window
root = tk.Tk()
root.title("OBD App")
root.geometry("800x600")

# create buttons across the top
connect_button = tk.Button(root, text="Connect", command=connect_to_car)
connect_button.grid(row=0, column=0)
disconnect_button = tk.Button(root, text="Disconnect", command=disconnect_from_car)
disconnect_button.grid(row=0, column=1)
scan_button = tk.Button(root, text="Scan", command=scan_for_dtcs)
scan_button.grid(row=0, column=2)
clear_codes_button = tk.Button(root, text="Clear Codes", command=clear_dtcs)
clear_codes_button.grid(row=0, column=3)

# create a label under the buttons to display the connection status in red or green
connection_status = tk.Label(root, text="Not Connected", fg="red")
connection_status.grid(row=1, column=0)

# create a treeview to display the OBD codes
tree = ttk.Treeview(root, columns=("Value"))
tree.grid(row=2, column=0, columnspan=4)
tree.heading("#0", text="Code")
tree.heading("Value", text="Value")
# create a scrollbar to scroll through the treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
scrollbar.grid(row=2, column=5, sticky="ns")
tree.configure(yscrollcommand=scrollbar.set)

# add a clear list button below the treeview
clear_list_button = tk.Button(root, text="Clear List", command=clear_tree)
clear_list_button.grid(row=3, column=0, columnspan=4)





# main loop
root.mainloop()
