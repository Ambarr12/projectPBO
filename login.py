import tkinter as tk
from tkinter import messagebox
from home import PsychologyServiceApp

def login():
    username = entry_name.get()
    password = entry_password.get()

    if username and password:  
        messagebox.showinfo("Login Sukses", f"Selamat datang, {username}!")
        root.destroy()  
        open_main_app() 
    else:
        messagebox.showwarning("Login Gagal", "Nama dan Password harus diisi!")

def open_main_app():
    main_root = tk.Tk()
    PsychologyServiceApp(main_root)
    main_root.mainloop()

root = tk.Tk()
root.title("Login - Layanan Psikolog")
root.geometry("400x300")
root.configure(bg="#D4F1F4")

login_frame = tk.Frame(root, bg="#D4F1F4")
login_frame.pack(expand=True)

welcome_text = "Selamat Datang di Layanan Psikolog, Silahkan Login Terlebih Dahulu           "
running_text = tk.StringVar(value=welcome_text)
welcome_label = tk.Label(login_frame, textvariable=running_text, font=("Arial", 16), bg="#D4F1F4", fg="black")
welcome_label.pack(pady=(10, 0))

def animate_text():
    """Animasi teks berjalan"""
    current_text = running_text.get()
    running_text.set(current_text[1:] + current_text[0])
    root.after(200, animate_text)

animate_text()

label_name = tk.Label(login_frame, text="Username", font=("Arial", 14), bg="#D4F1F4", fg="black")
label_name.pack(pady=(30, 0))
entry_name = tk.Entry(login_frame, font=("Arial", 14), width=30)
entry_name.pack(pady=5)

label_password = tk.Label(login_frame, text="Password", font=("Arial", 14), bg="#D4F1F4", fg="black")
label_password.pack(pady=(20, 0))
entry_password = tk.Entry(login_frame, font=("Arial", 14), width=30, show="*")
entry_password.pack(pady=5)

button_login = tk.Button(login_frame, text="Login", bg="#4CAF50", fg="white", font=("Arial", 12), command=login)
button_login.pack(pady=20)

root.mainloop()