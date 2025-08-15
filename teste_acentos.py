# -*- coding: utf-8 -*-
"""
Teste simples de acentos em Tkinter
"""

import tkinter as tk
from tkinter import ttk

def test_accent_input():
    root = tk.Tk()
    root.title("Teste de Acentos")
    root.geometry("400x200")
    
    # Frame principal
    frame = ttk.Frame(root, padding="20")
    frame.pack(fill=tk.BOTH, expand=True)
    
    # Label
    ttk.Label(frame, text="Digite um nome com acentos:").pack(pady=10)
    
    # Entry simples
    nome_var = tk.StringVar()
    entry = ttk.Entry(frame, textvariable=nome_var, width=40)
    entry.pack(pady=10)
    entry.focus_set()
    
    # Botão para mostrar o que foi digitado
    def mostrar_resultado():
        texto = nome_var.get()
        print(f"Texto digitado: '{texto}'")
        print(f"Caracteres: {[c for c in texto]}")
        result_label.config(text=f"Resultado: {texto}")
    
    ttk.Button(frame, text="Mostrar Resultado", command=mostrar_resultado).pack(pady=10)
    
    # Label resultado
    result_label = ttk.Label(frame, text="")
    result_label.pack(pady=10)
    
    # Instruções
    instructions = ttk.Label(frame, text="Tente digitar: José, María, João, Conceição")
    instructions.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_accent_input()