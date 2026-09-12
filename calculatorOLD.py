#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Калкулатор за Linux Mint 22.2
с две памети (M1 и M2) + индикация на стойностите
"""

import tkinter as tk
from tkinter import font as tkfont
import math

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калкулатор")
        self.root.resizable(False, False)
        self.root.configure(bg="#2d2d2d")

        window_width = 400
        window_height = 520
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.max_len = 14

        self.memory1 = 0.0
        self.memory2 = 0.0

        self.create_widgets()
        self.update_memory_buttons()

    def create_widgets(self):
        # ===== Дисплей =====
        display_frame = tk.Frame(self.root, bg="#2d2d2d")
        display_frame.pack(fill="x", padx=10, pady=(12, 8))

        display_font = tkfont.Font(family="Ubuntu", size=22, weight="bold")
        self.display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            font=display_font,
            bg="#1e1e1e",
            fg="#ffffff",
            anchor="e",
            padx=12,
            pady=18,
            relief="flat"
        )
        self.display.pack(fill="x")

        # ===== Бутони =====
        buttons_frame = tk.Frame(self.root, bg="#2d2d2d")
        buttons_frame.pack(expand=True, fill="both", padx=8, pady=8)

        BLUE = "#3a7bd5"
        self.btn_font = tkfont.Font(family="Ubuntu", size=12, weight="bold")
        self.btn_font_small = tkfont.Font(family="Ubuntu", size=10, weight="bold")

        # Ред 0
        self.make_btn(buttons_frame, "C",   0, 0, "#ff6b6b")
        self.make_btn(buttons_frame, "⌫",   0, 1, "#4a4a4a")
        self.make_btn(buttons_frame, "√",   0, 2, "#4a4a4a")
        self.make_btn(buttons_frame, "÷",   0, 3, "#ff9500")
        self.btn_m1_add = self.make_btn(buttons_frame, "+M1", 0, 4, BLUE, small=True)

        # Ред 1
        self.make_btn(buttons_frame, "7",   1, 0, "#5a5a5a")
        self.make_btn(buttons_frame, "8",   1, 1, "#5a5a5a")
        self.make_btn(buttons_frame, "9",   1, 2, "#5a5a5a")
        self.make_btn(buttons_frame, "×",   1, 3, "#ff9500")
        self.btn_m1_rcl = self.make_btn(buttons_frame, "RM1", 1, 4, BLUE, small=True)

        # Ред 2
        self.make_btn(buttons_frame, "4",   2, 0, "#5a5a5a")
        self.make_btn(buttons_frame, "5",   2, 1, "#5a5a5a")
        self.make_btn(buttons_frame, "6",   2, 2, "#5a5a5a")
        self.make_btn(buttons_frame, "−",   2, 3, "#ff9500")
        self.btn_m2_add = self.make_btn(buttons_frame, "+M2", 2, 4, BLUE, small=True)

        # Ред 3
        self.make_btn(buttons_frame, "1",   3, 0, "#5a5a5a")
        self.make_btn(buttons_frame, "2",   3, 1, "#5a5a5a")
        self.make_btn(buttons_frame, "3",   3, 2, "#5a5a5a")
        self.make_btn(buttons_frame, "+",   3, 3, "#ff9500")
        self.btn_m2_rcl = self.make_btn(buttons_frame, "RM2", 3, 4, BLUE, small=True)

        # Ред 4
        self.make_btn(buttons_frame, "0",   4, 0, "#5a5a5a")
        self.make_btn(buttons_frame, ".",   4, 1, "#5a5a5a")
        self.make_btn(buttons_frame, "%",   4, 2, "#4a4a4a")
        self.make_btn(buttons_frame, "=",   4, 3, "#ff9500")
        self.make_btn(buttons_frame, "±",   4, 4, "#4a4a4a")

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)

    def make_btn(self, parent, text, row, col, color, small=False):
        font = self.btn_font_small if small else self.btn_font
        btn = tk.Button(
            parent,
            text=text,
            font=font,
            bg=color,
            fg="white",
            activebackground="#777777",
            activeforeground="white",
            relief="flat",
            bd=0,
            command=lambda t=text: self.on_button_click(t)
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2, ipady=10)
        return btn

    def short_mem(self, value):
        """Кратък формат за показване върху бутона"""
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value)
        if len(s) > 7:
            try:
                s = f"{float(value):.2e}"
            except:
                s = s[:7]
        return s

    def update_memory_buttons(self):
        """Обновява текста на memory бутоните със стойностите"""
        m1 = self.short_mem(self.memory1)
        m2 = self.short_mem(self.memory2)

        self.btn_m1_add.config(text=f"+M1\n{m1}")
        self.btn_m1_rcl.config(text=f"RM1\n{m1}")
        self.btn_m2_add.config(text=f"+M2\n{m2}")
        self.btn_m2_rcl.config(text=f"RM2\n{m2}")

    def get_current_value(self):
        try:
            if not self.expression:
                return 0.0
            expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            return float(eval(expr))
        except:
            return 0.0

    def format_result(self, value):
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value)
        if len(s) > self.max_len:
            try:
                s = f"{float(value):.6e}"
            except:
                s = s[:self.max_len]
        return s

    def on_button_click(self, char):
        # Понеже текстът на memory бутоните се променя, взимаме само началото
        if char.startswith("+M1"):
            char = "+M1"
        elif char.startswith("RM1"):
            char = "RM1"
        elif char.startswith("+M2"):
            char = "+M2"
        elif char.startswith("RM2"):
            char = "RM2"

        if char == "C":
            self.expression = ""
            self.display_var.set("0")

        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")

        elif char == "√":
            try:
                value = self.get_current_value()
                if value < 0:
                    self.display_var.set("Грешка")
                    self.expression = ""
                    return
                result = math.sqrt(value)
                self.expression = self.format_result(result)
                self.display_var.set(self.expression)
            except:
                self.display_var.set("Грешка")
                self.expression = ""

        elif char == "%":
            try:
                value = self.get_current_value() / 100
                self.expression = self.format_result(value)
                self.display_var.set(self.expression)
            except:
                self.display_var.set("Грешка")
                self.expression = ""

        elif char == "±":
            try:
                value = -self.get_current_value()
                self.expression = self.format_result(value)
                self.display_var.set(self.expression)
            except:
                pass

        elif char == "+M1":
            self.memory1 += self.get_current_value()
            self.update_memory_buttons()

        elif char == "RM1":
            mem_str = self.format_result(self.memory1)
            if self.expression == "" or self.display_var.get() == "0":
                self.expression = mem_str
            else:
                last = self.expression[-1] if self.expression else ""
                if last in "+−×÷":
                    self.expression += mem_str
                else:
                    self.expression = mem_str
            self.display_var.set(self.expression)

        elif char == "+M2":
            self.memory2 += self.get_current_value()
            self.update_memory_buttons()

        elif char == "RM2":
            mem_str = self.format_result(self.memory2)
            if self.expression == "" or self.display_var.get() == "0":
                self.expression = mem_str
            else:
                last = self.expression[-1] if self.expression else ""
                if last in "+−×÷":
                    self.expression += mem_str
                else:
                    self.expression = mem_str
            self.display_var.set(self.expression)

        elif char == "=":
            try:
                expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
                result = eval(expr)
                self.expression = self.format_result(result)
                self.display_var.set(self.expression)
            except:
                self.display_var.set("Грешка")
                self.expression = ""

        else:
            if len(self.expression) >= self.max_len + 6:
                return
            if self.display_var.get() == "0" and char not in ".":
                self.expression = char
            else:
                self.expression += char
            self.display_var.set(self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
