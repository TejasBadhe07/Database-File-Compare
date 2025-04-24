import tkinter as tk
from tkinter import filedialog, scrolledtext
from ttkbootstrap import Style
from ttkbootstrap.widgets import Entry, Button, Label, Frame

def normalize_line(line):
    return line.strip().lower().replace(" ", "")

def compare_files():
    file1 = entry_file1.get()
    file2 = entry_file2.get()

    try:
        with open(file1, "r") as f1, open(file2, "r") as f2:
            lines1 = {normalize_line(line) for line in f1 if line.strip() and not line.startswith('--')}
            lines2 = {normalize_line(line) for line in f2 if line.strip() and not line.startswith('--')}

        diff = lines1 ^ lines2

        result_box.delete(1.0, tk.END)
        if diff:
            result_box.insert(tk.END, "🔍 Differences found:\n\n")
            for line in diff:
                result_box.insert(tk.END, f"{line}\n")
        else:
            result_box.insert(tk.END, "✅ No differences found.")
    except Exception as e:
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, f"❌ Error: {e}")

def browse_file(entry_widget):
    filename = filedialog.askopenfilename(filetypes=[("SQL files", "*.sql"), ("All files", "*.*")])
    if filename:
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, filename)

# Setup UI with ttkbootstrap
style = Style("flatly")  # Try: 'flatly', 'darkly', 'cyborg', 'minty', etc.
root = style.master
root.title("🗃️ MySQL Dump File Comparator")
root.geometry("800x600")

frame = Frame(root, padding=20)
frame.pack(expand=True, fill="both")

# File 1
Label(frame, text="Select Yesterday's SQL File:", bootstyle="info").grid(row=0, column=0, sticky="w")
entry_file1 = Entry(frame, width=60)
entry_file1.grid(row=1, column=0, padx=(0, 10))
Button(frame, text="📂 Browse", bootstyle="primary", command=lambda: browse_file(entry_file1)).grid(row=1, column=1)

# File 2
Label(frame, text="Select Today's SQL File:", bootstyle="info").grid(row=2, column=0, sticky="w", pady=(10, 0))
entry_file2 = Entry(frame, width=60)
entry_file2.grid(row=3, column=0, padx=(0, 10))
Button(frame, text="📂 Browse", bootstyle="primary", command=lambda: browse_file(entry_file2)).grid(row=3, column=1)

# Compare button
Button(frame, text="🔍 Compare Files", bootstyle="success outline", command=compare_files).grid(row=4, column=0, columnspan=2, pady=20)

# Result box
result_box = scrolledtext.ScrolledText(frame, height=18, font=("Consolas", 10))
result_box.grid(row=5, column=0, columnspan=2, sticky="nsew")

# Make UI responsive
frame.grid_rowconfigure(5, weight=1)
frame.grid_columnconfigure(0, weight=1)

root.mainloop()
