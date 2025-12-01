# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 03.10.2025
# ---------------------------

# Allgemeine Imports
import tkinter as tk
from tkinter import ttk

# Funktionen
    
def werkstofffenster(root, werkstoff_speichern, werkstoff_auslesen):
    fenster = tk.Toplevel(root)
    fenster.title("Werkstoffliste")
    fenster.geometry("420x310")
    fenster.minsize(420, 310)

    frame_left = ttk.Frame(fenster)
    frame_left.grid(row=0, column=0)

    label_werkstoff = ttk.Label(frame_left, text="Werkstoff eingeben:")
    label_werkstoff.pack(padx=5)

    entry_werkstoff = ttk.Entry(frame_left)
    entry_werkstoff.pack(padx=5)

    frame_right = ttk.Frame(fenster)
    frame_right.grid(row=0, column=1, sticky="nsew")

    tree_werkstoff = ttk.Treeview(frame_right, columns=("Werkstoff"), show="headings")
    tree_werkstoff.heading("Werkstoff", text="Werkstoff")
    tree_werkstoff.pack(fill="both", pady=10)
    
    def tree_aktualisieren():
        for wert in tree_werkstoff.get_children():
            tree_werkstoff.delete(wert)

        werkstoffwerte = werkstoff_auslesen()
        for wert in werkstoffwerte:
            tree_werkstoff.insert("", "end", values=wert)
    
    def eingabewert_speichern():
        werkstoff = entry_werkstoff.get()
        werkstoff_speichern(werkstoff)
        tree_aktualisieren()
        entry_werkstoff.delete(0, tk.END)

    frame_bottom = ttk.Frame(fenster)
    frame_bottom.grid(row=1, columnspan=2)

    button_hinzufuegen = ttk.Button(
        frame_bottom, text="Hinzufügen", width=15, 
        command=eingabewert_speichern
        )
    button_hinzufuegen.grid(row=0, column=0, padx=5)

    button_zurück = ttk.Button(frame_bottom, text="Zurück", command=fenster.destroy, width=15)
    button_zurück.grid(row=0, column=1, padx=5)

    label_autor = ttk.Label(fenster, text="Copyright by Sebastian Buchner")
    label_autor.grid(row=2, columnspan=2, pady=20)

    tree_aktualisieren()
    return fenster