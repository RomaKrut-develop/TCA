import tkinter as tk
from tkinter import scrolledtext
from tkinter import Tk
import logging
import random
import string
from pygame import mixer
import time
import os
import sys

logging.basicConfig(
    level=logging.DEBUG,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    filename='debug.log',
    filemode='w',
    encoding='UTF-8'
)

root = Tk()
root.iconbitmap('icon.ico')
WIDTH = '500' # Изменение размеров окна. Ширина окна (Значение по умолчанию)
HEIGHT = '460' # Изменение размеров окна. Высота окна (Значение по умолчанию)
BG_COLOR = "#303030"  # Тёмно-серый фон всего приложения
FG_COLOR_UI = "#5E5E5E"  # Тёмно-серый текста
BG_COLOR_SCROLL = "#414141"  # Фон вывод-плейса
FG_COLOR_SCROLL_TEXT = "#CACACA"  # Фон текста вывод-плейса
root.configure(bg=BG_COLOR)
root.minsize(280, 220)
root.maxsize(1080, 700) 
root.resizable = (False, False)
root.geometry(WIDTH + 'x' + HEIGHT)
description = '-----------------------\nTCA: Tkinter Console App\nПроект вдохновлён консолью из игрового движка Source' # Описание
version = 'v0.0.2' # Версия 
root.title('TCA ' + version)
MAX_OUTPUTS_PER_SEC = 10
last_output_times = []
output_counter = 0
MAX_WORD_LENGTH = 50

def print_output(text):
    output_area.configure(state='normal')
    output_area.insert(tk.END, text + "\n")
    output_area.configure(state='disabled')
    output_area.see(tk.END)  # Автопрокрутка вниз

def calculate_exp(exp): # Поднаготная калькулятора
    try:
        exp = exp.replace(" ", "") # Удаляем все пробелы для простоты обработки
        
        allowed_ops = {'+', '-', '*', '/', '**', '(', ')'}         # Проверяем допустимые операции
        if not all(c.isdigit() or c in allowed_ops for c in exp):
            mixer.init() # Инициализируем pygame микшер для звуков
            mixer.music.load('error.mp3') # Загружаем сам звук
            mixer.music.play(0)
            return "Недопустимые символы в выражении"
        
        return eval(exp, {'__builtins__':None}, {})
    except ZeroDivisionError:
        mixer.music.load('error.mp3')
        mixer.music.play(0)
        return 'Деление на ноль недопускается'
    except:
        mixer.music.load('error.mp3')
        mixer.music.play(0)
        return 'Некорректное выражение'
    
def gen_r_word(length: int) -> str: # Генератор хаотичных слов
    if length <= 0 or length > MAX_WORD_LENGTH:
        mixer.music.load('error.mp3')
        mixer.music.play(0)
        raise ValueError(f'\nВведите количество символов от 1 до {MAX_WORD_LENGTH}.')
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def execute_command(command): # Центр комманд
    if command.startswith("gen_r_w_"): # Комманда генерации слов
        try:
            length = int(command[8:])
            word = gen_r_word(length)
            logging.info(f"Генератор выдал слово '{word}' длинной в {length} символов")
            return f"{word}"
        except ValueError as e:
            mixer.music.load('error.mp3')
            mixer.music.play(0)
            return f"Недопустимая операция {str(e)}\nИспользуйте: 'gen_r_w_(длина)'"
    if command.lower() == "help": # Помощь
        mixer.init()
        mixer.music.load('output.mp3')
        mixer.music.play(0)
        logging.info('Пользователь вводит комманду help')
        return "Список базовых комманд: help, clear, exit\n----------------\nВведите числовое выражение (num)(оператор)(num) и получите ответ"
    elif command.lower() == "clear": # Очистка
        mixer.music.load('output.mp3')
        mixer.music.play(0)
        output_area.configure(state='normal')
        output_area.delete(1.0, tk.END)
        output_area.configure(state='disabled')
        logging.info('Пользователь вводит комманду clear. Консоль была отчищена')
    elif command.lower() == "show_info":  # Показывает информационное сообщение
        mixer.music.load('output.mp3')
        mixer.music.play(0)
        print_output(description)
    elif command.lower() == "exit": # Закрытие
        root.quit()
        logging.info('Пользователь закрыл программу')
        return ""
    # Здесь, логика интегрированного калькулятора
    elif any(op in command for op in ['+', '-', '*', '/']):
        result = calculate_exp(command)
        logging.info(f'Пользователь использует калькулятор. Выражение: {command}. Ответ: {result}')
        return result
    elif command.lower() == command: # Проверка на не очень умных пользователей которые любят спамить
        global last_output_times
        current_time = time.time()
        last_output_times = [t for t in last_output_times if current_time - t < 1.0]
        if len(last_output_times) >= MAX_OUTPUTS_PER_SEC:
            global output_counter
            mixer.init(frequency=44100, size=-16, channels=8)
            sound = mixer.Sound('output.mp3')
            channel = mixer.find_channel()
            if channel:
                channel.play(sound)
            print_output(f'Слишком много выводов в секунду!')
            output_counter += 10 # Учтём, что пока я не придумал как добавить сброс оутпута по таймеру, у пользователя не будет шанса прекратить баловаться с программой
            if output_counter >= 210:
                try:
                    logging.info('Пользователь решил поспамить в консоль. Исход очевиден')
                    mixer.init(frequency=44100, size=-16, channels=8)
                    stop_sound = mixer.Sound('stop.mp3')
                    stop_channel = mixer.find_channel()
                    stop_channel.play(stop_sound)
                    time.sleep(0.4)
                    sys.exit()
                except AttributeError:
                    print('')
        else:
            print_output(f"Возможно вы ввели неверную комманду: {command}\n(введите 'help' для списка команд)")
        last_output_times.append(current_time)
    else:
        return calculate_exp(command)
     # Здесь, конец его логики

def process_input(event=None): # Обрабатываем ввод пользователя
    mixer.init()
    mixer.music.load('button.mp3')
    mixer.music.play(0)
    command = input_entry.get()
    print_output(f"> {command}")
    
    # Обработка команды
    result = execute_command(command)
    if result:  # Если есть что выводить
        print_output(str(result))
    
    # Очищаем поле ввода
    input_entry.delete(0, tk.END)

# Поле вывода с прокруткой
output_area = scrolledtext.ScrolledText(
    root, 
    font=('Courier new', 14),
    bg=BG_COLOR_SCROLL,
    fg=FG_COLOR_SCROLL_TEXT,
    wrap=tk.WORD, 
    width=60, 
    height=20,
    state='disabled'
)

output_area.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

# Метка для поля ввода
input_label = tk.Label(root, text="Введите команду:", bg=BG_COLOR, fg=FG_COLOR_UI, font=('Consolas', 14))
input_label.grid(row=1, column=0, sticky="w", padx=10)

# Поле ввода
input_entry = tk.Entry(root, width=60)
input_entry.grid(row=2, column=0, padx=10, pady=(0, 10), sticky="we")
input_entry.bind("<Return>", process_input)  # Обработка нажатия Enter

# Кнопка отправки
submit_button = tk.Button(root, text="Подтвердить", command=process_input, bg=BG_COLOR, fg=FG_COLOR_UI, font=('Consolas', 14))
submit_button.grid(row=3, column=0, pady=(0, 10))

# Настройка расширения строк и столбцов
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Приветственное сообщение
logging.info('Консоль была запущенна')
print_output("Добро пожаловать в TCA!\nВведите команду и нажмите Enter")

if __name__ == "__main__": # Точка входа в приложение
    root.mainloop()