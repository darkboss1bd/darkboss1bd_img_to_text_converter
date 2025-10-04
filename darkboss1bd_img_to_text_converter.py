import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import threading
import os
import sys
import time
import base64
from PIL import Image, ImageTk, ImageEnhance
import io
import subprocess

class DarkBossNotesConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("DarkBoss1BD - Notes to Text Converter")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0a0a')
        self.root.resizable(True, True)
        
        # Center the window
        self.center_window()
        
        # Configure style
        self.setup_styles()
        
        # Initialize variables
        self.image_path = None
        self.extracted_text = ""
        self.tesseract_available = self.check_tesseract()
        
        self.create_widgets()
        self.open_links()
        
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width = 900
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def setup_styles(self):
        self.style = ttk.Style()
        
        # Use default theme to avoid style errors
        available_themes = self.style.theme_names()
        if 'clam' in available_themes:
            self.style.theme_use('clam')
        else:
            self.style.theme_use(available_themes[0] if available_themes else 'default')
        
        # Configure basic styles without complex names
        self.style.configure('Dark.TFrame', background='#0a0a0a')
        self.style.configure('Dark.TLabel', background='#0a0a0a', foreground='#00ff00', font=('Courier', 10))
        self.style.configure('Title.TLabel', background='#0a0a0a', foreground='#00ff00', font=('Courier', 16, 'bold'))
        
        # Simple button style
        self.style.configure('HackerButton.TButton', 
                           background='#003300', 
                           foreground='#00ff00', 
                           font=('Courier', 10),
                           focuscolor='none')
        
        # Progressbar style - FIXED: Use simple name
        self.style.configure('HackerProgressbar.Vertical.TProgressbar',
                           background='#00ff00',
                           troughcolor='#0a0a0a',
                           borderwidth=0,
                           lightcolor='#00ff00',
                           darkcolor='#00ff00')
        
        self.style.configure('HackerProgressbar.Horizontal.TProgressbar',
                           background='#00ff00',
                           troughcolor='#0a0a0a',
                           borderwidth=0,
                           lightcolor='#00ff00',
                           darkcolor='#00ff00')
        
        # Labelframe style
        self.style.configure('Hacker.TLabelframe',
                           background='#0a0a0a',
                           foreground='#00ff00')
        
        self.style.configure('Hacker.TLabelframe.Label',
                           background='#0a0a0a',
                           foreground='#00ff00')
        
    def check_tesseract(self):
        """Check if Tesseract is available in system PATH"""
        try:
            if os.name == 'nt':  # Windows
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, text=True, timeout=5, shell=True)
            else:  # Linux/Mac
                result = subprocess.run(['tesseract', '--version'], 
                                      capture_output=True, text=True, timeout=5)
            return result.returncode == 0
        except:
            return False
        
    def install_tesseract_instructions(self):
        """Provide instructions for installing Tesseract"""
        message = """
Tesseract OCR is required for text extraction.

For Kali Linux:
sudo apt update && sudo apt install tesseract-ocr

For Windows:
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Install with default settings
3. Add to PATH: C:\\Program Files\\Tesseract-OCR\\

For macOS:
brew install tesseract
        """
        messagebox.showinfo("Install Tesseract OCR", message)
        webbrowser.open("https://github.com/UB-Mannheim/tesseract/wiki")
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header with branding
        self.create_header(main_frame)
        
        # Upload area
        self.create_upload_area(main_frame)
        
        # Image preview area
        self.create_preview_area(main_frame)
        
        # Progress bar - FIXED: Use correct style
        self.progress = ttk.Progressbar(main_frame, 
                                      style='HackerProgressbar.Horizontal.TProgressbar', 
                                      mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # Buttons frame
        self.create_buttons(main_frame)
        
        # Text output area
        self.create_output_area(main_frame)
        
        # Footer with contact info
        self.create_footer(main_frame)
        
    def create_header(self, parent):
        header_frame = ttk.Frame(parent, style='Dark.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # DarkBoss1BD branding
        title_label = ttk.Label(header_frame, text="▓▓▓ DarkBoss1BD ▓▓▓", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        # Status indicator
        status_text = "▓ SYSTEM READY ▓" if self.tesseract_available else "▓ INSTALL TESSERACT ▓"
        status_label = ttk.Label(header_frame, text=status_text, style='Dark.TLabel')
        status_label.pack(side=tk.RIGHT)
        
        # Matrix style separator
        separator = ttk.Label(header_frame, text="═" * 80, style='Dark.TLabel')
        separator.pack(fill=tk.X, pady=5)
        
    def create_upload_area(self, parent):
        upload_frame = ttk.Frame(parent, style='Dark.TFrame')
        upload_frame.pack(fill=tk.X, pady=10)
        
        upload_label = ttk.Label(upload_frame, 
                               text="[+] UPLOAD A PHOTO OF YOUR NOTES TO TURN THEM INTO TEXT!", 
                               style='Dark.TLabel')
        upload_label.pack(pady=5)
        
        # Styled upload button
        upload_btn = ttk.Button(upload_frame, 
                              text="▓ CLICK TO UPLOAD OR DRAG AND DROP ▓", 
                              command=self.upload_image,
                              style='HackerButton.TButton')
        upload_btn.pack(pady=10)
        
        file_types_label = ttk.Label(upload_frame, 
                                   text="[SUPPORTED FORMATS] PNG, JPG, GIF | [MAX SIZE] 10MB", 
                                   style='Dark.TLabel')
        file_types_label.pack()
        
    def create_preview_area(self, parent):
        self.preview_frame = ttk.LabelFrame(parent, text="▓ IMAGE PREVIEW ▓", style='Hacker.TLabelframe')
        self.preview_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.preview_label = ttk.Label(self.preview_frame, 
                                     text="[NO IMAGE SELECTED]\n\nClick upload button above", 
                                     style='Dark.TLabel',
                                     justify=tk.CENTER)
        self.preview_label.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
        
    def create_buttons(self, parent):
        buttons_frame = ttk.Frame(parent, style='Dark.TFrame')
        buttons_frame.pack(fill=tk.X, pady=10)
        
        # Button container
        btn_container = ttk.Frame(buttons_frame, style='Dark.TFrame')
        btn_container.pack()
        
        extract_btn = ttk.Button(btn_container, text="▓ EXTRACT TEXT ▓", 
                               command=self.extract_text,
                               style='HackerButton.TButton')
        extract_btn.grid(row=0, column=0, padx=3, pady=3)
        
        if not self.tesseract_available:
            install_btn = ttk.Button(btn_container, text="▓ INSTALL TESSERACT ▓", 
                                   command=self.install_tesseract_instructions,
                                   style='HackerButton.TButton')
            install_btn.grid(row=0, column=1, padx=3, pady=3)
        
        enhance_btn = ttk.Button(btn_container, text="▓ ENHANCE IMAGE ▓", 
                               command=self.enhance_image,
                               style='HackerButton.TButton')
        enhance_btn.grid(row=0, column=2, padx=3, pady=3)
        
        clear_btn = ttk.Button(btn_container, text="▓ CLEAR ALL ▓", 
                             command=self.clear_all,
                             style='HackerButton.TButton')
        clear_btn.grid(row=0, column=3, padx=3, pady=3)
        
        save_btn = ttk.Button(btn_container, text="▓ SAVE TEXT ▓", 
                            command=self.save_text,
                            style='HackerButton.TButton')
        save_btn.grid(row=0, column=4, padx=3, pady=3)
        
    def create_output_area(self, parent):
        output_frame = ttk.LabelFrame(parent, text="▓ EXTRACTED TEXT ▓", style='Hacker.TLabelframe')
        output_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create text widget with hacker style
        self.text_output = tk.Text(output_frame, 
                                 bg='#0a0a0a', 
                                 fg='#00ff00', 
                                 insertbackground='#00ff00', 
                                 font=('Courier', 10),
                                 wrap=tk.WORD,
                                 relief='flat',
                                 selectbackground='#006600')
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(output_frame, orient=tk.VERTICAL, command=self.text_output.yview)
        self.text_output.configure(yscrollcommand=scrollbar.set)
        
        self.text_output.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Initial message
        welcome_text = """▓▓▓ DarkBoss1BD - Notes to Text Converter ▓▓▓

[INSTRUCTIONS]
1. Click UPLOAD button to select an image
2. Use ENHANCE IMAGE for better results (optional)
3. Click EXTRACT TEXT to convert image to text
4. Save your extracted text

[SUPPORTED LANGUAGES]
• English (Default)
• Add more languages by installing Tesseract language packs

[STATUS]: Ready for operation...
"""
        self.text_output.insert(tk.END, welcome_text)
        
    def create_footer(self, parent):
        footer_frame = ttk.Frame(parent, style='Dark.TFrame')
        footer_frame.pack(fill=tk.X, pady=10)
        
        # Contact information
        contact_text = "[TELEGRAM] @darkvaiadmin | [CHANNEL] @windowspremiumkey"
        contact_label = ttk.Label(footer_frame, text=contact_text, style='Dark.TLabel')
        contact_label.pack(pady=2)
        
        # Version info
        version_text = "DarkBoss1BD v2.2 | Advanced OCR Tool | Kali Linux Optimized"
        version_label = ttk.Label(footer_frame, text=version_text, style='Dark.TLabel')
        version_label.pack(pady=2)
        
        # Separator
        separator = ttk.Label(footer_frame, text="─" * 100, style='Dark.TLabel')
        separator.pack(fill=tk.X, pady=5)
        
    def upload_image(self):
        file_path = filedialog.askopenfilename(
            title="Select an image file",
            filetypes=[
                ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            # Check file size (max 10MB)
            file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
            if file_size > 10:
                messagebox.showerror("Error", "File size exceeds 10MB limit!")
                return
                
            self.image_path = file_path
            self.display_image(file_path)
            
            # Update status
            self.text_output.delete(1.0, tk.END)
            self.text_output.insert(tk.END, f"[STATUS] Image loaded successfully: {os.path.basename(file_path)}\n")
            self.text_output.insert(tk.END, f"[SIZE] {file_size:.2f} MB\n")
            self.text_output.insert(tk.END, "[ACTION] Click 'EXTRACT TEXT' to begin OCR process\n")
            
    def display_image(self, file_path):
        try:
            image = Image.open(file_path)
            # Resize image to fit preview area
            image.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(image)
            
            self.preview_label.configure(image=photo, text="")
            self.preview_label.image = photo
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def enhance_image(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
            
        try:
            image = Image.open(self.image_path)
            
            # Enhance image for better OCR
            # Convert to grayscale
            if image.mode != 'L':
                image = image.convert('L')
                
            # Enhance contrast
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)
            
            # Enhance sharpness
            enhancer = ImageEnhance.Sharpness(image)
            image = enhancer.enhance(2.0)
            
            # Save enhanced image temporarily
            enhanced_path = "enhanced_temp.png"
            image.save(enhanced_path, "PNG")
            
            # Display enhanced image
            image.thumbnail((400, 300))
            photo = ImageTk.PhotoImage(image)
            self.preview_label.configure(image=photo)
            self.preview_label.image = photo
            
            self.image_path = enhanced_path
            
            self.text_output.insert(tk.END, "[STATUS] Image enhanced for better text recognition!\n")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to enhance image: {str(e)}")
            
    def extract_text(self):
        if not self.tesseract_available:
            messagebox.showerror("Error", "Tesseract OCR is not installed!")
            self.install_tesseract_instructions()
            return
            
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first!")
            return
            
        self.progress.start()
        self.text_output.delete(1.0, tk.END)
        self.text_output.insert(tk.END, "[STATUS] Starting text extraction...\n")
        self.text_output.insert(tk.END, "[PROCESS] Analyzing image with Tesseract OCR...\n")
        
        # Run OCR in a separate thread
        threading.Thread(target=self.perform_ocr, daemon=True).start()
        
    def perform_ocr(self):
        try:
            # Use subprocess to call tesseract
            output_file = "darkboss_output"
            
            if os.name == 'nt':  # Windows
                cmd = f'tesseract "{self.image_path}" "{output_file}" -l eng --psm 6'
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30, shell=True)
            else:  # Linux/Mac
                cmd = ['tesseract', self.image_path, output_file, '-l', 'eng', '--psm', '6']
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                # Read the output file
                txt_file = output_file + '.txt'
                if os.path.exists(txt_file):
                    with open(txt_file, 'r', encoding='utf-8') as f:
                        text = f.read()
                    
                    # Clean up temporary file
                    try:
                        os.remove(txt_file)
                    except:
                        pass
                        
                    self.root.after(0, self.update_text_output, text)
                else:
                    self.root.after(0, self.show_error, "Output file not found")
            else:
                self.root.after(0, self.show_error, f"OCR failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            self.root.after(0, self.show_error, "OCR process timed out")
        except Exception as e:
            self.root.after(0, self.show_error, f"OCR failed: {str(e)}")
        finally:
            self.root.after(0, self.progress.stop)
            
    def update_text_output(self, text):
        self.extracted_text = text
        self.text_output.delete(1.0, tk.END)
        
        if text.strip():
            # Add header
            header = "▓▓▓ DarkBoss1BD - EXTRACTED TEXT ▓▓▓\n"
            header += "═" * 50 + "\n\n"
            self.text_output.insert(tk.END, header)
            
            # Insert extracted text
            self.text_output.insert(tk.END, text)
            
            # Add footer with stats
            footer = f"\n\n═" * 50 + "\n"
            footer += f"[EXTRACTION COMPLETE] Characters: {len(text)} | Words: {len(text.split())}\n"
            footer += "[STATUS] Text ready for copying or saving\n"
            self.text_output.insert(tk.END, footer)
        else:
            error_msg = "[ERROR] No text detected in the image.\n"
            error_msg += "[SUGGESTIONS]\n"
            error_msg += "• Try enhancing the image\n"
            error_msg += "• Use a clearer, higher resolution photo\n"
            error_msg += "• Ensure text is clearly visible\n"
            error_msg += "• Check lighting and focus\n"
            self.text_output.insert(tk.END, error_msg)
            
    def show_error(self, message):
        messagebox.showerror("Error", message)
        self.progress.stop()
        self.text_output.insert(tk.END, f"[ERROR] {message}\n")
        
    def clear_all(self):
        self.image_path = None
        self.extracted_text = ""
        self.text_output.delete(1.0, tk.END)
        self.preview_label.configure(image='')
        self.preview_label.image = None
        self.preview_label.configure(text="[NO IMAGE SELECTED]\n\nClick upload button above")
        
        # Reset to welcome message
        welcome_text = """▓▓▓ DarkBoss1BD - Notes to Text Converter ▓▓▓

[INSTRUCTIONS]
1. Click UPLOAD button to select an image
2. Use ENHANCE IMAGE for better results (optional)
3. Click EXTRACT TEXT to convert image to text
4. Save your extracted text

[STATUS]: Ready for operation...
"""
        self.text_output.insert(tk.END, welcome_text)
        
    def save_text(self):
        if not self.extracted_text.strip():
            messagebox.showwarning("Warning", "No text to save!")
            return
            
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ],
            title="Save extracted text"
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write("═" * 60 + "\n")
                    f.write("DarkBoss1BD - Extracted Text\n")
                    f.write("═" * 60 + "\n")
                    f.write(f"Date: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Source: {os.path.basename(self.image_path) if self.image_path else 'Unknown'}\n")
                    f.write("═" * 60 + "\n\n")
                    f.write(self.extracted_text)
                    f.write(f"\n\n═" * 60 + "\n")
                    f.write("Extracted by DarkBoss1BD Notes Converter\n")
                    f.write("Telegram: @darkvaiadmin | Channel: @windowspremiumkey\n")
                
                messagebox.showinfo("Success", f"Text saved to:\n{file_path}")
                
                # Update status
                self.text_output.insert(tk.END, f"\n[STATUS] Text saved successfully: {file_path}\n")
                
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {str(e)}")
                
    def open_links(self):
        """Open Telegram links automatically"""
        telegram_links = [
            "https://t.me/darkvaiadmin",
            "https://t.me/windowspremiumkey"
        ]
        
        for link in telegram_links:
            try:
                webbrowser.open_new_tab(link)
                time.sleep(1)  # Small delay between openings
            except Exception as e:
                print(f"Failed to open {link}: {e}")

def check_dependencies():
    """Check and install required Python packages"""
    required_packages = {
        'Pillow': 'PIL',
        'requests': 'requests'
    }
    
    print("🔍 Checking dependencies...")
    
    for pkg, import_name in required_packages.items():
        try:
            if import_name == 'PIL':
                import PIL
            else:
                __import__(import_name)
            print(f"✅ {pkg} is installed")
        except ImportError:
            print(f"📦 Installing {pkg}...")
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install', pkg])
                print(f"✅ {pkg} installed successfully")
            except subprocess.CalledProcessError:
                print(f"❌ Failed to install {pkg}")
                return False
    return True

def main():
    print("🚀 Starting DarkBoss1BD Notes Converter...")
    
    # Check dependencies
    if not check_dependencies():
        print("❌ Dependency installation failed!")
        return
        
    try:
        root = tk.Tk()
        app = DarkBossNotesConverter(root)
        
        print("✅ Application started successfully!")
        print("📱 Telegram links should open automatically...")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application:\n{str(e)}")

if __name__ == "__main__":
    main()
