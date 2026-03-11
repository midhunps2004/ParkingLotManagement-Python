from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class parking_lot_management:
    def __init__(self, root):
        self.root = root
        self.root.title("Parking Slot Booking")
        self.root.geometry("1200x850+100+50")

        # Variables
        self.OwnerName = StringVar()
        self.VehicleType = StringVar()
        self.VehicleNo = StringVar()
        self.PhoneNo = StringVar()
        self.SlotNo = StringVar()  # New Variable for Slot
        self.Captcha = StringVar()
        self.correct_captcha = "8e95Q"
        self.terms_var = IntVar()
        
        # Track occupied slots in memory
        self.occupied_slots = []

        # Title
        maintitle = Label(self.root, text="Parking Lot Management",
                          font=("times new roman", 25, "bold"),
                          bd=15, relief=GROOVE, bg="#147184", fg="white")
        maintitle.pack(side=TOP, fill=X)

        frame = Frame(self.root, bd=10, relief=RAISED, bg="white")
        frame.place(x=100, y=80, width=1000, height=420)

        # Labels and Entries
        Label(frame, text="Owner Name", font=("times new roman", 13, "bold"), bg="white").place(x=30, y=20)
        ttk.Entry(frame, textvariable=self.OwnerName, font=("times new roman", 15)).place(x=30, y=50, width=300)

        Label(frame, text="Vehicle Type", font=("times new roman", 13, "bold"), bg="white").place(x=30, y=100)
        self.vt_combo = ttk.Combobox(frame, textvariable=self.VehicleType, font=("times new roman", 15), state="readonly")
        self.vt_combo["values"] = ("Select", "Car", "Bike", "Bus")
        self.vt_combo.place(x=30, y=130, width=300)
        self.vt_combo.current(0)

        Label(frame, text="Vehicle Number", font=("times new roman", 13, "bold"), bg="white").place(x=30, y=180)
        ttk.Entry(frame, textvariable=self.VehicleNo, font=("times new roman", 15)).place(x=30, y=210, width=300)

        # SLOT SELECTION
        Label(frame, text="Select Parking Slot", font=("times new roman", 13, "bold"), bg="white").place(x=30, y=260)
        self.slot_combo = ttk.Combobox(frame, textvariable=self.SlotNo, font=("times new roman", 15), state="readonly")
        self.slot_combo["values"] = ("Select", "A1", "A2", "A3", "B1", "B2", "B3", "C1", "C2")
        self.slot_combo.place(x=30, y=290, width=300)
        self.slot_combo.current(0)

        Label(frame, text="Phone Number", font=("times new roman", 13, "bold"), bg="white").place(x=600, y=20)
        ttk.Entry(frame, textvariable=self.PhoneNo, font=("times new roman", 15)).place(x=600, y=50, width=300)

        Label(frame, text=f"CAPTCHA: {self.correct_captcha}", font=("times new roman", 13, "bold"), bg="white", fg="red").place(x=600, y=100)
        ttk.Entry(frame, textvariable=self.Captcha, font=("times new roman", 15)).place(x=600, y=130, width=300)

        Checkbutton(frame, text="Accept terms and conditions", variable=self.terms_var, bg="white").place(x=600, y=180)

        Button(frame, text="Confirm Booking", font=("times new roman", 15, "bold"), bg="#147184", fg="white",
               command=self.confirm).place(x=600, y=240, width=200)

        # Table Area
        tframe = Frame(self.root, bg="#444444", relief=RIDGE, bd=10)
        tframe.place(x=100, y=550, width=1000, height=250)

        scroll_x = ttk.Scrollbar(tframe, orient=HORIZONTAL)
        scroll_y = ttk.Scrollbar(tframe, orient=VERTICAL)

        self.table = ttk.Treeview(tframe,
                                  columns=("ownername", "vehicletype", "vehicleno", "phoneno", "slotno"),
                                  xscrollcommand=scroll_x.set,
                                  yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.table.xview)
        scroll_y.config(command=self.table.yview)

        self.table.heading("ownername", text="Owner Name")
        self.table.heading("vehicletype", text="Type")
        self.table.heading("vehicleno", text="Vehicle No")
        self.table.heading("phoneno", text="Phone No")
        self.table.heading("slotno", text="Slot")
        self.table["show"] = "headings"
        self.table.pack(fill=BOTH, expand=1)
        self.table.bind("<ButtonRelease-1>", self.get_cursor)

        # Control Buttons
        btn_frame = Frame(self.root, bg="white")
        btn_frame.place(x=100, y=510, width=1000, height=40)
        Button(btn_frame, text="Update", command=self.update, width=15).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Delete", command=self.delete, width=15).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Clear", command=self.clear, width=15).pack(side=LEFT, padx=10)
        Button(btn_frame, text="Exit", command=self.exit, width=15).pack(side=LEFT, padx=10)

    def confirm(self):
        slot = self.SlotNo.get()
        if self.OwnerName.get() == "" or self.VehicleType.get() == "Select" or slot == "Select":
            messagebox.showerror("Error", "All fields including Slot are required")
        elif self.Captcha.get() != self.correct_captcha:
            messagebox.showerror("Error", "Wrong CAPTCHA")
        elif self.terms_var.get() == 0:
            messagebox.showerror("Error", "Please accept terms")
        elif slot in self.occupied_slots:
            messagebox.showerror("Error", f"Slot {slot} is not available! Please choose another.")
        else:
            self.table.insert("", END, values=(
                self.OwnerName.get(),
                self.VehicleType.get(),
                self.VehicleNo.get(),
                self.PhoneNo.get(),
                slot
            ))
            self.occupied_slots.append(slot) # Mark as taken
            messagebox.showinfo("Success", f"Slot {slot} booked successfully")
            self.clear()

    def get_cursor(self, event=""):
        cursor_row = self.table.focus()
        content = self.table.item(cursor_row)
        row = content["values"]
        if row:
            self.OwnerName.set(row[0])
            self.VehicleType.set(row[1])
            self.VehicleNo.set(row[2])
            self.PhoneNo.set(row[3])
            self.SlotNo.set(row[4])

    def update(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showerror("Error", "Select a record first")
            return
        
        # Logic to handle slot changing during update
        old_val = self.table.item(selected)['values'][4]
        new_val = self.SlotNo.get()
        
        if new_val != old_val and new_val in self.occupied_slots:
            messagebox.showerror("Error", f"Slot {new_val} is already taken!")
            return

        self.occupied_slots.remove(str(old_val))
        self.table.item(selected, values=(
            self.OwnerName.get(), self.VehicleType.get(),
            self.VehicleNo.get(), self.PhoneNo.get(), new_val
        ))
        self.occupied_slots.append(new_val)
        messagebox.showinfo("Success", "Updated successfully")

    def delete(self):
        selected = self.table.focus()
        if not selected:
            messagebox.showerror("Error", "Select a record first")
        else:
            slot_to_free = self.table.item(selected)['values'][4]
            self.occupied_slots.remove(str(slot_to_free)) # Make slot available again
            self.table.delete(selected)
            messagebox.showinfo("Success", "Deleted and Slot freed")
            self.clear()

    def clear(self):
        self.OwnerName.set("")
        self.VehicleType.set("Select")
        self.VehicleNo.set("")
        self.PhoneNo.set("")
        self.SlotNo.set("Select")
        self.Captcha.set("")
        self.terms_var.set(0)

    def exit(self):
        if messagebox.askyesno("Exit", "Do you want to exit?"):
            self.root.destroy()

if __name__ == "__main__":
    root = Tk()
    app = parking_lot_management(root)
    root.mainloop()

