from tkinter import *
from tkinter import filedialog, messagebox
from window_templates import DialogueWindow
from tab_templates import BlankTab


class RarJpegDec(BlankTab):
    def __init__(self, parent):
        super().__init__(parent)

        self.polyglot_data = None
        self.polyglot_path = ""
        self.archive_data = None
        self.image_data = None

    def execute(self):
        self.draw_tab_w_cls_btn("rarjpeg_dec")

        self.label_polyglot = Label(self.tab_frame, text="Rarjpeg location (.jpeg):")
        self.entry_polyglot = Entry(self.tab_frame, width=50, state="disabled")
        self.btn_polyglot = Button(self.tab_frame, text="Search", command=self.select_polyglot)
        self.label_status = Label(self.tab_frame, text="Status: Select file", fg="blue")
        self.btn_analyze = Button(self.tab_frame, text="Analyze", command=self.analyze_polyglot, state="disabled")
        self.result_frame = LabelFrame(self.tab_frame, text="Analysis results")
        self.label_img = Label(self.result_frame, text="Image (.jpeg):")
        self.info_img = Label(self.result_frame, text="Not found")
        self.save_btn_img = Button(self.result_frame, text="Save", command=self.save_image, state="disabled")
        self.label_archive = Label(self.result_frame, text="Archive (.rar):")
        self.info_archive = Label(self.result_frame, text="Not found")
        self.save_btn_archive = Button(self.result_frame, text="Save", command=self.save_archive, state="disabled")

        self.label_polyglot.place(x=50, y=58)
        self.entry_polyglot.place(x=185, y=60)
        self.btn_polyglot.place(x=505, y=56)
        self.label_status.place(x=185, y=98)
        self.btn_analyze.place(x=310, y=125)
        self.result_frame.place(x=50, y=160)
        self.label_img.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.info_img.grid(row=0, column=1, padx=5, pady=5, sticky='w')
        self.save_btn_img.grid(row=0, column=2, padx=5, pady=5)
        self.label_archive.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.info_archive.grid(row=1, column=1, padx=5, pady=5, sticky='w')
        self.save_btn_archive.grid(row=1, column=2, padx=5, pady=5)

        self.riddle_window.root.destroy()

    def select_polyglot(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    self.polyglot_data = file.read()

                self.polyglot_path = file_path
                self.entry_polyglot.configure(state="normal")
                self.entry_polyglot.delete(0, "end")
                self.entry_polyglot.insert(0, file_path)
                self.entry_polyglot.configure(state="disabled")
                self.btn_analyze.config(state="normal")
                self.label_status.config(text="Status: File uploaded. Analyze it", fg="orange")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    def analyze_polyglot(self):
        try:
            jpeg_end_marker = b'\xff\xd9'
            jpeg_end_pos = self.polyglot_data.find(jpeg_end_marker)

            if jpeg_end_pos == -1:
                messagebox.showerror("Error", "No valid JPEG!")
                return

            self.image_data = self.polyglot_data[:jpeg_end_pos + 2]

            if not self.image_data.startswith(b'\xff\xd8'):
                messagebox.showerror("Error", "Detected JPEG data is corrupted!")
                self.image_data = None
                return

            self.archive_data = self.polyglot_data[jpeg_end_pos + 2:]

            if not self.archive_data.startswith(b'Rar!'):
                messagebox.showerror("Error", "RAR archive is not found!")
                self.archive_data = None
                return

            self.info_img.config(text=f"Found", fg="green")
            self.info_archive.config(text=f"Found", fg="green")

            self.save_btn_img.config(state="normal")
            self.save_btn_archive.config(state="normal")

            self.label_status.config(text="Status: File successfully analyzed", fg="green")

        except Exception as e:
            messagebox.showerror("Error", f"Failed analyzing file: {str(e)}")

    def save_image(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, 'wb') as file:
                file.write(self.image_data)

            messagebox.showinfo("Success", f"Image created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed image creation: {str(e)}")

    def save_archive(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".rar",
            filetypes=[("RAR files", "*.rar"), ("All files", "*.*")]
        )

        if not file_path:
            return

        try:
            with open(file_path, 'wb') as file:
                file.write(self.archive_data)

            messagebox.showinfo("Success", f"Archive created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed archive creation: {str(e)}")

    def rerun(self):
        self.polyglot_data = None
        self.polyglot_path = ""
        self.archive_data = None
        self.image_data = None

        self.entry_polyglot.configure(state="normal")
        self.entry_polyglot.delete(0, "end")
        self.entry_polyglot.configure(state="disabled")

        self.label_status.config(text="Status: Select file", fg="blue")
        self.btn_analyze.config(state="disabled")
        self.info_img.config(text="Not found", fg="black")
        self.info_archive.config(text="Not found", fg="black")
        self.save_btn_img.config(state="disabled")
        self.save_btn_archive.config(state="disabled")

    def undo(self):
        if self.archive_data is not None:
            self.archive_data = None
            self.image_data = None

            self.label_status.config(text="Status: File uploaded. Analyze it", fg="orange")
            self.info_img.config(text="Not found", fg="black")
            self.info_archive.config(text="Not found", fg="black")
            self.save_btn_img.config(state="disabled")
            self.save_btn_archive.config(state="disabled")

        elif self.btn_analyze['state'] == "normal":
            self.rerun()


class DecodeStegoWindow(DialogueWindow):
    CONCEALMENT_TYPES = [
        (RarJpegDec, "Rar+Jpeg"),
    ]

    def __init__(self, parent):
        super().__init__(parent, "Decode Dialogue")
