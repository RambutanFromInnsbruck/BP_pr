from tkinter import *
from tkinter import filedialog, messagebox
import os
from window_templates import DialogueWindow
from tab_templates import BlankTab


class RarJpegEnc(BlankTab):
    def __init__(self, parent):
        super().__init__(parent)

        self.archive_data = None
        self.image_data = None
        self.archive_name = ""
        self.image_name = ""
        self.action_stack = []

    def execute(self):
        self.draw_tab_w_cls_btn("rarjpeg_enc")

        self.label_archive = Label(self.tab_frame, text="Archive location (.rar):")
        self.entry_archive = Entry(self.tab_frame, width=50, state="disabled")
        self.btn_archive = Button(self.tab_frame, text="Search", command=self.select_archive)
        self.label_img = Label(self.tab_frame, text="Image location (.jpeg):")
        self.entry_img = Entry(self.tab_frame, width=50, state="disabled")
        self.btn_img = Button(self.tab_frame, text="Search", command=self.select_image)
        self.label_status = Label(self.tab_frame, text="Status: Select files", fg="blue")
        self.btn_create = Button(self.tab_frame, text="Create", command=self.create_polyglot, state="disabled")

        self.label_archive.place(x=50, y=58)
        self.entry_archive.place(x=185, y=60)
        self.btn_archive.place(x=505, y=56)
        self.label_img.place(x=50, y=98)
        self.entry_img.place(x=185, y=100)
        self.btn_img.place(x=505, y=96)
        self.label_status.place(x=185, y=140)
        self.btn_create.place(x=310, y=170)

        self.riddle_window.root.destroy()

    def select_archive(self):
        file_path = filedialog.askopenfilename(
        filetypes=[("RAR files", "*.rar")]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    data = file.read()

                if not data.startswith(b'Rar!'):
                    messagebox.showerror("Error", "The selected file is not a RAR archive!")
                    return

                self.archive_data = data
                self.archive_name = os.path.basename(file_path)
                self.entry_archive.configure(state="normal")
                self.entry_archive.delete(0, "end")
                self.entry_archive.insert(0, file_path)
                self.entry_archive.configure(state="disabled")

                if "archive" in self.action_stack:
                    self.action_stack.remove("archive")

                self.action_stack.append("archive")
                self.update_status()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    def select_image(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("JPEG files", "*.jpg *.jpeg")]
        )

        if file_path:
            try:
                with open(file_path, 'rb') as file:
                    data = file.read()

                if not data.startswith(b'\xff\xd8'):
                    messagebox.showerror("Error", "The selected file is not JPEG image!")
                    return

                self.image_data = data
                self.image_name = os.path.basename(file_path)
                self.entry_img.configure(state="normal")
                self.entry_img.delete(0, "end")
                self.entry_img.insert(0, file_path)
                self.entry_img.configure(state="disabled")

                if "image" in self.action_stack:
                    self.action_stack.remove("image")

                self.action_stack.append("image")
                self.update_status()

            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")

    def update_status(self):
        archive_loaded = self.archive_data is not None
        image_loaded = self.image_data is not None

        if archive_loaded and image_loaded:
            self.label_status.config(text="Status: Both files loaded into memory. Ready to create", fg="green")
            self.btn_create.config(state="normal")
        elif archive_loaded:
            self.label_status.config(text="Status: Archive uploaded. Select an image", fg="orange")
            self.btn_create.config(state="disabled")
        elif image_loaded:
            self.label_status.config(text="Status: Image uploaded. Select an archive", fg="orange")
            self.btn_create.config(state="disabled")
        else:
            self.label_status.config(text="Status: Select files", fg="blue")
            self.btn_create.config(state="disabled")

    def create_polyglot(self):
        output_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG files", "*.jpg"), ("All files", "*.*")]
        )

        if not output_path:
            return

        try:
            with open(output_path, 'wb') as out_file:
                out_file.write(self.image_data)
                out_file.write(self.archive_data)

            messagebox.showinfo("Success", "File created successfully!")

        except Exception as e:
            messagebox.showerror("Error", f"Failed file creation: {str(e)}")

    def rerun(self):
        self.archive_data = None
        self.image_data = None
        self.archive_name = ""
        self.image_name = ""

        self.entry_archive.configure(state="normal")
        self.entry_archive.delete(0, "end")
        self.entry_archive.configure(state="disabled")

        self.entry_img.configure(state="normal")
        self.entry_img.delete(0, "end")
        self.entry_img.configure(state="disabled")

        self.update_status()

    def undo(self):
        if not self.action_stack:
            return

        last_action = self.action_stack.pop()

        if last_action == "archive" and self.archive_data is not None:
            self.archive_data = None
            self.archive_name = ""
            self.entry_archive.configure(state="normal")
            self.entry_archive.delete(0, "end")
            self.entry_archive.configure(state="disabled")

        elif last_action == "image" and self.image_data is not None:
            self.image_data = None
            self.image_name = ""
            self.entry_img.configure(state="normal")
            self.entry_img.delete(0, "end")
            self.entry_img.configure(state="disabled")

        self.update_status()


class EncodeStegoWindow(DialogueWindow):
    CONCEALMENT_TYPES = [
        (RarJpegEnc, "Rar+Jpeg"),
    ]

    def __init__(self, parent):
        super().__init__(parent, "Encode Dialogue")
