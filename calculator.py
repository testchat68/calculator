#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Калкулатор за Linux Mint 22.2
с две памети (M1 и M2) + индикация на стойностите
Цветове от уиджета, подредени в стил 1962.
Дисплей на два етажа:
  горен ред — целият израз (по-дребен)
  долен ред — текущото число / резултат (едър, както преди)
Разредка през 3 разряда отдясно наляво.
Последният натиснат оператор (+ − × ÷ =) свети по-ярко
до следващ от същата група или до C.
"""
import tkinter as tk
from tkinter import font as tkfont
import math
import re

PINK      = "#EFAED0"   # бледо розово — горна лента и оператори + − × ÷ =
PINK_LIT  = "#FF6EB8"   # ярко розово — активен последно натиснат оператор
CREAM     = "#F7E8DF"   # крем — фон на прозореца и на клавиатурата
TEAL      = "#00c3d9"   # тъмен тийл — бутони памет M1 / M2
MEM1_ON   = "#1B5E20"   # тъмно зелено — +M1 и RM1 при ненулева памет
MEM2_ON   = "#0D47A1"   # тъмно синьо — +M2 и RM2 при ненулева памет
MAGENTA   = "#c70244"   # циклама — C, ⌫, ±
KEY_NUM   = "#4EB8B4"   # светъл тийл — цифри 0–9 и точка
KEY_SOFT  = "#F98F98"   # сьомга — √ и %
SCREEN_BG = "#1e1e1e"   # почти черно — фон на дисплея
DIGIT_FG  = "#7fff00"   # мента — цифри на долния ред на дисплея
WHITE     = "#FFFFFF"   # бяло — текст върху лентата и бутоните
HOVER     = "#00e5ff"   # циан — цвят при посочване на бутон
EXPR_FG   = "#7fff00"   # приглушено зелено — горен ред на дисплея (израз)

OP_GROUP = ("+", "−", "×", "÷", "=")


class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator 1962")
        self.root.resizable(False, False)
        self.root.configure(bg=CREAM)

        window_width = 400
        window_height = 580
        sw = root.winfo_screenwidth()
        sh = root.winfo_screenheight()
        self.root.geometry(
            f"{window_width}x{window_height}+{(sw-window_width)//2}+{(sh-window_height)//2}"
        )

        self.expression = ""
        self.display_var = tk.StringVar(value="0")
        self.max_len = 12
        self.max_digits = 12
        self.memory1 = 0.0
        self.memory2 = 0.0
        self.just_evaluated = False
        self.last_action = ""
        self.op_buttons = {}
        self.active_op = None

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
            bg=PINK, fg=WHITE, pady=6,
        ).pack()

        display_frame = tk.Frame(self.root, bg=SCREEN_BG, padx=8, pady=8)
        display_frame.pack(fill="x", padx=10, pady=(10, 8))

        try:
            expr_font = tkfont.Font(family="DS-Digital", size=14)
            display_font = tkfont.Font(family="DS-Digital", size=32)
        except tk.TclError:
            expr_font = tkfont.Font(family="Courier", size=11)
            display_font = tkfont.Font(family="Courier", size=24, weight="bold")

        self.expr_display = tk.Label(
            display_frame, text="", font=expr_font,
            bg=SCREEN_BG, fg=EXPR_FG, anchor="e",
            padx=4, pady=2,
        )
        self.expr_display.pack(fill="x")

        self.display = tk.Label(
            display_frame, text="0", font=display_font,
            bg=SCREEN_BG, fg=DIGIT_FG, anchor="e",
            padx=4, pady=6,
        )
        self.display.pack(fill="x")

        buttons_frame = tk.Frame(self.root, bg=CREAM)
        buttons_frame.pack(expand=True, fill="both", padx=8, pady=8)

        self.btn_font = tkfont.Font(family="Ubuntu", size=16, weight="bold")
        self.btn_font_small = tkfont.Font(family="Ubuntu", size=10, weight="bold")

        self.make_btn(buttons_frame, "C",   0, 0, MAGENTA, fg=WHITE)
        self.make_btn(buttons_frame, "⌫",   0, 1, MAGENTA, fg=WHITE)
        self.make_btn(buttons_frame, "√",   0, 2, KEY_SOFT, fg=WHITE)
        self.make_btn(buttons_frame, "÷",   0, 3, PINK,     fg=WHITE)
        self.btn_m1_add = self.make_btn(buttons_frame, "+M1", 0, 4, TEAL, fg=WHITE, small=True)

        self.make_btn(buttons_frame, "7",   1, 0, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "8",   1, 1, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "9",   1, 2, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "×",   1, 3, PINK,     fg=WHITE)
        self.btn_m1_rcl = self.make_btn(buttons_frame, "RM1", 1, 4, TEAL, fg=WHITE, small=True)

        self.make_btn(buttons_frame, "4",   2, 0, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "5",   2, 1, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "6",   2, 2, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "−",   2, 3, PINK,     fg=WHITE)
        self.btn_m2_add = self.make_btn(buttons_frame, "+M2", 2, 4, TEAL, fg=WHITE, small=True)

        self.make_btn(buttons_frame, "1",   3, 0, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "2",   3, 1, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "3",   3, 2, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "+",   3, 3, PINK,     fg=WHITE)
        self.btn_m2_rcl = self.make_btn(buttons_frame, "RM2", 3, 4, TEAL, fg=WHITE, small=True)

        self.make_btn(buttons_frame, "0",   4, 0, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, ".",   4, 1, KEY_NUM,  fg=WHITE)
        self.make_btn(buttons_frame, "%",   4, 2, KEY_SOFT, fg=WHITE)
        self.make_btn(buttons_frame, "=",   4, 3, PINK,     fg=WHITE)
        self.make_btn(buttons_frame, "±",   4, 4, MAGENTA, fg=WHITE)

        for i in range(5):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)

    def rest_color(self, btn):
        if self.active_op is not None and self.op_buttons.get(self.active_op) is btn:
            return PINK_LIT
        return btn._base_color

    def make_btn(self, parent, text, row, col, color, small=False, fg="white"):
        font = self.btn_font_small if small else self.btn_font
        btn = tk.Button(
            parent, text=text, font=font, bg=color, fg=fg,
            activebackground=HOVER, activeforeground=WHITE,
            relief="raised", bd=2,
            command=lambda t=text: self.on_button_click(t),
        )
        btn._base_color = color
        btn.grid(row=row, column=col, sticky="nsew", padx=3, pady=3, ipady=10)
        btn.bind("<Enter>", lambda e, b=btn: b.config(bg=HOVER))
        btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.rest_color(b)))
        if text in OP_GROUP:
            self.op_buttons[text] = btn
        return btn

    def set_active_op(self, char):
        self.active_op = char if char in OP_GROUP else None
        for name, btn in self.op_buttons.items():
            if name == self.active_op:
                btn.config(bg=PINK_LIT, relief="sunken")
            else:
                btn.config(bg=btn._base_color, relief="raised")

    def clear_active_op(self):
        self.active_op = None
        for btn in self.op_buttons.values():
            btn.config(bg=btn._base_color, relief="raised")

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

    def last_number(self, text):
        if not text or text in ("Грешка", "Error"):
            return text or "0"
        parts = re.split(r"([+−×÷])", text)
        for p in reversed(parts):
            if p not in ("", "+", "−", "×", "÷"):
                return p
        return "0"

    def current_operand_digits(self):
        if self.expression and self.expression[-1] in "+−×÷":
            return 0
        token = self.last_number(self.expression)
        return sum(ch.isdigit() for ch in token)

    def last_binary_action(self, expr):
        parts = [p for p in re.split(r"([+−×÷])", expr) if p != ""]
        if len(parts) < 3:
            return expr
        return "".join(parts[-3:])

    def apply_percent(self):
        expr = self.expression
        if expr and expr[-1] in "+−×÷":
            expr = expr[:-1]
        if not expr:
            return None
        parts = [p for p in re.split(r"([+−×÷])", expr) if p != ""]
        if len(parts) >= 3 and parts[-2] in "+−×÷":
            op = parts[-2]
            b = float(parts[-1].replace("−", "-"))
            left = "".join(parts[:-2]).replace("×", "*").replace("÷", "/").replace("−", "-")
            a = float(eval(left)) if left else 0.0
            pct = a * b / 100.0
            if op == "+":
                result = a + pct
            elif op == "−":
                result = a - pct
            elif op == "×":
                result = a * pct
            else:
                if pct == 0:
                    raise ZeroDivisionError
                result = a / pct
            action = f"{self.format_result(a)}{op}{self.format_result(b)}%"
            return result, action
        value = float(eval(expr.replace("×", "*").replace("÷", "/").replace("−", "-")))
        return value / 100.0, f"{self.format_result(value)}%"

    def refresh_display(self):
        raw = self.display_var.get()
        if raw in ("Грешка", "Error"):
            self.expr_display.config(text="")
            self.display.config(text=raw)
            return

        if self.just_evaluated:
            upper = self.format_for_screen(self.last_action) if self.last_action else ""
            self.expr_display.config(text=upper)
            self.display.config(text=self.format_for_screen(raw))
            return

        expr = self.expression
        if expr and expr[-1] in "+−×÷":
            upper = self.format_for_screen(expr)
            lower = self.format_for_screen(self.last_number(expr[:-1])) if expr[:-1] else "0"
        else:
            upper = self.format_for_screen(expr) if expr else ""
            lower = self.format_for_screen(self.last_number(expr) if expr else "0")

        if upper in ("0", ""):
            upper = ""
        self.expr_display.config(text=upper)
        self.display.config(text=lower)

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
        c1 = MEM1_ON if self.memory1 != 0 else TEAL
        c2 = MEM2_ON if self.memory2 != 0 else TEAL
        self.btn_m1_add._base_color = c1
        self.btn_m1_rcl._base_color = c1
        self.btn_m2_add._base_color = c2
        self.btn_m2_rcl._base_color = c2
        self.btn_m1_add.config(text=f"+M1\n{m1}", bg=c1)
        self.btn_m1_rcl.config(text=f"RM1\n{m1}", bg=c1)
        self.btn_m2_add.config(text=f"+M2\n{m2}", bg=c2)
        self.btn_m2_rcl.config(text=f"RM2\n{m2}", bg=c2)

    def get_current_value(self):
        try:
            if not self.expression:
                return 0.0
            expr = self.expression.replace("×", "*").replace("÷", "/").replace("−", "-")
            if expr[-1:] in "+-*/":
                expr = expr[:-1]
            if not expr:
                return 0.0
            return float(eval(expr))
        except Exception:
            return 0.0

    def format_result(self, value):
        try:
            v = float(value)
        except Exception:
            return str(value)
        if not math.isfinite(v):
            return "Грешка"
        limit = 10 ** self.max_digits
        if abs(v) >= limit or (v != 0 and abs(v) < 10 ** -(self.max_digits - 1)):
            return f"{v:.6e}".replace("e+0", "e+").replace("e-0", "e-")
        if abs(v - round(v)) < 1e-12:
            iv = int(round(v))
            if len(str(abs(iv))) <= self.max_digits:
                return str(iv)
        s = f"{v:.12g}"
        if s.endswith(".0"):
            s = s[:-2]
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

        if char in OP_GROUP:
            self.set_active_op(char)
        elif char == "C":
            self.clear_active_op()

        if char == "C":
            self.expression = ""
            self.last_action = ""
            self.just_evaluated = False
            self.display_var.set("0")
        elif char == "⌫":
            self.just_evaluated = False
            self.last_action = ""
            self.expression = self.expression[:-1]
            self.display_var.set(self.expression if self.expression else "0")
        elif char == "√":
            try:
                value = self.get_current_value()
                if value < 0:
                    self.display_var.set("Грешка")
                    self.expression = ""
                    self.last_action = ""
                    self.just_evaluated = False
                    return
                src = self.format_result(value)
                result = math.sqrt(value)
                shown = self.format_result(result)
                self.last_action = f"√{src}"
                self.expression = shown
                self.just_evaluated = True
                self.display_var.set(shown)
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
                self.last_action = ""
                self.just_evaluated = False
        elif char == "%":
            try:
                applied = self.apply_percent()
                if applied is None:
                    return
                result, action = applied
                shown = self.format_result(result)
                self.last_action = action
                self.expression = shown
                self.just_evaluated = True
                self.display_var.set(shown)
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
                self.last_action = ""
                self.just_evaluated = False
        elif char == "±":
            try:
                value = -self.get_current_value()
                self.expression = self.format_result(value)
                self.just_evaluated = True
                self.display_var.set(self.expression)
            except Exception:
                pass
        elif char == "+M1":
            self.memory1 += self.get_current_value()
            self.update_memory_buttons()
        elif char == "RM1":
            mem_str = self.format_result(self.memory1)
            if self.just_evaluated or self.expression == "" or self.display_var.get() == "0":
                self.expression = mem_str
            else:
                last = self.expression[-1] if self.expression else ""
                if last in "+−×÷":
                    self.expression += mem_str
                else:
                    self.expression = mem_str
            self.just_evaluated = False
            self.display_var.set(self.expression)
        elif char == "+M2":
            self.memory2 += self.get_current_value()
            self.update_memory_buttons()
        elif char == "RM2":
            mem_str = self.format_result(self.memory2)
            if self.just_evaluated or self.expression == "" or self.display_var.get() == "0":
                self.expression = mem_str
            else:
                last = self.expression[-1] if self.expression else ""
                if last in "+−×÷":
                    self.expression += mem_str
                else:
                    self.expression = mem_str
            self.just_evaluated = False
            self.display_var.set(self.expression)
        elif char in ("+", "×") and self.expression.endswith(char):
            try:
                value = self.get_current_value()
                result = value + value if char == "+" else value * value
                src = self.format_result(value)
                shown = self.format_result(result)
                self.last_action = f"{src}{char}{src}"
                self.expression = shown
                self.just_evaluated = True
                self.display_var.set(shown)
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
                self.last_action = ""
                self.just_evaluated = False
        elif char == "=":
            try:
                raw_expr = self.expression
                if raw_expr and raw_expr[-1] in "+−×÷":
                    raw_expr = raw_expr[:-1]
                expr = raw_expr.replace("×", "*").replace("÷", "/").replace("−", "-")
                result = eval(expr)
                shown = self.format_result(result)
                self.last_action = self.last_binary_action(raw_expr)
                self.just_evaluated = True
                self.expression = shown
                self.display_var.set(shown)
            except Exception:
                self.display_var.set("Грешка")
                self.expression = ""
                self.last_action = ""
                self.just_evaluated = False
        else:
            if self.just_evaluated and char not in "+−×÷":
                self.expression = ""
                self.last_action = ""
            self.just_evaluated = False
            if char.isdigit() and self.current_operand_digits() >= self.max_digits:
                return
            if (self.display_var.get() == "0" and char not in "." and char not in "+−×÷"
                    and self.expression in ("", "0")):
                self.expression = char
            else:
                self.expression += char
            self.display_var.set(self.expression)


if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
