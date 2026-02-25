import customtkinter as ctk
from database import get_db_connection

class AdminFrame(ctk.CTkFrame):
    def __init__(self, master, logout_callback):
        super().__init__(master)
        self.logout_callback = logout_callback
        
        ctk.CTkLabel(self, text="Admin Panel", font=("Arial", 24, "bold")).pack(pady=10)
        
        # Budget Selection
        self.budget_var = ctk.StringVar(value="2000-4000")
        ctk.CTkLabel(self, text="Select Budget Category:").pack()
        ctk.CTkComboBox(self, values=["2000-4000", "4000-6000", "6000-8000", "8000-10000"], 
                        variable=self.budget_var).pack(pady=5)
        
        # Input Fields
        self.name_entry = ctk.CTkEntry(self, placeholder_text="City Name (e.g. Mumbai)")
        self.name_entry.pack(pady=5)
        self.img_entry = ctk.CTkEntry(self, placeholder_text="Place Image (mumbai.jpg)")
        self.img_entry.pack(pady=5)
        
        self.rest_name = ctk.CTkEntry(self, placeholder_text="Restaurant Name")
        self.rest_name.pack(pady=5)
        self.rest_img = ctk.CTkEntry(self, placeholder_text="Restaurant Image")
        self.rest_img.pack(pady=5)

        self.hotel_name = ctk.CTkEntry(self, placeholder_text="Hotel Name")
        self.hotel_name.pack(pady=5)
        self.hotel_img = ctk.CTkEntry(self, placeholder_text="Hotel Image")
        self.hotel_img.pack(pady=5)
        
        ctk.CTkButton(self, text="Add to Database", command=self.save_data, fg_color="green").pack(pady=15)
        ctk.CTkButton(self, text="Logout", command=logout_callback, fg_color="gray").pack()

    def save_data(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO travel_spots (budget_range, name, place_img, rest_name, rest_img, hotel_name, hotel_img) VALUES (?,?,?,?,?,?,?)",
                       (self.budget_var.get(), self.name_entry.get(), self.img_entry.get(), 
                        self.rest_name.get(), self.rest_img.get(), self.hotel_name.get(), self.hotel_img.get()))
        conn.commit()
        conn.close()
        self.name_entry.delete(0, 'end') # Clear fields
        print("Data Added Successfully!")
