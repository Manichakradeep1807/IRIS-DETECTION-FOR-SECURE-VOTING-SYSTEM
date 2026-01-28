import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import sys
import os
import json
import numpy as np
import time
from datetime import datetime
import glob

# Import Theme
try:
    from theme_manager import theme_manager
    THEME_AVAILABLE = True
except ImportError:
    THEME_AVAILABLE = False

class AIWorkbench:
    def __init__(self, root, close_callback=None):
        self.root = root
        self.close_callback = close_callback
        self.is_training = False
        
        # Load Theme
        if THEME_AVAILABLE:
            self.colors = theme_manager.get_theme_colors()
            self.fonts = theme_manager.get_theme_fonts()
        else:
            self.colors = {
                'primary': "#0f172a", 'secondary': "#1e293b",
                'accent_primary': "#38bdf8", 'accent_secondary': "#818cf8",
                'success': "#10b981", 'warning': "#f59e0b", 'danger': "#ef4444",
                'text_primary': "#f8fafc", 'text_secondary': "#94a3b8"
            }
            self.fonts = {"primary": "Segoe UI", "secondary": "Arial"}

        self.setup_ui()
        self.refresh_stats()

    def setup_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.colors['primary'])
        header.pack(fill=tk.X, padx=30, pady=20)
        
        tk.Label(header, text="🛠️ AI WORKBENCH", font=(self.fonts['primary'], 20, "bold"),
                 fg=self.colors['accent_primary'], bg=self.colors['primary']).pack(side=tk.LEFT)
        
        if self.close_callback:
            tk.Button(header, text="Back to Dashboard", command=self.close_callback,
                     bg=self.colors['secondary'], fg=self.colors['text_secondary'],
                     font=(self.fonts['primary'], 10), relief="flat", padx=15).pack(side=tk.RIGHT)

        # Main Layout (Grid)
        content = tk.Frame(self.root, bg=self.colors['primary'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)
        
        # Left Col: Model Control
        left_col = tk.Frame(content, bg=self.colors['primary'])
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Right Col: Stats & Logs
        right_col = tk.Frame(content, bg=self.colors['primary'])
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(15, 0))

        # --- Model Status Card ---
        self.create_card(left_col, "Model Status", self.build_model_status)
        
        # --- Training Control Card ---
        self.create_card(left_col, "Training Operations", self.build_training_controls)
        
        # --- Dataset Stats ---
        self.create_card(right_col, "Dataset Statistics", self.build_dataset_stats)
        
        # --- Output Log ---
        self.create_card(right_col, "Process Logs", self.build_log_viewer, expand=True)

    def create_card(self, parent, title, content_builder, expand=False):
        card = tk.Frame(parent, bg=self.colors['secondary'], padx=20, pady=20)
        card.pack(fill=tk.BOTH, expand=expand, pady=(0, 20))
        
        tk.Label(card, text=title, font=(self.fonts['primary'], 14, "bold"),
                 fg=self.colors['text_primary'], bg=self.colors['secondary']).pack(anchor="w", pady=(0, 15))
        
        content_builder(card)

    def build_model_status(self, parent):
        self.status_labels = {}
        
        def row(label, key):
            f = tk.Frame(parent, bg=self.colors['secondary'])
            f.pack(fill=tk.X, pady=5)
            tk.Label(f, text=label, font=(self.fonts['primary'], 11), fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(side=tk.LEFT)
            l = tk.Label(f, text="--", font=(self.fonts['primary'], 11, "bold"), fg=self.colors['text_primary'], bg=self.colors['secondary'])
            l.pack(side=tk.RIGHT)
            self.status_labels[key] = l

        row("Current Accuracy:", "acc")
        row("Last Trained:", "date")
        row("Model Type:", "type")
        row("Status:", "status")

    def build_training_controls(self, parent):
        tk.Label(parent, text="Select a training mode:", font=(self.fonts['primary'], 10),
                 fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(anchor="w", pady=(0, 10))
        
        modes = [
            ("⚡ Fast Retrain (CNN)", "Quick adaptation (2-5 mins)", self.start_fast_train),
            ("🚀 High Accuracy (ResNet)", "Deep Learning (30+ mins)", self.start_high_acc_train),
        ]
        
        for name, desc, cmd in modes:
            btn_frame = tk.Frame(parent, bg=self.colors['secondary'], pady=5)
            btn_frame.pack(fill=tk.X)
            
            btn = tk.Button(btn_frame, text=name, command=cmd,
                           bg=self.colors['accent_secondary'], fg="#0f172a",
                           font=(self.fonts['primary'], 11, "bold"), relief="flat", padx=15, pady=8)
            btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            tk.Label(parent, text=desc, font=(self.fonts['primary'], 9),
                     fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(anchor="w", pady=(0, 10))

    def build_dataset_stats(self, parent):
        self.dataset_labels = {}
        def row(label, key):
             f = tk.Frame(parent, bg=self.colors['secondary'])
             f.pack(fill=tk.X, pady=3)
             tk.Label(f, text=label, fg=self.colors['text_secondary'], bg=self.colors['secondary']).pack(side=tk.LEFT)
             l = tk.Label(f, text="0", fg=self.colors['text_primary'], bg=self.colors['secondary'])
             l.pack(side=tk.RIGHT)
             self.dataset_labels[key] = l
             
        row("Total Samples:", "total")
        row("Number of Classes:", "classes")
        
        bg_bar = tk.Frame(parent, bg="#334155", height=10)
        bg_bar.pack(fill=tk.X, pady=10)
        self.usage_bar = tk.Frame(bg_bar, bg=self.colors['success'], height=10, width=0)
        self.usage_bar.pack(side=tk.LEFT)

    def build_log_viewer(self, parent):
        self.log_text = tk.Text(parent, bg="#0f172a", fg="#d1d5db", font=("Consolas", 10),
                               height=10, relief="flat", padx=10, pady=10)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log("AI Workbench Initialized.")
        self.log("Ready for operations.")

    def log(self, msg):
        self.log_text.insert(tk.END, f"[{datetime.now().strftime('%H:%M:%S')}] {msg}\n")
        self.log_text.see(tk.END)

    def refresh_stats(self):
        # Check Model
        model_path = 'model/high_accuracy_model.json'
        if os.path.exists(model_path):
            self.status_labels['status'].config(text="Active", fg=self.colors['success'])
            self.status_labels['type'].config(text="ResNet-Custom")
            # Try to get timestamp
            mtime = os.path.getmtime(model_path)
            self.status_labels['date'].config(text=datetime.fromtimestamp(mtime).strftime('%Y-%m-%d'))
        else:
            self.status_labels['status'].config(text="Not Found", fg=self.colors['danger'])
        
        # Check Dataset
        try:
            x_path = 'model/X.txt.npy'
            y_path = 'model/Y.txt.npy'
            if os.path.exists(x_path):
                # We won't load the whole thing to avoid lag, just get file size hint or try-load if small
                # Actually, loading just to check shape is kinda heavy.
                # Let's count files in dataset folder instead?
                # Assume 'sample_dataset' folder structure or just use saved npy if available
                # For safety, let's just use os.stat to guess or load lightweight
                total = 0
                classes = 0
                
                # Try sample_dataset count
                if os.path.exists('sample_dataset'):
                    people = glob.glob('sample_dataset/*')
                    classes = len(people)
                    total = sum(len(glob.glob(os.path.join(p, '*'))) for p in people)
                
                self.dataset_labels['total'].config(text=str(total))
                self.dataset_labels['classes'].config(text=str(classes))
                
        except Exception:
            pass

    def start_fast_train(self):
        self.run_training("Fast CNN", "train_fast_model.py")

    def start_high_acc_train(self):
        self.run_training("High Accuracy ResNet", "train_high_accuracy_model.py")

    def run_training(self, name, script_name):
        if self.is_training:
            messagebox.showwarning("Busy", "Training already in progress")
            return
            
        if not os.path.exists(script_name):
            self.log(f"Error: Script {script_name} not found!")
            return

        confirm = messagebox.askyesno("Confirm Training", f"Start {name}? This may take time.")
        if not confirm: return
        
        self.is_training = True
        self.log(f"Starting {name}...")
        
        def train_thread():
            try:
                import subprocess
                process = subprocess.Popen(
                    [sys.executable, script_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    bufsize=1,
                    universal_newlines=True
                )
                
                for line in process.stdout:
                    self.root.after(0, lambda l=line.strip(): self.log(l))
                
                process.wait()
                
                if process.returncode == 0:
                    self.root.after(0, lambda: self.log("✅ Training Completed Successfully!"))
                    self.root.after(0, self.refresh_stats)
                    self.root.after(0, lambda: messagebox.showinfo("Success", f"{name} Completed!"))
                else:
                    self.root.after(0, lambda: self.log("❌ Training Failed."))
                    
            except Exception as e:
                self.root.after(0, lambda e=e: self.log(f"Error: {e}"))
            finally:
                self.is_training = False

        threading.Thread(target=train_thread, daemon=True).start()

def show_workbench(root, close_cmd):
    # Clear and show
    for w in root.winfo_children(): w.destroy()
    AIWorkbench(root, close_callback=close_cmd)

if __name__ == "__main__":
    r = tk.Tk()
    r.geometry("1000x700")
    AIWorkbench(r)
    r.mainloop()
