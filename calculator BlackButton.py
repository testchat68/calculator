#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Калкулатор за Linux Mint 22.2
с две памети (M1 и M2) + индикация на стойностите
Цветове от уиджета, подредени в стил 1962.
Дисплей: шрифт/размер/цвят — без промяна.
Разредка през 3 разряда отдясно наляво.
"""
import tkinter as tk
from tkinter import font as tkfont
import math
import re


PINK      = "#F4A8C0"
CREAM     = "#F4E8C8"
TEAL      = "#4EB8B4"
MUSTARD   = "#E0C04A"
NAVY      = "#2C3A5A"
KEY_NUM   = "#D9C878"
KEY_DIM   = "#C9B56A"
SCREEN_BG = "#1e1e1e"
DIGIT_FG  = "#7FE8B0"


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator 1962")
        self.root.resizable(False, False)
        self.root.configure(bg=CREAM)

        window_width = 400
        window_height = 540
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.root.geometry(f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}")

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.max_len = 14
        self.memory1 = 0.0
        self.memory2 = 0.0

        self.create_widgets()
        self.update_memory_buttons()
        self.display_var.trace_add("write", lambda *_: self.refresh_display())
        self.refresh_display()

    def create_widgets(self):
        plate = tk.Frame(self.root, bg=PINK)
        plate.pack(fill="x")
        tk.Label(
            plate,
            text="·  CALCULATOR 1962  ·",
            font=tkfont.Font(family="Times", size=12, weight="bold"),
            bg=PINK, fg=NAVY, pady=6,
        ).pack()

        display_frame = tk.Frame(self.root, bg=CREAM)
        display_frame.pack(fill="x", padx=10, pady=(10, 8))

        try:
            display_font = tkfont.Font(family="DS-Digital", size=28)
        except tk.TclError:
            display_font = tkfont.Font(family="Courier", size=24, weight="bold")

        self.display = tk.Label(
            display_frame, text="0", font=display_font,
            bg=SCREEN_BG, fg=DIGIT_FG, anchor="e",
            padx=12, pady=18, relief="flat",
        )
        self.display.pack(fill="x")

        buttons_frame = tk.Frame(self.root, bg=CREAM)
        buttons_frame.pack(expand=True, fill="both", padx=8, pady=8)

        self.btn_font = tkfont.Font(family="Ubuntu", size=16, weight="bold")
        self.btn_font_small = tkfont.Font(family="Ubuntu", size=10, weight="bold")

        self.make_btn(buttons_frame, "C",   0, 0, PINK,     fg=NAVY)
        self.make_btn(buttons_frame, "⌫",   0, 1, PINK,     fg=NAVY)
        self.make_btn(buttons_frame, "√",   0, 2, KEY_DIM,  fg=NAVY)
        self.make_btn(buttons_frame, "÷",   0, 3, MUSTARD,  fg=NAVY)
        self.btn_m1_add = self.make_btn(buttons_frame, "+M1", 0, 4, TEAL, small=True)

        self.make_btn(buttons_frame, "7",   1, 0, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "8",   1, 1, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "9",   1, 2, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "×",   1, 3, MUSTARD,  fg=NAVY)
        self.btn_m1_rcl = self.make_btn(buttons_frame, "RM1", 1, 4, TEAL, small=True)

        self.make_btn(buttons_frame, "4",   2, 0, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "5",   2, 1, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "6",   2, 2, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "−",   2, 3, MUSTARD,  fg=NAVY)
        self.btn_m2_add = self.make_btn(buttons_frame, "+M2", 2, 4, TEAL, small=True)

        self.make_btn(buttons_frame, "1",   3, 0, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "2",   3, 1, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "3",   3, 2, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "+",   3, 3, MUSTARD,  fg=NAVY)
        self.btn_m2_rcl = self.make_btn(buttons_frame, "RM2", 3, 4, TEAL, small=True)

        self.make_btn(buttons_frame, "0",   4, 0, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, ".",   4, 1, KEY_NUM,  fg=NAVY)
        self.make_btn(buttons_frame, "%",   4, 2, KEY_DIM,  fg=NAVY)
        self.make_btn(buttons_frame, "=",   4, 3, MUSTARD,  fg=NAVY)
        self.make_btn(buttons_frame, "±",   4, 4, PINK,     fg=NAVY)

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)

    def make_btn(self, parent, text, row, col, color, small=False, fg="white"):
        font = self.btn_font_small if small else self.btn_font
        btn = tk.Button(
            parent, text=text, font=font, bg=color, fg=fg,
            activebackground="#ffffff", activeforeground=NAVY,
            relief="raised", bd=2,
            command=lambda t=text: self.on_button_click(t),
        )
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3, ipady=10)
        return btn

    def group_number(self, token):
        if token in ("Грешка", "Error"):
            return token
        sign = ""
        if token[:1] in "-−":
            sign, token = token[0], token[1:]
        if "." in token:
            body, frac = token.split(".", 1)
            frac = "." + frac
        else:
            body, frac = token, ""
        chunks = []
        while len(body) > 3:
            chunks.append(body[-3:])
            body = body[:-3]
        if body:
            chunks.append(body)
        return sign + "\u2004".join(reversed(chunks)) + frac

    def format_for_screen(self, text):
        if not text:
            return "0"
        if text in ("Грешка", "Error"):
            return text
        parts = re.split(r"([+−×÷])", text)
        out = []
        for p in parts:
            if p in "+−×÷" or p == "":
                out.append(p)
            else:
                out.append(self.group_number(p))
        return "".join(out)

    def refresh_display(self):
        self.display.config(text=self.format_for_screen(self.display_var.get()))

    def short_mem(self, value):
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value)
        if len(s) > 7:
            try:
                s = f"{float(value):.2e}"
            except Exception:
                s = s[:7]
        return s

    def update_memory_buttons(self):
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
        except Exception:
            return 0.0

    def format_result(self, value):
        if isinstance(value, float) and value.is_integer():
            value = int(value)
        s = str(value)
        if len(s) > self.max_len:
            try:
                s = f"{float(value):.6e}"
            except Exception:
                s = s[:self.max_len]
        return s

    def on_button_click(self, char):
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
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
        elif char == "%":
            try:
                value = self.get_current_value() / 100
                self.expression = self.format_result(value)
                self.display_var.set(self.expression)
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
        elif char == "±":
            try:
                value = -self.get_current_value()
                self.expression = self.format_result(value)
                self.display_var.set(self.expression)
            except Exception:
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
            except Exception:
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
