import os 
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
# import tkinter as tk
# from tkinter import ttk, filedialog, messagebox
from PIL import ImageTk, Image
from steg_crypto import Steganography
import cv2
import numpy as np

class StegApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Secure Image Steganography")
        self.geometry("800x600")
        self.create_widgets()
    
    def create_widgets(self):
        # Notebook for tabs
        tab_control = ttk.Notebook(self)
        
        # Encryption Tab
        enc_tab = ttk.Frame(tab_control)
        self.build_encryption_tab(enc_tab)
        
        # Decryption Tab
        dec_tab = ttk.Frame(tab_control)
        self.build_decryption_tab(dec_tab)
        
        tab_control.add(enc_tab, text='Encryption')
        tab_control.add(dec_tab, text='Decryption')
        tab_control.pack(expand=1, fill='both')
        
    def build_encryption_tab(self, parent):
        # Cover Image Selection
        ttk.Label(parent, text="Cover Image:").grid(row=0, column=0, padx=5, pady=5)
        self.cover_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.cover_path, width=50).grid(row=0, column=1)
        ttk.Button(parent, text="Browse", command=self.select_cover).grid(row=0, column=2)
        
        # Secret Message
        ttk.Label(parent, text="Secret Message:").grid(row=1, column=0)
        self.secret_msg = tk.Text(parent, height=5, width=50)
        self.secret_msg.grid(row=1, column=1, columnspan=2)
        
        # Passcode
        ttk.Label(parent, text="Passcode:").grid(row=2, column=0)
        self.enc_pass = ttk.Entry(parent, show="*")
        self.enc_pass.grid(row=2, column=1)
        
        # Encrypt Button
        ttk.Button(parent, text="Encrypt", command=self.perform_encryption).grid(row=3, column=1)
        
    def build_decryption_tab(self, parent):
        # Encrypted Image Selection
        ttk.Label(parent, text="Encrypted Image:").grid(row=0, column=0)
        self.encrypted_path = tk.StringVar()
        ttk.Entry(parent, textvariable=self.encrypted_path, width=50).grid(row=0, column=1)
        ttk.Button(parent, text="Browse", command=self.select_encrypted).grid(row=0, column=2)
        
        # Passcode
        ttk.Label(parent, text="Passcode:").grid(row=1, column=0)
        self.dec_pass = ttk.Entry(parent, show="*")
        self.dec_pass.grid(row=1, column=1)
        
        # Decrypt Button
        ttk.Button(parent, text="Decrypt", command=self.perform_decryption).grid(row=2, column=1)
        
        # Result Display
        ttk.Label(parent, text="Decrypted Message:").grid(row=3, column=0)
        self.decrypted_msg = tk.Text(parent, height=5, width=50)
        self.decrypted_msg.grid(row=3, column=1)
    
    def select_cover(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.bmp")])
        if path:
            self.cover_path.set(path)
    
    def select_encrypted(self):
        path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
        if path:
            self.encrypted_path.set(path)
    
    def perform_encryption(self):
        try:
            img = cv2.imread(self.cover_path.get())
            if img is None:
                raise ValueError("Invalid cover image")
            
            message = self.secret_msg.get("1.0", tk.END).strip()
            password = self.enc_pass.get()
            
            if not message or not password:
                raise ValueError("Message and password required")
            
            encrypted_img = Steganography.encrypt_message(
                self.cover_path.get(), message, password
            )
            
            save_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                filetypes=[("PNG Files", "*.png")]
            )
            if save_path:
                cv2.imwrite(save_path, encrypted_img)
                messagebox.showinfo("Success", "Image encrypted successfully!")
        
        except Exception as e:
            messagebox.showerror("Error", str(e))
    #Final Touch
    def perform_decryption(self):
        try:
            path = self.encrypted_path.get()
            if not os.path.exists(path):
                raise ValueError("File does not exist")

            img = cv2.imread(path)
            if img is None:
                raise ValueError("Invalid image: Use PNG format")

            password = self.dec_pass.get()
            if not password:
                raise ValueError("Passcode required")

            decrypted = Steganography.decrypt_message(img, password)
            self.decrypted_msg.delete("1.0", tk.END)
            self.decrypted_msg.insert(tk.END, decrypted)
    
        except Exception as e:
            messagebox.showerror("Decryption Failed", 
                f"Error: {str(e)}\n\nPossible causes:\n"
                "1. Wrong passcode\n"
                "2. Image is not encrypted\n"
                "3. File corrupted or not PNG format")



    # def perform_decryption(self):
    #     try:
    #         path = self.encrypted_path.get()

    #         # Validate path exists
    #         if not os.path.exists(path):
    #             raise ValueError(f"File not found: {path}")

    #         # Read image with OpenCV
    #         img = cv2.imread(path)
    #         if img is None:
    #             raise ValueError("Failed to read image. Ensure:\n"
    #                               "1. It's a PNG file\n"
    #                               "2. Full path is correct\n"
    #                               "3. File isn't corrupted")
        
    #     # Rest of the decryption code...
    #         img = cv2.imread(path)
    #         if img is None:
    #             # Check if OpenCV supports the file format
    #             with open(path, 'rb') as f:
    #                 header = f.read(8)
    #                 if header != b'\x89PNG\r\n\x1a\n':
    #                     raise ValueError("File is not a valid PNG")

    #             raise ValueError("Failed to read image (corrupted or invalid)")

    #         # Rest of the decryption code...

    #     except Exception as e:
    #         messagebox.showerror("Error", str(e))



    # def perform_decryption(self):
    #     try:
    #         path = self.encrypted_path.get()
    #         print(f"Debug: Attempting to read {path}")  # Debug line

    #         if not os.path.exists(path):
    #             raise ValueError("File does not exist")

    #         img = cv2.imread(path)
    #         if img is None:
    #             # Check if OpenCV supports the file format
    #             with open(path, 'rb') as f:
    #                 header = f.read(8)
    #                 if header != b'\x89PNG\r\n\x1a\n':
    #                     raise ValueError("File is not a valid PNG")

    #             raise ValueError("Failed to read image (corrupted or invalid)")
        
    #     # Rest of the decryption code...
        
    #     # try:
    #     #     img = cv2.imread(self.encrypted_path.get())
    #     #     if img is None:
    #     #         raise ValueError("Invalid encrypted image")
            
    #         password = self.dec_pass.get()
    #         if not password:
    #             raise ValueError("Password required")
            
    #         decrypted = Steganography.decrypt_message(img, password)
    #         self.decrypted_msg.delete("1.0", tk.END)
    #         self.decrypted_msg.insert(tk.END, decrypted)
        
        # except Exception as e:
        #     messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    app = StegApp()
    app.mainloop()