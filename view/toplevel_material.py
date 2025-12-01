# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 03.10.2025
# ---------------------------

# Allgemeine Imports
import tkinter as tk
from tkinter import ttk

# Funktionen

def materialfenster(
        root, 
        werkstoff_auslesen, 
        material_speichern, 
        werkstoff_bezeichnung_auslesen,
        material_loeschen
        ):
    fenster = tk.Toplevel(root)
    fenster.title("Material hinzufügen / löschen")
    fenster.geometry("900x320")
    fenster.minsize(900, 320)

    frame_left = ttk.Frame(fenster)
    frame_left.grid(row=0, column=0, pady=5)

    label_werkstoff = ttk.Label(frame_left, text="Werkstoff auswählen:")
    label_werkstoff.grid(row=0, column=0, pady=5)

    combobox_werkstoff = ttk.Combobox(frame_left, state="readonly")
    combobox_werkstoff.grid(row=0, column=1, pady=5)

    werkstoffwerte = werkstoff_auslesen()
    combobox_werkstoff_werte = []
    for wert in werkstoffwerte:
        combobox_werkstoff_werte.append(wert[0])
    combobox_werkstoff["values"] = combobox_werkstoff_werte

    label_dicke = ttk.Label(frame_left, text="Dicke eingeben:")
    label_dicke.grid(row=1, column=0, pady=5)

    entry_dicke = ttk.Entry(frame_left)
    entry_dicke.grid(row=1, column=1, pady=5)

    label_breite = ttk.Label(frame_left, text="Breite eingeben:")
    label_breite.grid(row=2, column=0, pady=5)

    entry_breite = ttk.Entry(frame_left)
    entry_breite.grid(row=2, column=1, pady=5)

    label_laenge = ttk.Label(frame_left, text="Länge eingeben:")
    label_laenge.grid(row=3, column=0, pady=5)

    entry_laenge = ttk.Entry(frame_left)
    entry_laenge.grid(row=3, column=1, pady=5)

    label_bezeichnung = ttk.Label(frame_left, text=("Bezeichnung eingeben: \n"
        "(Format: Ronde/Tafel DickexBreitexLänge)" ))
    label_bezeichnung.grid(row=4, column=0, pady=5)

    entry_bezeichnung = ttk.Entry(frame_left,)
    entry_bezeichnung.grid(row=4, column=1, pady=5)

    frame_right = ttk.Frame(fenster)
    frame_right.grid(row=0, column=1, sticky="nsew")

    tree_werkstoff_bezeichnung = ttk.Treeview(frame_right, 
                                columns=("Material_ID", "Werkstoff", "Bezeichnung"), 
                                show="headings", selectmode="browse")
    tree_werkstoff_bezeichnung.heading("Material_ID", text="Material_ID")
    tree_werkstoff_bezeichnung.column("Material_ID", width=70, anchor="center")
    tree_werkstoff_bezeichnung.heading("Werkstoff", text="Werkstoff")
    tree_werkstoff_bezeichnung.column("Werkstoff", width=100, anchor="center")
    tree_werkstoff_bezeichnung.heading("Bezeichnung", text="Bezeichnung")
    tree_werkstoff_bezeichnung.column("Bezeichnung", anchor="center")
    tree_werkstoff_bezeichnung.pack(fill="both", pady=10)

    def tree_aktualisieren():
        for wert in tree_werkstoff_bezeichnung.get_children():
            tree_werkstoff_bezeichnung.delete(wert)
        
        werkstoff_bezeichnung_werte = werkstoff_bezeichnung_auslesen()
        for wert in werkstoff_bezeichnung_werte:
            tree_werkstoff_bezeichnung.insert("", "end", values=wert)
    
    def eingabewerte_speichern_db():
        eingabe_werkstoff = combobox_werkstoff.get()
        eingabe_dicke = entry_dicke.get()
        eingabe_breite = entry_breite.get()
        eingabe_laenge = entry_laenge.get()
        eingabe_bezeichnung = entry_bezeichnung.get()
        material_speichern(eingabe_werkstoff, eingabe_dicke, 
                        eingabe_breite, eingabe_laenge, eingabe_bezeichnung)
        tree_aktualisieren()
        combobox_werkstoff.set("")
        entry_dicke.delete(0, tk.END)
        entry_breite.delete(0, tk.END)
        entry_laenge.delete(0, tk.END)
        entry_bezeichnung.delete(0, tk.END)

    def treeauswahl_loeschen_db():
        auswahl_tree_holen = tree_werkstoff_bezeichnung.selection()
        if auswahl_tree_holen:
            spaltenwerte = tree_werkstoff_bezeichnung.item(auswahl_tree_holen, 
                                                        "values")
            # Spaltenwerte= Tuple, daher [0] (material_ID) in Integer umwandeln
            material_ID = int(spaltenwerte[0])
            material_loeschen(material_ID)
            tree_aktualisieren()
        
    label_tree = ttk.Label(frame_right, text="Auswahl treffen!")
    label_tree.pack()

    def treeauswahl_anzeigen(event):
        if tree_werkstoff_bezeichnung.selection():
            werte = tree_werkstoff_bezeichnung.item(
                    tree_werkstoff_bezeichnung.selection(), "values")
            label_tree.config(text=f"Ausgewählt: {werte}")
        else:
            label_tree.config(text="Auswahl treffen!")

    tree_werkstoff_bezeichnung.bind("<<TreeviewSelect>>", treeauswahl_anzeigen)

    frame_bottom = ttk.Frame(fenster)
    frame_bottom.grid(row=1, columnspan=2)

    button_hinzufuegen = ttk.Button(
        frame_bottom, text="Hinzufügen", width=15, 
        command=eingabewerte_speichern_db)
    button_hinzufuegen.grid(row=0, column=0, padx=5)

    button_loeschen = ttk.Button(frame_bottom, text="Löschen", width=15,
                                command=treeauswahl_loeschen_db)
    button_loeschen.grid(row=0, column=1, padx=5)

    button_zurück = ttk.Button(frame_bottom, text="Zurück", command=fenster.destroy, 
                                width=15)
    button_zurück.grid(row=0, column=2, padx=5)

    label_autor = ttk.Label(fenster, text="Copyright by Sebastian Buchner")
    label_autor.grid(row=2, columnspan=2, pady=20)

    tree_aktualisieren()
    return fenster