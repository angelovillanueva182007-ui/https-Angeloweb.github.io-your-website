from tkinter import *
from tkinter import messagebox

root = Tk()
root.title("Login | Register")
root.geometry("500x450")
root.config(bg="#1e1e2f")  # main dark background

# ---------- FILE SYSTEM ----------
def save_user(username, password):
    with open("users.txt", "a") as file:
        file.write(username + "," + password + "\n")

def check_user(username, password):
    try:
        with open("users.txt", "r") as file:
            for line in file:
                u, p = line.strip().split(",")
                if u == username and p == password:
                    return True
    except:
        return False
    return False

# ---------- REGISTER ----------
def open_register():
    reg = Toplevel(root)
    reg.title("Register")
    reg.geometry("400x350")
    reg.config(bg="#25253a")

    Label(reg, text="Create Account",
          font=("Arial", 20, "bold"),
          bg="#25253a", fg="#ffffff").pack(pady=15)

    Label(reg, text="Username", bg="#25253a", fg="#cfcfe6").pack()
    reg_user = Entry(reg, font=("Arial", 12), bg="#2f2f47", fg="white", insertbackground="white")
    reg_user.pack(pady=5)

    Label(reg, text="Password", bg="#25253a", fg="#cfcfe6").pack()
    reg_pass = Entry(reg, show="*", font=("Arial", 12),
                     bg="#2f2f47", fg="white", insertbackground="white")
    reg_pass.pack(pady=5)

    def register():
        if reg_user.get() == "" or reg_pass.get() == "":
            messagebox.showerror("Error", "Fill all fields")
        else:
            save_user(reg_user.get(), reg_pass.get())
            messagebox.showinfo("Success", "Registered!")
            reg.destroy()

    Button(reg, text="Register",
           bg="#6c63ff", fg="white",
           activebackground="#5750d6",
           font=("Arial", 12, "bold"),
           width=15, command=register).pack(pady=15)

# ---------- PROFILE ----------
def open_profile(username):
    profile = Toplevel(root)
    profile.title("Profile")
    profile.geometry("400x350")
    profile.config(bg="#25253a")

    Label(profile, text="User Profile",
          font=("Arial", 20, "bold"),
          bg="#25253a", fg="white").pack(pady=20)

    Label(profile, text=f"Welcome, {username}",
          font=("Arial", 16),
          bg="#25253a", fg="#6c63ff").pack(pady=10)

    def logout():
        profile.destroy()
        root.deiconify()

    Button(profile, text="Logout",
           bg="#ff5c5c", fg="white",
           activebackground="#e14b4b",
           font=("Arial", 12, "bold"),
           width=12, command=logout).pack(pady=30)

# ---------- LOGIN ----------
def login():
    username = user_entry.get()
    password = password_entry.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "Invalid input")
    elif check_user(username, password):
        messagebox.showinfo("Success", "Login Successful")
        root.withdraw()
        open_profile(username)
    else:
        messagebox.showerror("Error", "Wrong credentials")

# ---------- UI ----------
Label(root, text="Login System",
      font=("Arial", 24, "bold"),
      bg="#1e1e2f", fg="#ffffff").pack(pady=30)

frame = Frame(root, bg="#1e1e2f")
frame.pack()

Label(frame, text="Username",
      bg="#1e1e2f", fg="#cfcfe6").grid(row=0, column=0, pady=10)

user_entry = Entry(frame, font=("Arial", 12),
                   width=20, bg="#2f2f47", fg="white",
                   insertbackground="white")
user_entry.grid(row=0, column=1, pady=10)

Label(frame, text="Password",
      bg="#1e1e2f", fg="#cfcfe6").grid(row=1, column=0, pady=10)

password_entry = Entry(frame, show="*", font=("Arial", 12),
                       width=20, bg="#2f2f47", fg="white",
                       insertbackground="white")
password_entry.grid(row=1, column=1, pady=10)

Button(root, text="Login",
       bg="#6c63ff", fg="white",
       activebackground="#5750d6",
       font=("Arial", 12, "bold"),
       width=15, command=login).pack(pady=15)

Button(root, text="Register",
       bg="#2f2f47", fg="white",
       activebackground="#3a3a5a",
       font=("Arial", 12, "bold"),
       width=15, command=open_register).pack()

root.mainloop()