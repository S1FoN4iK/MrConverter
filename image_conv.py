import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import *
from PIL import Image, ImageTk
import os
import ctypes
import platform

def setup_dpi_awareness():
    """Настройка поддержки HiDPI для чёткого отображения"""
    if platform.system() == "Windows":
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    elif platform.system() == "Darwin":
        root.tk.call('tk', 'scaling', 2.0)
    else:
        root.tk.call('tk', 'scaling', 1.5)

def create_icon(size, color):
    """Создание иконки в памяти для кнопок"""
    img = Image.new("RGBA", size, color)
    return ImageTk.PhotoImage(img)

def drop(event):
    """Обработка drag-and-drop файлов"""
    file_paths = root.tk.splitlist(event.data)
    file_list.delete(0, tk.END)
    for file_path in file_paths:
        if os.path.splitext(file_path)[1].lower() in ['.png', '.jpg', '.jpeg', '.bmp', '.gif', '.tiff']:
            file_list.insert(tk.END, file_path)
    update_status(f"Добавлено {file_list.size()} файлов")

def browse_files():
    """Выбор файлов через диалог"""
    files = filedialog.askopenfilenames(
        title="Выберите изображения",
        filetypes=[("Изображения", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff")]
    )
    if files:
        file_list.delete(0, tk.END)
        for file in files:
            file_list.insert(tk.END, file)
        update_status(f"Добавлено {file_list.size()} файлов")
        animate_button(browse_button)

def clear_list():
    """Очистка списка файлов"""
    file_list.delete(0, tk.END)
    update_status("Список очищен")
    animate_button(clear_button)

def convert_to_jpg():
    """Конвертация изображений в JPG"""
    if file_list.size() == 0:
        messagebox.showwarning("Предупреждение", "Выберите хотя бы одно изображение!")
        return

    output_dir = filedialog.askdirectory(title="Выберите папку для сохранения")
    if not output_dir:
        return

    progress["maximum"] = file_list.size()
    progress["value"] = 0
    convert_button.config(state="disabled")
    update_status("Конвертация началась...")

    try:
        for i in range(file_list.size()):
            file_path = file_list.get(i)
            img = Image.open(file_path)
            if img.mode in ("RGBA", "LA"):
                img = img.convert("RGB")
            base_name = os.path.splitext(os.path.basename(file_path))[0]
            output_path = os.path.join(output_dir, f"{base_name}.jpg")
            img.save(output_path, "JPEG", quality=90, optimize=True, subsampling=0)
            progress["value"] = i + 1
            root.update_idletasks()

        update_status(f"Конвертировано {file_list.size()} изображений!")
        messagebox.showinfo("Успех", f"Конвертировано {file_list.size()} изображений в JPG!")
        animate_button(convert_button)
    except Exception as e:
        update_status("Ошибка при конвертации")
        messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
    finally:
        convert_button.config(state="normal")

def animate_button(button):
    """Простая анимация изменения размера кнопки"""
    original_size = button.winfo_width()
    for scale in [1.0, 1.1, 1.0]:
        button.config(width=int(original_size * scale // 10))
        root.update()
        root.after(50)

def update_status(text):
    """Обновление строки статуса"""
    status_label.config(text=text)

root = TkinterDnD.Tk()
root.title("Конвертер изображений в JPG")
root.geometry("800x500")
root.configure(bg="#1a1a2e")
root.resizable(True, True)
setup_dpi_awareness()

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=15, font=("Segoe UI", 14), foreground="#e94560", borderwidth=0)
style.map("TButton", background=[("active", "#0f172a")])
style.configure("TLabel", background="#1a1a2e", foreground="#e94560", font=("Segoe UI", 14))
style.configure("TProgressbar", troughcolor="#0f172a", background="#e94560", thickness=25)

browse_icon = create_icon((20, 20), (233, 69, 96, 255))
convert_icon = create_icon((20, 20), (233, 69, 96, 255))
clear_icon = create_icon((20, 20), (233, 69, 96, 255))

main_frame = ttk.Frame(root)
main_frame.pack(padx=20, pady=20, fill="both", expand=True)

info_label = ttk.Label(main_frame, text="Перетащите изображения или выберите их для конвертации в JPG")
info_label.pack(pady=10)

file_list = tk.Listbox(main_frame, height=10, bg="#0f172a", fg="#e94560", font=("Segoe UI", 12))
file_list.pack(fill="both", expand=True, pady=10)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=10)

browse_button = ttk.Button(button_frame, text="Выбрать файлы", image=browse_icon, compound="left", command=browse_files)
browse_button.pack(side="left", padx=5)

clear_button = ttk.Button(button_frame, text="Очистить список", image=clear_icon, compound="left", command=clear_list)
clear_button.pack(side="left", padx=5)

convert_button = ttk.Button(button_frame, text="Конвертировать", image=convert_icon, compound="left", command=convert_to_jpg)
convert_button.pack(side="left", padx=5)

progress = ttk.Progressbar(main_frame, orient="horizontal", mode="determinate")
progress.pack(fill="x", pady=10)

status_label = ttk.Label(main_frame, text="Готово к работе")
status_label.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', drop)

root.mainloop()