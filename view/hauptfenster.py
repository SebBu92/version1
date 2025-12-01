# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 11.10.2025
# ---------------------------

# Allgemeine Imports
import tkinter as tk
from tkinter import ttk

# Eigene Module Importieren
from .toplevel_werkstoff import werkstofffenster
from .toplevel_material import materialfenster
from .toplevel_buchungen import buchungsfenster

def hauptfenster_erzeugen(callbacks):
    root = tk.Tk()
    root.title("Lagerverwaltung")
    root.geometry("520x250")
    root.minsize(520, 250)

    button_bestand = ttk.Button(root, text="Bestand", width=20,
                                command=lambda:callbacks["export_materialbestand_csv"]())
    button_bestand.grid(row=5, column=0, padx=20, pady=20)

    button_werkstoffliste = ttk.Button(root, text="Werkstoffliste", width=20,
                                        command=lambda:werkstofffenster(
                                            root, 
                                            callbacks["werkstoff_speichern"], 
                                            callbacks["werkstoff_auslesen"]))
    button_werkstoffliste.grid(row=5, column=1, padx=20, pady=20)

    button_hinzufuegen_loeschen = ttk.Button(root, 
                                            text="Material hinzufügen/Löschen", 
                                            width=20, 
                                            command=lambda:materialfenster(
                                                root,
                                                callbacks["werkstoff_auslesen"],
                                                callbacks["material_speichern"],
                                                callbacks["werkstoff_bezeichnung_auslesen"],
                                                callbacks["material_loeschen"]))
    button_hinzufuegen_loeschen.grid(row=10, column=0, padx=20, pady=20)

    button_materialbuchung = ttk.Button(root, text="Materialbuchung", width=20,
                                        command=lambda:buchungsfenster(
                                            root,
                                            callbacks["werkstoff_auslesen"],
                                            callbacks["dicke_auslesen"],
                                            callbacks["material_auslesen"],
                                            callbacks["bestand_verfuegbar_aktualisieren"],
                                            callbacks["vorgemerkt_verfuegbar_aktualisieren"],
                                            callbacks["bestand_vorgemerkt_aktualisieren"],))
    button_materialbuchung.grid(row=10, column=1, padx=20, pady=20)

    button_beenden = ttk.Button(root, text="Beenden", command=root.destroy, width=20)
    button_beenden.grid(row=15, column=1, padx=20, pady=20)

    label_autor = ttk.Label(root, text="Copyright by Sebastian Buchner")
    label_autor.grid(row=20, column=0, columnspan=2)

    return root