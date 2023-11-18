import tkinter as tk
from tkinter import filedialog, ttk
import os
import pdfkit

excluded_dirs = []

def browse_exclude_dir():
    global excluded_dirs
    dirname = filedialog.askdirectory(title="Select directory to exclude")
    if dirname not in excluded_dirs:
        excluded_dirs.append(dirname)
        update_excluded_dirs_listbox()

def update_excluded_dirs_listbox():
    excluded_dirs_listbox.delete(0, tk.END)
    for dir in excluded_dirs:
        excluded_dirs_listbox.insert(tk.END, dir)

def remove_excluded_dir():
    selected_index = excluded_dirs_listbox.curselection()
    if selected_index:
        removed_dir = excluded_dirs_listbox.get(selected_index)
        excluded_dirs.remove(removed_dir)
        update_excluded_dirs_listbox()
    else:
        tk.messagebox.showwarning("Warning", "No directory selected")

def browse_path():
    path = filedialog.askdirectory(title="Select Directory")
    path_entry.delete(0, tk.END)
    path_entry.insert(0, path)

def export_content():
    global path_entry, format_entry, output_path, text_area, progress_bar

    path = path_entry.get()
    format = format_entry.get()
    output_path = filedialog.asksaveasfilename(title="Save Exported Content", filetypes=[("Text Files", "*.txt"), ("PDF Files", "*.pdf")])

    if path and format and output_path:
        exclude_all_val = exclude_all.get() == 1
        export_directory_content(path, format, output_path, excluded_dirs, exclude_all_val)

def export_directory_content(path, format, output_path, excluded_dirs, exclude_all):
    global text_area, progress_bar

    content = ""
    toc = generate_table_of_contents(path, excluded_dirs, exclude_all)
    content += "Table of Contents:\n" + toc + "\n\n"

    total_files = count_files(path)
    current_file = 0

    for root, _, files in os.walk(path):
        if root in excluded_dirs and exclude_all:
            continue

        for file in files:
            file_path = os.path.join(root, file)
            file_extension = os.path.splitext(file_path)[1].lower()

            if file_extension not in [".jpg", ".svg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".mp4", ".avi", ".mov", ".wmv", ".mp3", ".wav", ".ogg"]:
                file_content = read_file_content(file_path)
                content += "\n\nFile: " + file_path + "\n"
                content += file_content

            # Update progress bar
            current_file += 1
            progress_value = int((current_file / total_files) * 100)
            progress_bar["value"] = progress_value
            progress_bar.update()

    if format == "txt":
        with open(output_path, "w", encoding="utf-8") as file:  # Specify encoding
            file.write(content)
    elif format == "pdf":
        pdfkit.from_string(content, output_path)

    text_area.delete(0.0, tk.END)
    text_area.insert(0.0, "Content exported successfully!")

def generate_table_of_contents(path, excluded_dirs, exclude_all):
    toc = ""
    for root, dirs, files in os.walk(path):
        if root in excluded_dirs and exclude_all:
            continue

        indent = root.replace(path, "").count(os.sep)
        toc += "  " * indent + f"{root}\n"

        for file in files:
            file_path = os.path.join(root, file)
            toc += "  " * (indent + 1) + f"{file_path}\n"

    return toc

def count_files(path):
    count = sum(len(files) for _, _, files in os.walk(path))
    return count

def list_directory_tree(path, level):
    content = ""
    for root, dirs, files in os.walk(path):
        indent = level * " "
        content += indent + root + "\n"
    return content

def read_file_content(file_path):
    with open(file_path, "rb") as file:
        try:
            file_content = file.read().decode("utf-8")
        except UnicodeDecodeError:
            file_content = "Binary file - cannot display content"
    return file_content

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Directory Content Exporter")

    # GUI components for directory exclusion
    excluded_dirs_listbox = tk.Listbox(root)
    excluded_dirs_listbox.pack()

    exclude_dirs_button = ttk.Button(root, text="Browse", command=browse_exclude_dir)
    exclude_dirs_button.pack()

    remove_dir_button = ttk.Button(root, text="Remove", command=remove_excluded_dir)
    remove_dir_button.pack()

    exclude_all = tk.BooleanVar()
    exclude_all_checkbox = ttk.Checkbutton(root, variable=exclude_all, text="Exclude all under")
    exclude_all_checkbox.pack()

    # GUI components for directory export
    path_label = ttk.Label(root, text="Select Directory:")
    path_label.pack()

    path_entry = ttk.Entry(root, width=50)
    path_entry.pack()

    browse_button = ttk.Button(root, text="Browse", command=browse_path)
    browse_button.pack()

    format_label = ttk.Label(root, text="Select Format (txt/pdf):")
    format_label.pack()

    format_entry = ttk.Entry(root, width=20)
    format_entry.pack()

    # Progress bar
    progress_bar = ttk.Progressbar(root, orient=tk.HORIZONTAL, length=100, mode='determinate')
    progress_bar.pack()

    export_button = ttk.Button(root, text="Export", command=export_content)
    export_button.pack()

    text_area = tk.Text(root, height=10, width=80)
    text_area.pack()

    root.mainloop()
