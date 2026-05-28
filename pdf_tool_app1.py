import os
import glob
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

try:
    from tkinterdnd2 import DND_FILES, TkinterDnD
    HAS_DND = True
except:
    HAS_DND = False

def silent_print_to_pdf(source_folder, destination_folder, progress, status_label):
    pdf_files = glob.glob(os.path.join(source_folder, "*.pdf"))
    total = len(pdf_files)
    processed = 0

    if total == 0:
        messagebox.showinfo("Info", "No PDF files found.")
        return

    progress["maximum"] = total

    for idx, pdf in enumerate(pdf_files):
        try:
            output_path = os.path.join(destination_folder, os.path.basename(pdf))

            with open(pdf, "rb") as src, open(output_path, "wb") as dst:
                dst.write(src.read())

            processed += 1
        except Exception as e:
            print(e)

        progress["value"] = idx + 1
        status_label.config(text=f"Processing {idx+1}/{total}")
        status_label.update_idletasks()

    messagebox.showinfo(
        "Done",
        f"Files found: {total}\nProcessed successfully: {processed}"
    )

def build_app():
    root = TkinterDnD.Tk() if HAS_DND else tk.Tk()
    root.title("PDF Tool")
    root.geometry("600x300")

    tk.Label(root, text="Source Folder").pack()
    source_entry = tk.Entry(root, width=70)
    source_entry.pack()

    def browse_source():
        folder = filedialog.askdirectory()
        source_entry.delete(0, tk.END)
        source_entry.insert(0, folder)

    tk.Button(root, text="Browse", command=browse_source).pack()

    if HAS_DND:
        def drop(event):
            path = event.data.strip("{}")
            source_entry.delete(0, tk.END)
            source_entry.insert(0, path)

        source_entry.drop_target_register(DND_FILES)
        source_entry.dnd_bind('<<Drop>>', drop)

    tk.Label(root, text="Destination Folder").pack()
    dest_entry = tk.Entry(root, width=70)
    dest_entry.pack()

    def browse_dest():
        folder = filedialog.askdirectory()
        dest_entry.delete(0, tk.END)
        dest_entry.insert(0, folder)

    tk.Button(root, text="Browse").pack()

    progress = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate")
    progress.pack(pady=10)

    status_label = tk.Label(root, text="Idle")
    status_label.pack()

    def run():
        source = source_entry.get()
        dest = dest_entry.get()

        if not source or not dest:
            messagebox.showerror("Error", "Select folders")
            return

        thread = threading.Thread(
            target=silent_print_to_pdf,
            args=(source, dest, progress, status_label)
        )
        thread.start()

    tk.Button(root, text="Print to PDF", command=run, bg="green", fg="white").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    build_app()
