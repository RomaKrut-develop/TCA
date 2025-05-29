import tkinter as tk
from tkinter import ttk

def change_theme():
    selected_theme = theme_combobox.get()
    
    # Цветовые темы (фон, текст, кнопки)
    themes = {
        "Светлая": {"bg": "#f0f0f0", "fg": "black", "button_bg": "#e0e0e0"},
        "Тёмная": {"bg": "#2d2d2d", "fg": "white", "button_bg": "#3d3d3d"},
        "Синяя": {"bg": "#d6e6ff", "fg": "navy", "button_bg": "#a8c4ff"},
        "Зелёная": {"bg": "#e6ffe6", "fg": "darkgreen", "button_bg": "#b3ffb3"},
    }
    
    if selected_theme in themes:
        theme = themes[selected_theme]
        root.config(bg=theme["bg"])
        label.config(bg=theme["bg"], fg=theme["fg"])
        button.config(bg=theme["button_bg"], fg=theme["fg"])
        theme_combobox.config(style=f"{selected_theme}.TCombobox")

# Создаем главное окно
root = tk.Tk()
root.title("Смена темы")
root.geometry("400x230")

# Создаем стили для Combobox
style = ttk.Style()
style.theme_use('clam')

# Настройка стилей для разных тем
style.configure("Светлая.TCombobox", fieldbackground="#e0e0e0", foreground="black")
style.configure("Тёмная.TCombobox", fieldbackground="#3d3d3d", foreground="white")
style.configure("Синяя.TCombobox", fieldbackground="#a8c4ff", foreground="navy")
style.configure("Зелёная.TCombobox", fieldbackground="#b3ffb3", foreground="darkgreen")

# Метка
label = tk.Label(root, text="Выберите тему:", font=('Arial', 12))
label.pack(pady=10)

# Описание
label = tk.Label(root, text="Это нерабочий конфигуратор. Возможно, когда нибудь, если\nЯ не заброшу эту прогу, я смогу его\nСделать рабочим и связаным с основной консолью", font=('Arial', 9))
label.pack(pady=10)

# Выпадающий список тем
themes = ["Светлая", "Тёмная", "Синяя", "Зелёная"]
theme_combobox = ttk.Combobox(root, values=themes, state="readonly")
theme_combobox.current(0)
theme_combobox.pack(pady=5)

# Кнопка для смены темы
button = tk.Button(root, text="Применить тему", command=change_theme)
button.pack(pady=20)

# Устанавливаем светлую тему по умолчанию
change_theme()

root.mainloop()