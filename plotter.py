import os
import re
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# === CONFIGURATION ===
BASE_DIR = "./data"  # folders like 10_readings, 25_readings, 50_readings
PATTERN = re.compile(r"(\d+)_f(\d+)d(\d+)n(\d+)_(\d+)\.txt")

# === STEP 1: Extract f/d/n/index values across all folders ===
def extract_parameters(base_dir):
    values_f, values_d, values_n, values_idx = set(), set(), set(), set()
    folders = [f for f in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, f))]

    for folder in folders:
        folder_path = os.path.join(base_dir, folder)
        for fname in os.listdir(folder_path):
            m = PATTERN.match(fname)
            if m:
                p, f_val, d_val, n_val, idx = m.groups()
                values_f.add(int(f_val))
                values_d.add(int(d_val))
                values_n.add(int(n_val))
                values_idx.add(int(idx))

    return sorted(values_f), sorted(values_d), sorted(values_n), sorted(values_idx)

# === STEP 2: Read file data ===
def read_file(filepath):
    values = []
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return values
    with open(filepath, "r") as file:
        for line in file:
            v = line.strip()
            if v:
                try:
                    values.append(int(v)/4095*2.5)
                except ValueError:
                    pass
    return values

# === STEP 3: GUI ===
def main():
    root = tk.Tk()
    root.title("Zoomable Multi-Plot Viewer")
    root.geometry("1000x700")

    # --- Frames ---
    selection_frame = ttk.Frame(root, padding=15)
    selection_frame.pack(side="top", fill="x")

    plot_frame = ttk.Frame(root)
    plot_frame.pack(side="top", fill="both", expand=True)

    # --- Dropdowns ---
    values_f, values_d, values_n, values_idx = extract_parameters(BASE_DIR)

    label_font = ("Arial", 12, "bold")
    combobox_font = ("Arial", 12)
    status_font = ("Arial", 11, "italic")

    ttk.Label(selection_frame, text="Frequency (f):", font=label_font).grid(column=0, row=0, sticky="e", padx=5, pady=5)
    ttk.Label(selection_frame, text="Distance (d):", font=label_font).grid(column=2, row=0, sticky="e", padx=5, pady=5)
    ttk.Label(selection_frame, text="n:", font=label_font).grid(column=4, row=0, sticky="e", padx=5, pady=5)
    ttk.Label(selection_frame, text="Index:", font=label_font).grid(column=6, row=0, sticky="e", padx=5, pady=5)

    combo_f = ttk.Combobox(selection_frame, values=values_f, state="readonly", width=6, font=combobox_font, justify="center")
    combo_d = ttk.Combobox(selection_frame, values=values_d, state="readonly", width=6, font=combobox_font, justify="center")
    combo_n = ttk.Combobox(selection_frame, values=values_n, state="readonly", width=6, font=combobox_font, justify="center")
    combo_idx = ttk.Combobox(selection_frame, values=values_idx, state="readonly", width=6, font=combobox_font, justify="center")

    combo_f.grid(column=1, row=0, padx=5, pady=5)
    combo_d.grid(column=3, row=0, padx=5, pady=5)
    combo_n.grid(column=5, row=0, padx=5, pady=5)
    combo_idx.grid(column=7, row=0, padx=5, pady=5)

    result_label = ttk.Label(selection_frame, text="Select parameters and click Plot", font=status_font)
    result_label.grid(column=0, row=1, columnspan=8, pady=10)

    # --- Scrollable plot_frame ---
    canvas_frame = tk.Canvas(plot_frame)
    scrollbar = ttk.Scrollbar(plot_frame, orient="vertical", command=canvas_frame.yview)
    scrollable_frame = ttk.Frame(canvas_frame)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas_frame.configure(
            scrollregion=canvas_frame.bbox("all")
        )
    )

    canvas_frame.create_window((0,0), window=scrollable_frame, anchor="nw")
    canvas_frame.configure(yscrollcommand=scrollbar.set)

    canvas_frame.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # --- Get all filepaths matching selected f/d/n/index ---
    def get_matching_filepaths():
        f_val = combo_f.get()
        d_val = combo_d.get()
        n_val = combo_n.get()
        idx = combo_idx.get()
        if not (f_val and d_val and n_val and idx):
            messagebox.showwarning("Warning", "Please select all parameters.")
            return []

        filepaths = []
        folders = [f for f in os.listdir(BASE_DIR) if os.path.isdir(os.path.join(BASE_DIR, f))]
        for folder in folders:
            prefix = folder.split("_")[0]  # e.g., "50"
            folder_path = os.path.join(BASE_DIR, folder)
            filename = f"{prefix}_f{f_val}d{d_val}n{n_val}_{idx}.txt"
            full_path = os.path.join(folder_path, filename)
            if os.path.exists(full_path):
                filepaths.append((prefix, full_path))
        return filepaths

    # --- Plot all matching files ---
    def on_plot_all():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()  # clear previous plots

        filepaths = get_matching_filepaths()
        if not filepaths:
            result_label.config(text="⚠️ No files found for selected parameters", foreground="red")
            return

        for prefix, filepath in filepaths:
            values = read_file(filepath)
            if not values:
                continue

            # --- Figure and Canvas ---
            fig, ax = plt.subplots(figsize=(8,3))
            x = np.arange(len(values))
            ax.plot(x, values)
            ax.set_xlim(0, len(values))
            ax.set_ylim(0.8, 2.8)
            ax.set_xlabel("Sample Index")
            ax.set_ylabel("Voltage (V)")
            ax.set_title(f"{prefix}: {os.path.basename(filepath)}")

            canvas = FigureCanvasTkAgg(fig, master=scrollable_frame)
            canvas.get_tk_widget().pack(fill="x", pady=5)
            canvas.draw()

            # --- Add toolbar for zoom/pan ---
            toolbar_frame = ttk.Frame(scrollable_frame)
            toolbar_frame.pack(fill="x")
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()

        result_label.config(text=f"✅ Plotted {len(filepaths)} files", foreground="green")

    # --- Plot button ---
    plot_button = ttk.Button(selection_frame, text="Plot All", command=on_plot_all, width=12)
    plot_button.grid(column=8, row=0, padx=10, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()