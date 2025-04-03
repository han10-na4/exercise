import tkinter as tk
from tkinter import ttk
import math

class WindowsCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("계산기")
        self.root.geometry("320x400")
        self.root.resizable(False, False)
        
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure('TButton', font=('Segoe UI', 12))
        self.style.configure('Display.TLabel', font=('Segoe UI', 24), anchor='e')
        
        # 변수 초기화
        self.current = ""
        self.operation = ""
        self.first_num = 0
        self.memory = 0
        self.should_clear = False
        
        # 결과 표시창
        self.result_var = tk.StringVar()
        self.result_var.set("0")
        
        self.create_widgets()
        
    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="5")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # 결과 표시 레이블
        display_frame = ttk.Frame(main_frame)
        display_frame.grid(row=0, column=0, columnspan=4, sticky="nsew", pady=(0, 5))
        
        result_label = ttk.Label(
            display_frame,
            textvariable=self.result_var,
            style='Display.TLabel',
            padding=(10, 10)
        )
        result_label.pack(fill='x')
        
        # 버튼 스타일 및 텍스트
        button_style = {
            'num': {'bg': '#f0f0f0'},
            'op': {'bg': '#e1e1e1'},
            'equal': {'bg': '#0078d7', 'fg': 'white'},
            'func': {'bg': '#e1e1e1'}
        }
        
        buttons = [
            ('MC', 'func'), ('MR', 'func'), ('MS', 'func'), ('M+', 'func'),
            ('C', 'func'), ('±', 'func'), ('%', 'func'), ('÷', 'op'),
            ('7', 'num'), ('8', 'num'), ('9', 'num'), ('×', 'op'),
            ('4', 'num'), ('5', 'num'), ('6', 'num'), ('-', 'op'),
            ('1', 'num'), ('2', 'num'), ('3', 'num'), ('+', 'op'),
            ('0', 'num'), ('.', 'num'), ('=', 'equal')
        ]
        
        # 버튼 생성
        row = 1
        col = 0
        for (text, style_type) in buttons:
            if text == '0':
                btn = ttk.Button(
                    main_frame,
                    text=text,
                    command=lambda t=text: self.click(t),
                    width=8
                )
                btn.grid(row=row, column=col, columnspan=2, padx=2, pady=2, sticky="nsew")
            else:
                btn = ttk.Button(
                    main_frame,
                    text=text,
                    command=lambda t=text: self.click(t),
                    width=4
                )
                btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")
            
            col += 1
            if col > 3:
                col = 0
                row += 1
        
        # 그리드 가중치 설정
        for i in range(7):
            main_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            main_frame.grid_columnconfigure(i, weight=1)
            
    def click(self, key):
        if self.should_clear:
            self.current = ""
            self.should_clear = False
            
        if key in '0123456789.':
            if key == '.' and '.' in self.current:
                return
            self.current += key
            self.result_var.set(self.current)
            
        elif key == 'C':
            self.current = ""
            self.operation = ""
            self.first_num = 0
            self.result_var.set("0")
            
        elif key == '±':
            if self.current:
                if self.current[0] == '-':
                    self.current = self.current[1:]
                else:
                    self.current = '-' + self.current
                self.result_var.set(self.current)
                
        elif key == '%':
            if self.current:
                self.current = str(float(self.current) / 100)
                self.result_var.set(self.current)
                
        elif key in '+-×÷':
            if self.current:
                if self.operation:
                    self.calculate()
                self.first_num = float(self.current)
                self.operation = key
                self.should_clear = True
                
        elif key == '=':
            if self.current and self.operation:
                self.calculate()
                self.operation = ""
                
        elif key == 'MC':
            self.memory = 0
        elif key == 'MR':
            self.current = str(self.memory)
            self.result_var.set(self.current)
        elif key == 'MS':
            if self.current:
                self.memory = float(self.current)
        elif key == 'M+':
            if self.current:
                self.memory += float(self.current)
                
    def calculate(self):
        if self.current and self.operation:
            second_num = float(self.current)
            if self.operation == '+':
                result = self.first_num + second_num
            elif self.operation == '-':
                result = self.first_num - second_num
            elif self.operation == '×':
                result = self.first_num * second_num
            elif self.operation == '÷':
                if second_num != 0:
                    result = self.first_num / second_num
                else:
                    result = "Error"
                    
            # 결과 포맷팅
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)
                    
            self.current = str(result)
            self.result_var.set(self.current)
            self.should_clear = True

if __name__ == "__main__":
    root = tk.Tk()
    app = WindowsCalculator(root)
    root.mainloop() 