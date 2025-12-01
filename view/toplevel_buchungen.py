# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 11.10.2025
# ---------------------------

# Allgemeine Imports
import tkinter as tk
from tkinter import ttk

# Funktionen

def buchungsfenster(
        root, 
        werkstoff_auslesen, 
        dicke_auslesen, 
        material_auslesen, 
        bestand_verfuegbar_aktualisieren,
        vorgemerkt_verfuegbar_aktualisieren,
        bestand_vorgemerkt_aktualisieren):
    fenster = tk.Toplevel(root)
    fenster.title("Materialbuchungen")
    fenster.geometry("1000x430")
    fenster.minsize(1000, 430)

    frame_top = ttk.Frame(fenster)
    frame_top.grid(row=0, column=0, pady=5)

    label_werkstoff = ttk.Label(frame_top, text="Werkstoff auswählen:")
    label_werkstoff.grid(row=0, column=0, pady=5, padx=10)

    combobox_werkstoff = ttk.Combobox(frame_top, state="readonly")
    combobox_werkstoff.grid(row=1, column=0, pady=5, padx=10)

    werkstoffwerte = werkstoff_auslesen()
    werkstoff_werte = [""]
    for wert in werkstoffwerte:
        werkstoff_werte.append(wert[0])
    combobox_werkstoff["values"] = werkstoff_werte

    label_dicke = ttk.Label(frame_top, text="Dicke auswählen:")
    label_dicke.grid(row=0, column=1, pady=5, padx=10)

    combobox_dicke = ttk.Combobox(frame_top, state="readonly")
    combobox_dicke.grid(row=1, column=1, pady=5, padx=10)

    materialdicke_werte = dicke_auslesen()
    werte_materialdicke = [""]
    for wert in materialdicke_werte:
        werte_materialdicke.append(wert[0])
    combobox_dicke["values"] = werte_materialdicke

    frame_center = ttk.Frame(fenster)
    frame_center.grid(row=1, column=0)

    tree_columns = ["Material_ID", "Werkstoff", "Dicke", "Breite", "Länge", 
                    "Bezeichnung", "Bestand", "Vorgemerkt", "Verfügbar"]

    tree_material = ttk.Treeview(frame_center, columns=tree_columns, show="headings",
                                selectmode="browse")
    for col in tree_columns:
        tree_material.heading(col, text=col)
        tree_material.column(col, width=100, anchor="center")
        tree_material.pack(fill="both", pady=10)
    tree_material.column("Bezeichnung", width=200)

    def tree_aktualisieren(event):
        auswahl_werkstoff = combobox_werkstoff.get()
        auswahl_dicke = combobox_dicke.get()

        for wert in tree_material.get_children():
            tree_material.delete(wert)

        material_werte = material_auslesen(auswahl_werkstoff, auswahl_dicke)

        for wert in material_werte:
            tree_material.insert("", "end", values=wert)

    def zubuchen_speichern_db():
        eingabe_stueckzahl = entry_stueckzahl.get()
        auswahl_tree_holen = tree_material.selection()
        if auswahl_tree_holen:
            spaltenwerte = tree_material.item(auswahl_tree_holen, "values")
            material_ID = int(spaltenwerte[0])
        bestand_verfuegbar_aktualisieren(eingabe_stueckzahl, material_ID)
        tree_aktualisieren(event=tree_aktualisieren)
    
    def vormerken_speichern_db():
        eingabe_stueckzahl = entry_stueckzahl.get()
        auswahl_tree_holen = tree_material.selection()
        if auswahl_tree_holen:
            spaltenwerte = tree_material.item(auswahl_tree_holen, "values")
            material_ID = int(spaltenwerte[0])
        vorgemerkt_verfuegbar_aktualisieren(eingabe_stueckzahl, material_ID)
        tree_aktualisieren(event=tree_aktualisieren)

    def abbuchen_speichern_db():
        eingabe_stueckzahl = entry_stueckzahl.get()
        auswahl_tree_holen = tree_material.selection()
        if auswahl_tree_holen:
            spaltenwerte = tree_material.item(auswahl_tree_holen, "values")
            material_ID = int(spaltenwerte[0])
        bestand_vorgemerkt_aktualisieren(eingabe_stueckzahl, material_ID)
        tree_aktualisieren(event=tree_aktualisieren)

    frame_center_bottom = ttk.Frame(fenster)
    frame_center_bottom.grid(row=2, column=0)

    label_stueckzahl = ttk.Label(frame_center_bottom, text="Stückzahl eingeben:")
    label_stueckzahl.pack(padx=5, pady=10, side="left", anchor="center")

    entry_stueckzahl = ttk.Entry(frame_center_bottom, width=10)
    entry_stueckzahl.pack(padx=5, pady=10, side="left", anchor="center")

    label_tree = ttk.Label(frame_center_bottom, text="Auswahl treffen!")
    label_tree.pack(padx=40, pady=10, side="left", anchor="center")

    def treeauswahl_anzeigen(event):
        if tree_material.selection():
            werte = tree_material.item(tree_material.selection(), "values")
            label_tree.config(text=f"Ausgewählt: {werte[1], werte[5]}")
        else:
            label_tree.config(text="Auswahl treffen!")

    frame_bottom = ttk.Frame(fenster)
    frame_bottom.grid(row=3, columnspan=2)

    button_zubuchen = ttk.Button(frame_bottom, text="Zubuchen", width=15, 
                                command=zubuchen_speichern_db)
    button_zubuchen.grid(row=0, column=0, padx=5)

    button_vormerken = ttk.Button(frame_bottom, text="Vormerken", width=15,
                                command=vormerken_speichern_db)
    button_vormerken.grid(row=0, column=1, padx=5)

    button_abbuchen = ttk.Button(frame_bottom, text="Abbuchen", width=15,
                                command=abbuchen_speichern_db)
    button_abbuchen.grid(row=0, column=2)

    button_zurück = ttk.Button(frame_bottom, text="Zurück", width=15,
                                command=fenster.destroy)
    button_zurück.grid(row=0, column=3, padx=5)

    label_autor = ttk.Label(fenster, text="Copyright by Sebastian Buchner")
    label_autor.grid(row=4, columnspan=3, pady=20)

    tree_material.bind("<<TreeviewSelect>>", treeauswahl_anzeigen)
    combobox_werkstoff.bind("<<ComboboxSelected>>", tree_aktualisieren)
    combobox_dicke.bind("<<ComboboxSelected>>", tree_aktualisieren)

    tree_aktualisieren(event=tree_aktualisieren)
    return fenster