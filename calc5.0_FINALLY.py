import tkinter as tk
from tkinter import messagebox
import math
from PIL import Image, ImageTk
import urllib.request
from io import BytesIO

class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Барный калькулятор")
        self.window.resizable(False, False)
        
        # Загрузка фонового изображения
        self.load_background_image()
        
        # Цветовая схема
        self.colors = {
            'display_bg': '#1A1A2E',  
            'display_fg': '#FFFFFF',
            'number_bg': '#16213E',   
            'number_fg': '#FFFFFF',
            'number_hover': '#0F3460',  
            'operator_bg': '#533483',  
            'operator_fg': '#FFFFFF',
            'operator_hover': '#6A4C9C',  
            'special_bg': '#E94560',   
            'special_fg': '#FFFFFF',
            'special_hover': '#FF6B8B',
            'window_bg': '#000000'
        }
        
        self.setup_ui()
        self.center_window()
        self.bind_events()
        
    def load_background_image(self):
        """Загрузка фонового изображения из интернета с использованием urllib"""
        try:
            # URL изображение с пиксельным баром из pinterest
            image_url = "https://i.pinimg.com/736x/02/7c/1e/027c1e92162aa79ccea473b78dd63fbb.jpg"
            
            # Загрузка изображения из интернета с помощью urllib
            with urllib.request.urlopen(image_url) as response:
                image_data = response.read()
            
            # Открытие и обработка изображения
            original_image = Image.open(BytesIO(image_data))
            
            # Изменение размера изображения под размер калькулятора
            width = 400
            height = 600
            resized_image = original_image.resize((width, height), Image.LANCZOS)
            
            # Конвертация для Tkinter
            self.background_image = ImageTk.PhotoImage(resized_image)
            
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
            # Создаем простой градиентный фон в случае ошибки
            self.background_image = None
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание Canvas для фонового изображения
        self.canvas = tk.Canvas(
            self.window,
            width=400,
            height=600,
            highlightthickness=0
        )
        self.canvas.pack(fill="both", expand=True)
        
        # Добавление фонового изображения если оно загружено
        if self.background_image:
            self.canvas.create_image(0, 0, image=self.background_image, anchor="nw")
        else:
            # Создаем градиентный фон в случае отсутствия изображения
            self.create_gradient_background()
        
        # Создание полупрозрачного темного overlay для лучшей читаемости
        self.canvas.create_rectangle(
            0, 0, 400, 600, 
            fill="#000000", 
            stipple="gray50",  # Создает эффект полупрозрачности
            width=0
        )
        
        # Поле ввода/вывода
        self.display_var = tk.StringVar()
        
        # Создание фона для дисплея
        self.canvas.create_rectangle(15, 15, 385, 85, fill=self.colors['display_bg'], outline="")
        
        self.display = tk.Entry(
            self.window,
            textvariable=self.display_var,
            font=('DejaVu', 28, 'bold'),
            justify='right',
            bd=0,
            relief='flat',
            bg=self.colors['display_bg'],
            fg=self.colors['display_fg'],
            insertbackground='white',
            highlightthickness=2,
            highlightcolor=self.colors['operator_bg'],
            highlightbackground=self.colors['number_bg']
        )
        
        # Размещение дисплея на canvas
        self.display_window = self.canvas.create_window(
            20, 20,
            window=self.display,
            width=365,
            height=60,
            anchor="nw"
        )
        
        # Создание кнопок
        self.create_buttons()
    
    def create_gradient_background(self):
        """Создание градиентного фона если изображение не загрузилось"""
        for i in range(600):
            # Создаем сине-фиолетовый градиент, соответствующий изображению
            r = int(20 + 30 * i / 600)
            g = int(20 + 40 * i / 600)
            b = int(40 + 80 * i / 600)
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 400, i, fill=color)
    
    def create_buttons(self):
        """Создание кнопок калькулятора"""
        buttons = [
            ('C', 1, 0), ('√', 1, 1), ('<-', 1, 2), ('÷', 1, 3),  
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('-', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('0', 5, 0, 2), ('.', 5, 2), ('=', 5, 3)
        ]
        
        self.buttons = {}
        button_width = 85
        button_height = 70
        start_x = 20
        start_y = 100
        spacing = 10
        
        for button in buttons:
            text = button[0]
            row = button[1]
            col = button[2]
            colspan = button[3] if len(button) > 3 else 1
            
            if text in ['=', '+', '-', '×', '÷']:  
                bg_color = self.colors['operator_bg']
                fg_color = self.colors['operator_fg']
                hover_color = self.colors['operator_hover']
            elif text in ['C', '√', '<-']:
                bg_color = self.colors['special_bg']
                fg_color = self.colors['special_fg']
                hover_color = self.colors['special_hover']
            else:
                bg_color = self.colors['number_bg']
                fg_color = self.colors['number_fg']
                hover_color = self.colors['number_hover']
            
            x = start_x + col * (button_width + spacing)
            y = start_y + row * (button_height + spacing)
            width = button_width * colspan + spacing * (colspan - 1)
            
            # Создание фона для кнопки
            button_bg = self.canvas.create_rectangle(
                x, y, x + width, y + button_height,
                fill=bg_color,
                outline="",
                width=0
            )
            
            # Создание кнопки
            btn = tk.Button(
                self.window,
                text=text,
                font=('DejaVu', 20, 'bold'),
                bg=bg_color,
                fg=fg_color,
                activebackground=hover_color,
                activeforeground=fg_color,
                relief='flat',
                bd=0,
                height=2,
                width=6 if colspan == 1 else 13
            )
            
            # Размещение кнопки на canvas
            btn_window = self.canvas.create_window(
                x, y,
                window=btn,
                width=width,
                height=button_height,
                anchor="nw"
            )
            
            # Сохраняем ссылки на элементы кнопки
            self.buttons[text] = {
                'button': btn,
                'background': button_bg,
                'window': btn_window,
                'bg_color': bg_color,
                'hover_color': hover_color
            }
            
            # Привязываем события мыши
            btn.bind('<Enter>', lambda e, t=text: self.on_enter(e, t))
            btn.bind('<Leave>', lambda e, t=text: self.on_leave(e, t))
            btn.bind('<Button-1>', self.button_click)
    
    def on_enter(self, event, button_text):
        """Эффект при наведении курсора"""
        if button_text in self.buttons:
            btn_data = self.buttons[button_text]
            self.canvas.itemconfig(btn_data['background'], fill=btn_data['hover_color'])
    
    def on_leave(self, event, button_text):
        """Возврат к исходному цвету при уходе курсора"""
        if button_text in self.buttons:
            btn_data = self.buttons[button_text]
            self.canvas.itemconfig(btn_data['background'], fill=btn_data['bg_color'])
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.window.update_idletasks()
        width = 400
        height = 600
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def bind_events(self):
        """Привязка событий клавиатуры"""
        self.window.bind('<Key>', self.key_press)
        self.window.bind('<BackSpace>', self.backspace)
        self.window.focus_set()
    
    def button_click(self, event):
        """Обработка клика по кнопке"""
        text = event.widget.cget('text')
        self.process_input(text)
    
    def key_press(self, event):
        """Обработка нажатия клавиш"""
        key = event.char
        keys_mapping = {
            '\r': '=',
            '\x08': '<-',  
            '*': '×',
            'x': '×',
            'X': '×',
            's': '√',
            'S': '√',
            '/': '÷'  
        }
        
        if key in keys_mapping:
            key = keys_mapping[key]
        
        if key in '0123456789.+-/=×÷√' or key == 'C' or key == '<-':  
            self.process_input(key)
    
    def backspace(self, event):
        """Обработка специальной клавиши Backspace"""
        self.process_input('<-')
    
    def process_input(self, value):
        """Обработка ввода"""
        current_text = self.display_var.get()
        
        try:
            if value == 'C':
                self.display_var.set('')
            elif value == '<-':  
                if current_text:
                    self.display_var.set(current_text[:-1])
            elif value == '=':
                result = self.calculate(current_text)
                self.display_var.set(result)
            elif value == '√':
                if current_text:
                    num = float(current_text)
                    if num < 0:
                        messagebox.showerror("Упс!", "Корень из отрицательного числа!")
                        return
                    self.display_var.set(math.sqrt(num))
            else:
                # Заменяем × на * и ÷ на / для вычислений
                display_value = value
                if value == '×':
                    display_value = '*'
                elif value == '÷':
                    display_value = '/'
                    
                new_text = current_text + display_value
                self.display_var.set(new_text)
                
        except Exception as e:
            messagebox.showerror("Упс!", "Некорректный ввод!")
            self.display_var.set('')
    
    def calculate(self, expression):
        """Вычисление математического выражения"""
        try:
            # Заменяем × на * и ÷ на / для вычисления
            expression = expression.replace('×', '*').replace('÷', '/')
            # Проверка деления на ноль
            if '/0' in expression and not '/0.' in expression:
                raise ZeroDivisionError
            result = eval(expression)
            # Форматируем результат (убираем лишние нули после запятой)
            if isinstance(result, float) and result.is_integer():
                return int(result)
            return result
        except ZeroDivisionError:
            messagebox.showerror("Упс!", "Делить на ноль нельзя!")
            return ''
        except:
            messagebox.showerror("Упс!", "Некорректное выражение!")
            return ''
    
    def run(self):
        """Запуск приложения"""
        self.window.mainloop()

if __name__ == "__main__":
    calc = Calculator()
    calc.run()
