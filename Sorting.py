import matplotlib.pyplot as plt
import numpy as np
import matplotlib.image as mpimg
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Global flag to stop sorting when the user closes the window
stop_sorting = False

# Load background images
# Note: Ensure these files exist in your directory
try:
    bg_image = mpimg.imread("sortingpage2.png")  # Used in sorting visualization
    original_bg = Image.open("sortingpage1.png")  # Used for Tkinter background
except FileNotFoundError:
    print("Warning: Background images not found. Using solid colors.")
    bg_image = None
    original_bg = None

def draw_bars_with_labels(arr, step):
    """ Draws bars with background image and updates the plot. """
    global stop_sorting
    if stop_sorting:
        return
    
    plt.clf()
    if bg_image is not None:
        plt.imshow(bg_image, aspect='auto', extent=[-1, len(arr), 0, max(arr) + 5], alpha=0.7)
    
    plt.bar(range(len(arr)), arr, color="#1035AC")
    
    # Modernized Matplotlib font
    for i, val in enumerate(arr):
        plt.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=9, color='black', fontname='sans-serif')
    
    plt.yticks(np.arange(0, 101, 20))
    tick_positions = [4, 9, 14, 19, 24, 29]
    tick_labels = [5, 10, 15, 20, 25, 30]

    plt.xticks(tick_positions, tick_labels)
    plt.title(f"Sorting Visualization - Step {step}", fontsize=12, fontweight='bold', family='sans-serif')
    plt.pause(0.01)

def sorting_wrapper(sort_function, arr):
    """ Wrapper to handle premature closing of the plot window. """
    global stop_sorting
    stop_sorting = False

    def on_close(event):
        global stop_sorting
        stop_sorting = True
        plt.close()

    fig = plt.figure()
    fig.canvas.mpl_connect("close_event", on_close)
    sort_function(arr)

    if not stop_sorting:
        finalize_plot(arr)

def finalize_plot(arr):
    plt.clf()
    if bg_image is not None:
        plt.imshow(bg_image, aspect='auto', extent=[-1, len(arr), 0, max(arr) + 5], alpha=0.7)
    plt.bar(range(len(arr)), arr, color="#1035AC")
    
    for i, val in enumerate(arr):
        plt.text(i, val + 0.5, str(val), ha='center', va='bottom', fontsize=9, color='black')
    
    plt.title("Sorting Completed", fontsize=14, fontweight='bold')
    plt.show(block=True)

# --- Sorting Algorithms ---

def bubble_sort(arr):
    n = len(arr)
    step = 0
    for i in range(n):
        for j in range(0, n - i - 1):
            if stop_sorting: return
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                step += 1
                draw_bars_with_labels(arr, step)

def insertion_sort(arr):
    step = 0
    for i in range(1, len(arr)):
        if stop_sorting: return
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
            step += 1
            draw_bars_with_labels(arr, step)
        arr[j + 1] = key
        step += 1
        draw_bars_with_labels(arr, step)

def selection_sort(arr):
    step = 0
    n = len(arr)
    for i in range(n):
        if stop_sorting: return
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]: min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        step += 1
        draw_bars_with_labels(arr, step)

def merge_sort(arr):
    def _merge_sort(arr, left, right, step):
        if left < right:
            mid = (left + right) // 2
            step = _merge_sort(arr, left, mid, step)
            step = _merge_sort(arr, mid + 1, right, step)
            step = merge(arr, left, mid, right, step)
        return step
    def merge(arr, left, mid, right, step):
        left_copy = arr[left:mid + 1]
        right_copy = arr[mid + 1:right + 1]
        i, j, k = 0, 0, left
        while i < len(left_copy) and j < len(right_copy):
            if stop_sorting: return step
            if left_copy[i] < right_copy[j]:
                arr[k] = left_copy[i]; i += 1
            else:
                arr[k] = right_copy[j]; j += 1
            k += 1; step += 1; draw_bars_with_labels(arr, step)
        while i < len(left_copy):
            if stop_sorting: return step
            arr[k] = left_copy[i]; i += 1; k += 1; step += 1; draw_bars_with_labels(arr, step)
        while j < len(right_copy):
            if stop_sorting: return step
            arr[k] = right_copy[j]; j += 1; k += 1; step += 1; draw_bars_with_labels(arr, step)
        return step
    _merge_sort(arr, 0, len(arr) - 1, 0)

def shell_sort(arr):
    n = len(arr); gap = n // 2; step = 0
    while gap > 0:
        for i in range(gap, n):
            if stop_sorting: return
            temp = arr[i]; j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]; j -= gap; step += 1; draw_bars_with_labels(arr, step)
            arr[j] = temp; step += 1; draw_bars_with_labels(arr, step)
        gap //= 2

def quick_sort(arr):
    def _quick_sort(items, low, high, step):
        if low < high:
            pi, step = partition(items, low, high, step)
            step = _quick_sort(items, low, pi - 1, step)
            step = _quick_sort(items, pi + 1, high, step)
        return step
    def partition(items, low, high, step):
        pivot = items[high]; i = low - 1
        for j in range(low, high):
            if stop_sorting: return step
            if items[j] < pivot:
                i += 1; items[i], items[j] = items[j], items[i]; step += 1; draw_bars_with_labels(items, step)
        items[i + 1], items[high] = items[high], items[i + 1]; step += 1; draw_bars_with_labels(items, step)
        return i + 1, step
    _quick_sort(arr, 0, len(arr) - 1, 0)

def heap_sort(arr):
    def heapify(arr, n, i, step):
        largest = i; l = 2 * i + 1; r = 2 * i + 2
        if l < n and arr[l] > arr[largest]: largest = l
        if r < n and arr[r] > arr[largest]: largest = r
        if largest != i:
            if stop_sorting: return step
            arr[i], arr[largest] = arr[largest], arr[i]; step += 1; draw_bars_with_labels(arr, step)
            step = heapify(arr, n, largest, step)
        return step
    n = len(arr); step = 0
    for i in range(n // 2 - 1, -1, -1): step = heapify(arr, n, i, step)
    for i in range(n - 1, 0, -1):
        if stop_sorting: return
        arr[i], arr[0] = arr[0], arr[i]; step += 1; draw_bars_with_labels(arr, step); step = heapify(arr, i, 0, step)

# --- GUI Setup ---
root = tk.Tk()
root.title("Sorting Algorithms Visualization")

# Stylized Font Constants
HEADER_FONT = ("Segoe UI", 14, "bold")
BUTTON_FONT = ("Segoe UI", 9, "bold")
EXPANDED_FONT = ("Segoe UI", 10, "bold")
ENTRY_FONT = ("Consolas", 11)

def update_background(event=None):
    if original_bg is None: return
    new_width = root.winfo_width()
    new_height = root.winfo_height()
    resized_bg = original_bg.resize((new_width, new_height), Image.Resampling.LANCZOS)
    new_tk_bg = ImageTk.PhotoImage(resized_bg)
    canvas.config(width=new_width, height=new_height)
    canvas.itemconfig(bg_canvas_image, image=new_tk_bg)
    canvas.image = new_tk_bg 
    canvas.coords(bg_canvas_image, 0, 0)
    update_positions()

initial_width, initial_height = 900, 650
root.geometry(f"{initial_width}x{initial_height}")

canvas = tk.Canvas(root, highlightthickness=0)
canvas.pack(fill="both", expand=True)

if original_bg:
    resized_bg = original_bg.resize((initial_width, initial_height), Image.Resampling.LANCZOS)
    tk_bg_image = ImageTk.PhotoImage(resized_bg)
    bg_canvas_image = canvas.create_image(0, 0, image=tk_bg_image, anchor="nw")
else:
    bg_canvas_image = canvas.create_rectangle(0, 0, initial_width, initial_height, fill="#f0f0f0")

def process_input(sort_algorithm):
    user_input = entry.get()
    try:
        arr = list(map(int, user_input.split()))
        if len(arr) != 30: raise ValueError("Please enter exactly 30 integers.")
        if any(val > 100 for val in arr): raise ValueError("Numbers must be 0-100.")

        plt.ion()
        sorting_wrapper({
            "bubble": bubble_sort, "insertion": insertion_sort, "selection": selection_sort,
            "merge": merge_sort, "shell": shell_sort, "quick": quick_sort, "heap": heap_sort
        }[sort_algorithm], arr)
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

# UI Elements with Upgraded Design
label_id = canvas.create_text(0, 0, text="Enter 30 Integers (Space-Separated):", 
                             fill="black", font=HEADER_FONT, anchor="center")

entry = tk.Entry(root, width=60, font=ENTRY_FONT, relief="flat", bd=5)
entry_window = canvas.create_window(0, 0, window=entry)

# Light Green Buttons with cleaner styling and Expansion Hover effect
def create_styled_button(text, cmd):
    btn = tk.Button(root, text=text, command=cmd, 
                   bg="#90EE90", fg="#2E422E", 
                   activebackground="#7CCD7C", font=BUTTON_FONT,
                   relief="flat", padx=10, pady=5, cursor="hand2")
    
    # Hover effect functions with expansion
    def on_enter(e):
        btn.config(bg="#A8F5A8", font=EXPANDED_FONT, padx=15, pady=8)  # Increase size and padding
        
    def on_leave(e):
        btn.config(bg="#90EE90", font=BUTTON_FONT, padx=10, pady=5)    # Reset to original
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

bubble_button = create_styled_button("Bubble Sort", lambda: process_input("bubble"))
insertion_button = create_styled_button("Insertion Sort", lambda: process_input("insertion"))
selection_button = create_styled_button("Selection Sort", lambda: process_input("selection"))
merge_button = create_styled_button("Merge Sort", lambda: process_input("merge"))
shell_button = create_styled_button("Shell Sort", lambda: process_input("shell"))
quick_button = create_styled_button("Quick Sort", lambda: process_input("quick"))
heap_button = create_styled_button("Heap Sort", lambda: process_input("heap"))

buttons = [bubble_button, insertion_button, selection_button, merge_button, shell_button, quick_button, heap_button]
button_windows = [canvas.create_window(0, 0, window=b) for b in buttons]

def update_positions():
    w, h = root.winfo_width(), root.winfo_height()
    cx = w // 2
    
    # Position Label
    canvas.coords(label_id, cx, h - 240)
    # Position Entry
    canvas.coords(entry_window, cx, h - 190)

    # Position Buttons
    spacing = 120
    total_w = (len(buttons) - 1) * spacing
    start_x = (w - total_w) // 2
    for i, b_win in enumerate(button_windows):
        canvas.coords(b_win, start_x + (i * spacing), h - 100)

root.bind("<Configure>", update_background)
root.resizable(True, True)
root.mainloop()