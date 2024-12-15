import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
from db import Database


class PsychologyServiceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Layanan Psikolog")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        self.db = Database()

        self.patients_data = []

        self.sidebar_frame = tk.Frame(self.root, bg="#000000", width=250)
        self.sidebar_frame.pack(side=tk.LEFT, fill=tk.Y, expand=False)

        self.create_sidebar()

        self.main_frame = tk.Frame(self.root, bg="#FFFFFF")
        self.main_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.create_dashboard()

        self.root.bind("<Configure>", self.resize_sidebar)

    def create_sidebar(self):
        """Membuat sidebar menu"""
        menu_items = [
            ("🏠 Dashboard", self.show_dashboard),
            ("Data", None),
            ("  🩺 Pasien", self.show_patient),
            ("  🧠 Layanan", self.show_service),
            ("Catatan Terapi", None),
            ("  📄 Psikologi Klinis", self.show_clinical_psychology),
            ("  📄 Psikologi Pendidikan", self.show_educational_psychology),
            ("  📄 Konseling Karir", self.show_career_counseling),
            ("  📄 Psikoterapi", self.show_psychotherapy),
            ("  📄 Psikologi Forensik", self.show_forensic_psychology),
            ("  📄 Psikologi Anak & Remaja", self.show_child_psychology),
        ]

        tk.Label(
            self.sidebar_frame,
            text="Layanan Psikolog",
            bg="#000000",
            fg="#FFFFFF",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        for menu, command in menu_items:
            label = tk.Label(
            self.sidebar_frame,
            text=menu,
            bg="#000000",
            fg="#FFFFFF",
            font=("Arial", 12),
            anchor="w",
            padx=10,
        )
            label.pack(fill=tk.X, pady=5)

            if command:
                label.bind("<Button-1>", lambda event, cmd=command: cmd())

            label.bind("<Enter>", lambda event, lbl=label: lbl.config(fg="#FFD700"))
            label.bind("<Leave>", lambda event, lbl=label: lbl.config(fg="#FFFFFF"))
    
    def create_dashboard(self):
        """Membuat konten Dashboard"""
        self.clear_main_content()

        animation_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        animation_frame.pack(fill=tk.X, pady=30)

        self.running_text = "Selamat Datang di Layanan Psikologi Kami        "
        self.running_text_label = tk.Label(animation_frame, text="", font=("Arial", 16, "bold"), bg="#FFFFFF", fg="#000000")
        self.running_text_label.pack()

        self.animate_text()

        image_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        image_frame.pack(pady=10)

        try:
            image = Image.open("img.jpg") 
            image = image.resize((600, 600))
            self.photo = ImageTk.PhotoImage(image)

            img_label = tk.Label(image_frame, image=self.photo, bg="#FFFFFF")
            img_label.pack()
        except Exception as e:
            tk.Label(image_frame, text="Gagal memuat gambar.", bg="#FFFFFF", fg="#FF0000", font=("Arial", 12)).pack()

        content_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(content_frame, text="Kesehatan Mental Anda Prioritas Kami",
                bg="#FFFFFF", fg="#000000", font=("Arial", 14)).pack()

    def animate_text(self):
        """Animasi teks berjalan"""
        current_text = self.running_text

        self.running_text = current_text[1:] + current_text[0]

        self.running_text_label.config(text=self.running_text)

        self.root.after(200, self.animate_text)

    def save_patient_to_db(self, patient_data):
        query = """
        INSERT INTO patients (name, dob, age, gender, phone, address, complaint)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        try:
            db_manager = Database()
            db_manager.execute_query(query, patient_data)
            messagebox.showinfo("Info", "Pasien berhasil disimpan ke database.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menyimpan data pasien: {e}")

    def add_patient(self):
        """Fungsi untuk menambah pasien baru (menggunakan dialog form input)"""
        form_window = tk.Toplevel(self.root)
        form_window.title("Tambah Pasien Baru")
        form_window.geometry("400x300")
        form_window.resizable(False, False)

        form_frame = tk.Frame(form_window, padx=10, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        def create_form_row_with_placeholder(parent, label_text, placeholder):
            row_frame = tk.Frame(parent)
            row_frame.pack(fill=tk.X, pady=5)

            label = tk.Label(row_frame, text=label_text, width=15, anchor="w")
            label.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(row_frame, width=25, fg="gray")
            entry.insert(0, placeholder)

            def on_focus_in(event):
                if entry.get() == placeholder:
                    entry.delete(0, tk.END)
                    entry.config(fg="black")

            def on_focus_out(event):
                if not entry.get():
                    entry.insert(0, placeholder)
                    entry.config(fg="gray")
            
            entry.bind("<FocusIn>", on_focus_in)
            entry.bind("<FocusOut>", on_focus_out)
            entry.pack(side=tk.LEFT, padx=5)
            return entry

        name_entry = create_form_row_with_placeholder(form_frame, "Nama:", "Contoh: John Doe")
        dob_entry = create_form_row_with_placeholder(form_frame, "Tanggal Lahir:", "YYYY-MM-DD")
        age_entry = create_form_row_with_placeholder(form_frame, "Umur:", "Contoh: 30")
        gender_entry = create_form_row_with_placeholder(form_frame, "Jenis Kelamin:", "Contoh: L/P")
        phone_entry = create_form_row_with_placeholder(form_frame, "Telepon:", "Contoh: 08123456789")
        address_entry = create_form_row_with_placeholder(form_frame, "Alamat:", "Contoh: Jl. Mawar No.1")
        complaint_entry = create_form_row_with_placeholder(form_frame, "Keluhan:", "Contoh: Halusinasi")

        def save_patient():
            """Menyimpan data pasien baru dan menambahkan ke tabel"""
            name = name_entry.get()
            dob = dob_entry.get()
            age = int(age_entry.get())
            gender = gender_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            complaint = complaint_entry.get()

            if not all([name, dob, age, gender, phone, complaint]):
                messagebox.showwarning("Peringatan", "Semua field wajib diisi!")
                return

            patient_data = (name, dob, age, gender, phone, address, complaint)

            self.save_patient_to_db(patient_data)
            form_window.destroy()
            self.update_patient_table_from_db()

        save_button = tk.Button(form_frame, text="Simpan", command=save_patient, bg="green", fg="white", padx=10, pady=5)
        save_button.pack(pady=10)
        
    def update_patient_table_from_db(self):
        """Update tabel dengan data dari database."""
        query = "SELECT * FROM patients"
        db = Database()
        data = db.fetch_query(query)

        if data:
            for row in self.table.get_children():
                self.table.delete(row)

            for row in data:
                self.table.insert("", "end", values=(
                    row["id"], row["name"], row["dob"], row["age"], 
                    row["gender"], row["phone"], row["address"], row["complaint"]
                ))
        else:
            messagebox.showinfo("Info", "Tidak ada data pasien ditemukan.")

    def delete_patient(self):
        """Menghapus pasien yang dipilih dari tabel dan database."""
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih pasien yang ingin dihapus.")
            return

        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data pasien ini?")
        if not confirm:
            return

        try:
            patient_id = self.table.item(selected_item[0])["values"][0]

            query = "DELETE FROM patients WHERE id = %s"
            db = Database()
            db.execute_query(query, (patient_id,))

            self.table.delete(selected_item[0])

            messagebox.showinfo("Info", "Pasien berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menghapus pasien: {e}")

    def edit_patient(self):
        """Mengedit data pasien yang dipilih dari tabel"""
        selected_item = self.table.selection()

        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih pasien yang ingin diedit.")
            return

        # Ambil data pasien dari baris yang dipilih
        patient_data = self.table.item(selected_item[0])["values"]

        # Buka formulir untuk mengedit pasien
        form_window = tk.Toplevel(self.root)
        form_window.title("Edit Pasien")
        form_window.geometry("400x400")
        form_window.resizable(False, False)

        form_frame = tk.Frame(form_window, padx=10, pady=10)
        form_frame.pack(fill=tk.BOTH, expand=True)

        # Buat field input dengan data awal
        name_entry = self.create_form_row(form_frame, "Nama:", patient_data[1])
        dob_entry = self.create_form_row(form_frame, "Tanggal Lahir:", patient_data[2])
        age_entry = self.create_form_row(form_frame, "Umur:", patient_data[3])
        gender_entry = self.create_form_row(form_frame, "Jenis Kelamin:", patient_data[4])
        phone_entry = self.create_form_row(form_frame, "Telepon:", patient_data[5])
        address_entry = self.create_form_row(form_frame, "Alamat:", patient_data[6])
        complaint_entry = self.create_form_row(form_frame, "Keluhan:", patient_data[7])

        def update_patient():
            """Simpan perubahan ke database dan perbarui tabel"""
            updated_data = (
                name_entry.get(),
                dob_entry.get(),
                int(age_entry.get()),
                gender_entry.get(),
                phone_entry.get(),
                address_entry.get(),
                complaint_entry.get(),
                patient_data[0],  
            )

            try:
                query = """
                UPDATE patients 
                SET name = %s, dob = %s, age = %s, gender = %s, phone = %s, address = %s, complaint = %s 
                WHERE id = %s
                """
                db = Database()
                db.execute_query(query, updated_data)
                messagebox.showinfo("Info", "Data pasien berhasil diperbarui.")
                self.update_patient_table_from_db()
                form_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Gagal memperbarui data pasien: {e}")

        save_button = tk.Button(
            form_frame, 
            text="Simpan Perubahan", 
            command=update_patient, 
            bg="green", 
            fg="white", 
            padx=10, 
            pady=5
        )
        save_button.pack(pady=10)

    def create_form_row(self, parent, label_text, initial_value):
        row_frame = tk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=5)

        label = tk.Label(row_frame, text=label_text, width=15, anchor="w")
        label.pack(side=tk.LEFT, padx=5)

        entry = tk.Entry(row_frame, width=25)
        entry.insert(0, initial_value)
        entry.pack(side=tk.LEFT, padx=5)

        return entry

    def show_dashboard(self):
        """Tampilkan konten Dashboard"""
        self.create_dashboard() 
    
    def clear_main_content(self):
        """Clear current content in the main frame"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def resize_sidebar(self, event):
        """Fungsi untuk mengatur ulang sidebar agar tetap proporsional saat ukuran layar berubah"""
        new_width = event.width // 5  
        if new_width > 600:
            new_width = 600
        elif new_width < 250:
            new_width = 250
        self.sidebar_frame.config(width=new_width)

    def show_patient(self):
        self.clear_main_content()

        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Label(header_frame, text="Data Pasien", bg="#FFFFFF", fg="#000000", font=("Arial", 16, "bold")).pack(side=tk.LEFT)
        tk.Button(header_frame, text="+ Pasien Baru", bg="#FFFFFF", fg="#000000", font=("Arial", 12), relief="solid", command=self.add_patient).pack(side=tk.RIGHT)

        table_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.table = ttk.Treeview(
            table_frame,
            columns=("ID", "Nama", "Tanggal Lahir", "Umur", "Jenis Kelamin", "Telepon", "Alamat", "Keluhan"),
            show="headings",
            height=15
        )
        self.table.heading("ID", text="ID")
        self.table.heading("Nama", text="Nama")
        self.table.heading("Tanggal Lahir", text="Tanggal Lahir")
        self.table.heading("Umur", text="Umur")
        self.table.heading("Jenis Kelamin", text="Jenis Kelamin")
        self.table.heading("Telepon", text="Telepon")
        self.table.heading("Alamat", text="Alamat")
        self.table.heading("Keluhan", text="Keluhan")

        for col in ("ID", "Nama", "Tanggal Lahir", "Umur", "Jenis Kelamin", "Telepon", "Alamat", "Keluhan"):
            self.table.column(col, anchor="center", width=100)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.configure(yscrollcommand=scrollbar.set)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        delete_button = tk.Button(button_frame, text="Hapus Pasien", command=self.delete_patient, bg="red", fg="white", font=("Arial", 12), padx=10, pady=5)
        delete_button.pack(side=tk.LEFT, padx=10)

        edit_button = tk.Button(button_frame, text="Edit Pasien", command=self.edit_patient, bg="green", fg="white", font=("Arial", 12), padx=10, pady=5)
        edit_button.pack(side=tk.LEFT, padx=10)

        refresh_button = tk.Button(button_frame, text="Refresh Data", command=self.update_patient_table_from_db, bg="blue", fg="white", font=("Arial", 12), padx=10, pady=5)
        refresh_button.pack(side=tk.LEFT)

        self.update_patient_table_from_db()

    def show_service(self):
        self.clear_main_content()

        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Label(header_frame, text="Layanan Pasien", bg="#FFFFFF", fg="#000000", font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        input_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        input_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Label(input_frame, text="Masukkan ID Pasien :", bg="#FFFFFF", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)

        self.service_input = tk.Entry(input_frame, font=("Arial", 12))
        self.service_input.pack(side=tk.LEFT, padx=5)

        search_button = tk.Button(input_frame, text="Cari", command=self.search_service, bg="green", fg="white", font=("Arial", 12), padx=10)
        search_button.pack(side=tk.LEFT, padx=5)

        output_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        output_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.service_table = ttk.Treeview(
            output_frame,
            columns=("ID", "Nama", "Keluhan", "Layanan"),
            show="headings",
            height=10
        )
        self.service_table.heading("ID", text="ID")
        self.service_table.heading("Nama", text="Nama")
        self.service_table.heading("Keluhan", text="Keluhan")
        self.service_table.heading("Layanan", text="Layanan")

        for col in ("ID", "Nama", "Keluhan", "Layanan"):
            self.service_table.column(col, anchor="center", width=200)

        self.service_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(output_frame, orient="vertical", command=self.service_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.service_table.configure(yscrollcommand=scrollbar.set)

    def determine_service(self, complaint):
        """Menentukan layanan berdasarkan keluhan pasien"""
        layanan_map = {
            "Psikologi Klinis": ["stres", "bunuh diri", "trauma", "gangguan bipolar", "insomnia"],
            "Psikologi Pendidikan": ["gangguan belajar", "gangguan perkembangan", "masalah motivasi", "gangguan sosial"],
            "Psikologi Forensik": ["halusinasi", "kekerasan", "narsistik"],
            "Psikologi Anak & Remaja": ["depresi", "gangguan kecemasan", "speech delay"],
            "Psikoterapi": ["gangguan mood", "panic attack", "kehilangan dan duka cita", "fobia"],
            "Konseling Karir": ["social anxiety", "pascatrauma", "kecanduan", "agresif"],
        }

        for layanan, keywords in layanan_map.items():
            if any(keyword.lower() in complaint.lower() for keyword in keywords):
                return layanan
        return "Tidak ditemukan layanan yang sesuai"

    def search_service(self):
        """
        Fetch data based on input (ID Pasien) and display the corresponding keluhan and layanan.
        """
        search_input = self.service_input.get().strip() 

        if not search_input:
            messagebox.showwarning("Peringatan", "Masukkan ID Pasien")
            return

        patient_data = self.get_patient_data(search_input)

        if not patient_data:
            messagebox.showinfo("Info", "Pasien tidak ditemukan.")
            return

        for row in self.service_table.get_children():
            self.service_table.delete(row)

        self.service_table.insert("", "end", values=(patient_data["id"], patient_data["nama"], patient_data["keluhan"], patient_data["layanan"]))

    def get_patient_data(self, show_patient):
        """
        Retrieve patient data from the database based on ID or Name.
        """
        try:
            query = """
            SELECT id, name, complaint 
            FROM patients 
            WHERE id LIKE %s OR LOWER(name) LIKE %s
            """
            search_query = f"%{show_patient}%".lower() 
            db = Database()
            result = db.fetch_query(query, (search_query, search_query))
            
            if result:
                patient = result[0]
                layanan = self.determine_service(patient["complaint"])

                return {
                    "id": patient["id"],
                    "nama": patient["name"],
                    "keluhan": patient["complaint"],
                    "layanan": layanan 
                }
            else:
                print("Tidak ditemukan data pasien dengan ID:", show_patient) 
                return None
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data pasien: {e}")
            return None

    def show_clinical_psychology(self):
        self.show_patients_by_service("Psikologi Klinis")

    def show_educational_psychology(self):
        self.show_patients_by_service("Psikologi Pendidikan")

    def show_career_counseling(self):
        self.show_patients_by_service("Konseling Karir")

    def show_psychotherapy(self):
        self.show_patients_by_service("Psikoterapi")

    def show_forensic_psychology(self):
        self.show_patients_by_service("Psikologi Forensik")

    def show_child_psychology(self):
        self.show_patients_by_service("Psikologi Anak & Remaja")

    def show_patients_by_service(self, service):
        """Menampilkan tabel pasien berdasarkan layanan tertentu."""
        self.clear_main_content()  

        header_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        header_frame.pack(fill=tk.X, pady=10, padx=20)

        tk.Label(header_frame, text=f"Data Pasien - {service}", bg="#FFFFFF", fg="#000000", font=("Arial", 16, "bold")).pack(side=tk.LEFT)

        table_frame = tk.Frame(self.main_frame, bg="#FFFFFF")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.service_table = ttk.Treeview(
            table_frame,
            columns=("ID", "Nama", "Tanggal Lahir" , "Umur" ,"Jenis Kelamin","Telepon", "Alamat", "Keluhan"),
            show="headings",
            height=15
        )

        for col in ("ID", "Nama", "Tanggal Lahir", "Umur", "Jenis Kelamin", "Telepon", "Alamat", "Keluhan"):
            self.service_table.heading(col, text=col)
            self.service_table.column(col, anchor="center", width=100)

        self.service_table.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.service_table.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.service_table.configure(yscrollcommand=scrollbar.set)

        patients = self.get_all_patients_by_service(service)
        if patients:
            for patient in patients:
                self.service_table.insert("", "end", values=(
                    patient["id"], patient["name"], patient["dob"],
                    patient["age"], patient["gender"],
                    patient["phone"], patient["address"], patient["complaint"]
                ))
        else:
            messagebox.showinfo(service, "Tidak ada pasien dalam kategori ini.")

    def get_all_patients_by_service(self, service):
        """Mengambil semua pasien berdasarkan layanan tertentu."""
        try:
            query = """
            SELECT id, name, dob, age, gender, phone, address, complaint 
            FROM patients
            """
            db = Database()
            result = db.fetch_query(query)

            filtered_patients = []
            for patient in result:
                if self.determine_service(patient["complaint"]) == service:
                    filtered_patients.append({
                        "id": patient["id"],
                        "name": patient["name"],
                        "dob": patient["dob"],
                        "age": patient["age"],
                        "gender": patient["gender"],
                        "phone": patient["phone"],
                        "address": patient["address"],
                        "complaint": patient["complaint"]
                    })
            return filtered_patients
        except Exception as e:
            messagebox.showerror("Error", f"Gagal mengambil data pasien: {e}")
            return []
    


if __name__ == "__main__":
    root = tk.Tk()
    app = PsychologyServiceApp(root)
    root.mainloop()