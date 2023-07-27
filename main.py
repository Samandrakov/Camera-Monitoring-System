import cv2
import tkinter as tk
from tkinter import messagebox, ttk
from PIL import Image, ImageTk


def get_available_cameras():
    available_cameras = []
    for i in range(10):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap.isOpened():
            available_cameras.append(f"Камера {i}")
            cap.release()
    return available_cameras


cap = None


def show_camera_window(cap):
    def update_frame():
        nonlocal cap
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Исправляем цветовую схему
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            camera_label.configure(image=photo)
            camera_label.image = photo
            camera_label.after(10, update_frame)  # Обновление каждые 10 миллисекунд
        else:
            cap.release()  # Освобождаем ресурсы камеры
            camera_label.after(1000,
                               lambda: show_camera_window(cap))  # Если кадр не захватывается, пробуем через 1 секунду

    update_frame()


def select_camera():
    global cap
    selected_camera_index = camera_combobox.current()
    if cap is not None:
        cap.release()  # Освобождаем текущую камеру
    cap = cv2.VideoCapture(selected_camera_index, cv2.CAP_DSHOW)  # Переустанавливаем объект VideoCapture
    show_camera_window(cap)  # Запускаем окно с новой камерой


def exit_program():
    global cap
    if cap is not None:
        cap.release()
    root.destroy()


# Создание окна с названием "Скрипт мониторинга камер"
root = tk.Tk()
root.title("Скрипт мониторинга камер")

# Окно с надписью "Система мониторинга"
intro_label = tk.Label(root, text="Система мониторинга", font=("Arial", 20))
intro_label.pack(padx=50, pady=30)

# Выпадающий список с камерами
available_cameras = get_available_cameras()
camera_combobox = ttk.Combobox(root, values=available_cameras)
camera_combobox.pack(padx=20, pady=10)

# Кнопка "Выбрать камеру"
select_button = tk.Button(root, text="Выбрать камеру", command=select_camera)
select_button.pack(padx=20, pady=10)

# Окно с камерой и кнопкой "завершение работы"
camera_label = tk.Label(root)
camera_label.pack(padx=20, pady=20)

# Показываем кнопку "завершение работы"
exit_button = tk.Button(root, text="Завершение работы", command=exit_program)
exit_button.pack(padx=20, pady=10)

root.mainloop()
