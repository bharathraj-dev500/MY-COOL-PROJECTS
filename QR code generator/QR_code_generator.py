import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
from PIL import Image, ImageTk
import os
import webbrowser

class QRCodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Generator")
        self.root.geometry("600x700")
        self.root.resizable(False, False)
        
        # Variables
        self.qr_data = tk.StringVar()
        self.fill_color = tk.StringVar(value="#000000")
        self.back_color = tk.StringVar(value="#FFFFFF")
        self.qr_size = tk.IntVar(value=10)
        self.border_size = tk.IntVar(value=4)
        self.error_correction = tk.StringVar(value="M")
        self.file_path = tk.StringVar()
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="QR Code Content", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Enter text/URL:").grid(row=0, column=0, sticky=tk.W)
        self.entry = ttk.Entry(input_frame, textvariable=self.qr_data, width=50)
        self.entry.grid(row=1, column=0, columnspan=2, pady=5, sticky=tk.EW)
        self.entry.focus()
        
        # Settings section
        settings_frame = ttk.LabelFrame(main_frame, text="QR Code Settings", padding="10")
        settings_frame.pack(fill=tk.X, pady=5)
        
        # Color settings
        ttk.Label(settings_frame, text="Fill Color:").grid(row=0, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.fill_color, width=10).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Button(settings_frame, text="Pick", command=lambda: self.pick_color(self.fill_color)).grid(row=0, column=2, padx=5)
        
        ttk.Label(settings_frame, text="Background Color:").grid(row=1, column=0, sticky=tk.W)
        ttk.Entry(settings_frame, textvariable=self.back_color, width=10).grid(row=1, column=1, sticky=tk.W, padx=5)
        ttk.Button(settings_frame, text="Pick", command=lambda: self.pick_color(self.back_color)).grid(row=1, column=2, padx=5)
        
        # Size settings
        ttk.Label(settings_frame, text="QR Code Size:").grid(row=2, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=1, to=20, variable=self.qr_size, orient=tk.HORIZONTAL).grid(row=2, column=1, columnspan=2, sticky=tk.EW)
        
        ttk.Label(settings_frame, text="Border Size:").grid(row=3, column=0, sticky=tk.W)
        ttk.Scale(settings_frame, from_=1, to=10, variable=self.border_size, orient=tk.HORIZONTAL).grid(row=3, column=1, columnspan=2, sticky=tk.EW)
        
        # Error correction
        ttk.Label(settings_frame, text="Error Correction:").grid(row=4, column=0, sticky=tk.W)
        correction_frame = ttk.Frame(settings_frame)
        correction_frame.grid(row=4, column=1, columnspan=2, sticky=tk.W)
        corrections = [("Low (7%)", "L"), ("Medium (15%)", "M"), ("High (25%)", "Q"), ("Highest (30%)", "H")]
        for i, (text, val) in enumerate(corrections):
            ttk.Radiobutton(correction_frame, text=text, variable=self.error_correction, value=val).grid(row=0, column=i, padx=2)
        
        # Preview section
        preview_frame = ttk.LabelFrame(main_frame, text="QR Code Preview", padding="10")
        preview_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.preview_label = ttk.Label(preview_frame, text="QR Code will appear here")
        self.preview_label.pack(expand=True)
        
        # Button section
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Generate QR Code", command=self.generate_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Save QR Code", command=self.save_qr).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Exit", command=self.root.quit).pack(side=tk.RIGHT)
        
        # Bind Enter key to generate QR code
        self.root.bind('<Return>', lambda event: self.generate_qr())
        
    def pick_color(self, color_var):
        from tkinter.colorchooser import askcolor
        color = askcolor(title="Choose color", initialcolor=color_var.get())
        if color[1]:  # User didn't cancel
            color_var.set(color[1])
    
    def generate_qr(self):
        data = self.qr_data.get().strip()
        if not data:
            messagebox.showwarning("Warning", "Please enter some text or URL first!")
            return
        
        try:
            # Create QR code
            qr = qrcode.QRCode(
                version=1,
                error_correction=getattr(qrcode.constants, f"ERROR_CORRECT_{self.error_correction.get()}"),
                box_size=self.qr_size.get(),
                border=self.border_size.get()
            )
            qr.add_data(data)
            qr.make(fit=True)
            
            # Create image
            img = qr.make_image(fill_color=self.fill_color.get(), back_color=self.back_color.get())
            
            # Display preview
            img.thumbnail((300, 300))  # Resize for preview
            photo = ImageTk.PhotoImage(img)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo  # Keep reference
            
            # Store the full-size image for saving
            self.current_qr_image = qr.make_image(fill_color=self.fill_color.get(), back_color=self.back_color.get())
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate QR code: {str(e)}")
    
    def save_qr(self):
        if not hasattr(self, 'current_qr_image'):
            messagebox.showwarning("Warning", "Please generate a QR code first!")
            return
            
        file_types = [
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", ".")
        ]
        
        initial_file = "qrcode.png"
        if self.qr_data.get().startswith(("http://", "https://")):
            initial_file = os.path.basename(self.qr_data.get().rstrip('/')) + ".png"
        
        file_path = filedialog.asksaveasfilename(
            title="Save QR Code",
            initialfile=initial_file,
            defaultextension=".png",
            filetypes=file_types
        )
        
        if file_path:
            try:
                # Determine format from extension
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ('.jpg', '.jpeg'):
                    format = 'JPEG'
                else:
                    format = 'PNG'
                
                self.current_qr_image.save(file_path, format=format)
                messagebox.showinfo("Success", f"QR code saved successfully to:\n{file_path}")
                self.file_path.set(file_path)
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save QR code: {str(e)}")
    
    def clear(self):
        self.qr_data.set("")
        self.preview_label.configure(image='')
        if hasattr(self, 'preview_label.image'):
            del self.preview_label.image
        if hasattr(self, 'current_qr_image'):
            del self.current_qr_image
        self.entry.focus()

if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeGeneratorApp(root)
    root.mainloop()