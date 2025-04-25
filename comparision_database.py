import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Frame, Progressbar
from ttkbootstrap.constants import *
import threading
import time

def normalize_line(line):
    return line.strip().lower().replace(" ", "")

def compare_files():
    file1 = entry_file1.get()
    file2 = entry_file2.get()
    
    if not file1 or not file2:
        status_label.config(text="❌ Please select both files", bootstyle="danger")
        return
        
    status_label.config(text="⏳ Comparing files...", bootstyle="info")
    progress_bar.start()
    
    def comparison_thread():
        try:
            with open(file1, "r") as f1, open(file2, "r") as f2:
                lines1 = {normalize_line(line) for line in f1 if line.strip() and not line.startswith('--')}
                lines2 = {normalize_line(line) for line in f2 if line.strip() and not line.startswith('--')}

            diff = lines1 ^ lines2
            
            root.after(0, update_results, diff)
        except Exception as e:
            root.after(0, show_error, str(e))
    
    threading.Thread(target=comparison_thread, daemon=True).start()

def update_results(diff):
    progress_bar.stop()
    result_box.delete(1.0, tk.END)
    if diff:
        result_box.insert(tk.END, "🔍 Differences found:\n\n", "header")
        for line in diff:
            result_box.insert(tk.END, f"• {line}\n", "diff")
        status_label.config(text="✅ Comparison complete - Differences found", bootstyle="success")
    else:
        result_box.insert(tk.END, "✅ No differences found.", "success")
        status_label.config(text="✅ Comparison complete - No differences", bootstyle="success")

def show_error(error_msg):
    progress_bar.stop()
    result_box.delete(1.0, tk.END)
    result_box.insert(tk.END, f"❌ Error: {error_msg}", "error")
    status_label.config(text=f"❌ Error: {error_msg}", bootstyle="danger")

def browse_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)
        status_label.config(text="✅ File selected", bootstyle="success")

# Setup UI with ttkbootstrap
style = Style("minty")  # Modern theme
root = style.master
root.title("🗃️ MySQL Dump File Comparator")
root.geometry("900x700")

# Main container
main_frame = Frame(root, padding=20)
main_frame.pack(expand=True, fill="both")

# Header
header_frame = Frame(main_frame)
header_frame.pack(fill="x", pady=(0, 20))
Label(header_frame, text="MySQL Dump File Comparator", font=("Helvetica", 16, "bold"), bootstyle="primary").pack()

# File selection frame
file_frame = Frame(main_frame)
file_frame.pack(fill="x", pady=10)

# File 1
file1_frame = Frame(file_frame)
file1_frame.pack(fill="x", pady=5)
Label(file1_frame, text="Select Yesterday's SQL File:", bootstyle="info").pack(side="left")
entry_file1 = Entry(file1_frame, width=60)
entry_file1.pack(side="left", padx=10, expand=True, fill="x")
Button(file1_frame, text="📂 Browse", bootstyle="primary-outline", command=lambda: browse_file(entry_file1)).pack(side="left")

# File 2
file2_frame = Frame(file_frame)
file2_frame.pack(fill="x", pady=5)
Label(file2_frame, text="Select Today's SQL File:", bootstyle="info").pack(side="left")
entry_file2 = Entry(file2_frame, width=60)
entry_file2.pack(side="left", padx=10, expand=True, fill="x")
Button(file2_frame, text="📂 Browse", bootstyle="primary-outline", command=lambda: browse_file(entry_file2)).pack(side="left")

# Compare button
Button(main_frame, text="🔍 Compare Files", bootstyle="success", command=compare_files).pack(pady=20)

# Progress bar
progress_frame = Frame(main_frame)
progress_frame.pack(fill="x", pady=5)
progress_bar = Progressbar(progress_frame, bootstyle="success-striped", mode="indeterminate")
progress_bar.pack(fill="x")

# Result box
result_frame = Frame(main_frame)
result_frame.pack(expand=True, fill="both", pady=10)
result_box = scrolledtext.ScrolledText(result_frame, height=20, font=("Consolas", 10))
result_box.pack(expand=True, fill="both")

# Configure text tags for styling
result_box.tag_configure("header", font=("Consolas", 10, "bold"), foreground="#2c3e50")
result_box.tag_configure("diff", foreground="#e74c3c")
result_box.tag_configure("success", foreground="#27ae60")
result_box.tag_configure("error", foreground="#c0392b")

# Status bar
status_frame = Frame(main_frame)
status_frame.pack(fill="x", pady=(10, 0))
status_label = Label(status_frame, text="Ready", bootstyle="info")
status_label.pack(side="left")

# Make UI responsive
main_frame.grid_rowconfigure(4, weight=1)
main_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
