import customtkinter as ctk
from PIL import Image
import os
from database import init_db, get_db_connection
from admin import AdminFrame

class UserFrame(ctk.CTkFrame):
    def __init__(self, master, logout_cb, username):
        super().__init__(master, fg_color="#00798c") # Teal background
        self.logout_cb = logout_cb
        self.username = username
        self.results = []
        self.index = 0
        self.show_budget_selection()

    def show_budget_selection(self):
        for w in self.winfo_children(): w.destroy()
        ctk.CTkLabel(self, text=f"Traveler: {self.username}", font=("Arial", 16), text_color="white").pack(pady=10)
        
        ranges = ["2000-4000", "4000-6000", "6000-8000", "8000-10000"]
        for r in ranges:
            ctk.CTkButton(self, text=f"Rs {r}", fg_color="#30638e", 
                          command=lambda x=r: self.load_places(x)).pack(pady=10)

        ctk.CTkButton(self, text="Reset Password", fg_color="#edae49", text_color="black", command=self.show_reset).pack(pady=5)
        ctk.CTkButton(self, text="Delete Account", fg_color="#d1495b", command=self.delete_acc).pack(pady=5)
        ctk.CTkButton(self, text="Logout", command=self.logout_cb).pack(pady=20)

    def show_reset(self):
        for w in self.winfo_children(): w.destroy()
        new_p = ctk.CTkEntry(self, placeholder_text="New Password", show="*")
        new_p.pack(pady=20)
        def save():
            conn = get_db_connection()
            conn.execute("UPDATE users SET password=? WHERE username=?", (new_p.get(), self.username))
            conn.commit(); conn.close()
            self.show_budget_selection()
        ctk.CTkButton(self, text="Update", command=save).pack()

    def delete_acc(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM users WHERE username=?", (self.username,))
        conn.commit(); conn.close()
        self.logout_cb()

    def load_places(self, budget):
        conn = get_db_connection()
        self.results = conn.execute("SELECT * FROM travel_spots WHERE budget_range=?", (budget,)).fetchall()
        conn.close()
        if self.results: self.show_place_swap()

    def show_place_swap(self):
        for w in self.winfo_children(): w.destroy()
        place = self.results[self.index]
        
        if os.path.exists(place[3]):
            img = ctk.CTkImage(Image.open(place[3]), size=(400, 250))
            ctk.CTkLabel(self, image=img, text=place[2], compound="bottom", font=("Arial", 24, "bold"), text_color="white").pack(pady=20)
        else:
            ctk.CTkLabel(self, text=f"{place[2]} (No Image)", font=("Arial", 20), text_color="white").pack(pady=20)

        ctk.CTkButton(self, text="Next Place ➔", command=self.next_p, fg_color="#30638e").pack(pady=5)
        ctk.CTkButton(self, text="Select This Plan", fg_color="#d1495b", command=lambda: self.show_final(place)).pack(pady=5)

    def next_p(self):
        self.index = (self.index + 1) % len(self.results)
        self.show_place_swap()

    def show_final(self, place):
        for w in self.winfo_children(): w.destroy()
        ctk.CTkLabel(self, text=f"Travel Details for {place[2]}", font=("Arial", 22, "bold"), text_color="white").pack(pady=10)
        
        # Helper to show image + text
        def create_card(title, name, img_path):
            frame = ctk.CTkFrame(self, fg_color="#30638e")
            frame.pack(pady=10, fill="x", padx=20)
            if os.path.exists(img_path):
                img = ctk.CTkImage(Image.open(img_path), size=(100, 70))
                ctk.CTkLabel(frame, image=img, text=f"{title}: {name}", compound="left", padx=10, text_color="white").pack(pady=5)
            else:
                ctk.CTkLabel(frame, text=f"{title}: {name} (Img Missing)", text_color="white").pack(pady=5)

        create_card("Restaurant", place[4], place[5])
        create_card("Hotel", place[6], place[7])
        
        ctk.CTkButton(self, text="Back to Menu", command=self.show_budget_selection, fg_color="#d1495b").pack(pady=20)

class TravelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x750")
        self.title("Travel Mood Explorer")
        init_db()
        self.show_login()

    def show_login(self):
        for w in self.winfo_children(): w.destroy()
        self.configure(fg_color="#30638e") # Login Background
        
        frame = ctk.CTkFrame(self, fg_color="#00798c")
        frame.pack(pady=80, padx=50, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Login", font=("Arial", 30, "bold"), text_color="white").pack(pady=20)
        self.u = ctk.CTkEntry(frame, placeholder_text="Username")
        self.u.pack(pady=10)
        self.p = ctk.CTkEntry(frame, placeholder_text="Password", show="*")
        self.p.pack(pady=10)
        
        ctk.CTkButton(frame, text="Sign In", fg_color="#d1495b", command=self.do_login).pack(pady=10)
        ctk.CTkButton(frame, text="Register", fg_color="transparent", border_width=1, command=self.do_reg).pack()

    def do_login(self):
        # FIX: Save values before destroying the entry boxes
        uname = self.u.get()
        pword = self.p.get()
        
        conn = get_db_connection()
        res = conn.execute("SELECT role FROM users WHERE username=? AND password=?", (uname, pword)).fetchone()
        conn.close()
        
        if res:
            for w in self.winfo_children(): w.destroy()
            if res[0] == 'admin': AdminFrame(self, self.show_login).pack(fill="both", expand=True)
            else: UserFrame(self, self.show_login, uname).pack(fill="both", expand=True)

    def do_reg(self):
        conn = get_db_connection()
        try:
            conn.execute("INSERT INTO users VALUES (?, ?, 'user')", (self.u.get(), self.p.get()))
            conn.commit()
            print("Registered!")
        except: print("Error!")
        conn.close()

if __name__ == "__main__":
    app = TravelApp()
    app.mainloop()
