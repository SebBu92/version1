# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 11.10.2025
# ---------------------------

# Allgemeine Imports
import sys
import os
import csv

# Eigene Module Importieren
from view.hauptfenster import hauptfenster_erzeugen
from model.lagerverwaltung_db import insert_werkstoff
from model.lagerverwaltung_db import get_werkstoff
from model.lagerverwaltung_db import insert_material
from model.lagerverwaltung_db import get_werkstoff_bezeichnung
from model.lagerverwaltung_db import get_materialdicke
from model.lagerverwaltung_db import get_material
from model.lagerverwaltung_db import delete_material
from model.lagerverwaltung_db import update_bestand_verfuegbar
from model.lagerverwaltung_db import update_vorgemerkt_verfuegbar
from model.lagerverwaltung_db import update_bestand_vorgemerkt
from model.lagerverwaltung_db import get_material_filter_werkstoff_dicke
from model.lagerverwaltung_db import get_material_filter_werkstoff
from model.lagerverwaltung_db import get_material_filter_dicke

# Funktionen

def hole_basis_verzeichnis(): 
    """Gibt den Ordner zurück, in dem die EXE bzw. main.app liegt.""" 
    if getattr(sys, 'frozen', False): 
        # PyInstaller (EXE oder APP) 
        return os.path.dirname(os.path.abspath(sys.argv[0])) 
    else: 
        # Normaler Python-Start 
        return os.path.dirname(os.path.abspath(__file__))
    
BASIS_VERZEICHNIS = hole_basis_verzeichnis()

# -------------------------------- CSV Schreiben --------------------------------

def export_materialbestand_csv(dateiname="materialbestand_export.csv"): 
    spalten = ["Material_ID", "Werkstoff", "Dicke", "Breite", "Länge", 
                "Bezeichnung", "Bestand", "Vorgemerkt", "Verfügbar"]
    daten = get_material() 
    pfad = os.path.join(BASIS_VERZEICHNIS, dateiname) 
    
    with open(pfad, "w", newline="", encoding="utf-8") as csv_file: 
        writer = csv.writer(csv_file) 
        writer.writerow(spalten) 
        writer.writerows(daten)

# ------------------------------- Daten Speichern -------------------------------

def werkstoff_speichern(werkstoff):
    if len(werkstoff) > 3:
        return insert_werkstoff(werkstoff)

def material_speichern(werkstoff, dicke, breite, laenge, bezeichnung):
    if (
        len(werkstoff) > 0 and 
        len(dicke) > 0 and 
        len(breite) > 0 and 
        len(laenge) > 0 and 
        len(bezeichnung)> 0):
        try:
            dicke = float(dicke.replace(",", "."))
            breite = int(breite)
            laenge = int(laenge)
        except ValueError:
            return
        return insert_material(werkstoff, dicke, breite, laenge, bezeichnung)

# ------------------------------- Daten abfragen --------------------------------

def werkstoff_auslesen():
    return get_werkstoff()

def werkstoff_bezeichnung_auslesen():
    return get_werkstoff_bezeichnung()

def dicke_auslesen():
    return get_materialdicke()

def material_auslesen(werkstoff, dicke):
    if werkstoff and dicke:
        return get_material_filter_werkstoff_dicke(werkstoff, dicke)
    elif dicke:
        return get_material_filter_dicke(dicke)
    elif werkstoff:
        return get_material_filter_werkstoff(werkstoff)
    else:
        return get_material()

# ------------------------------- Daten löschen ---------------------------------

def material_loeschen(material_ID):
    return delete_material(material_ID)

# ---------------------------- Daten aktualisieren ------------------------------

def bestand_verfuegbar_aktualisieren(stueckzahl, material_ID):
    return update_bestand_verfuegbar(stueckzahl, material_ID)

def vorgemerkt_verfuegbar_aktualisieren(stueckzahl, material_ID):
    return update_vorgemerkt_verfuegbar(stueckzahl, material_ID)

def bestand_vorgemerkt_aktualisieren(stueckzahl, material_ID):
    return update_bestand_vorgemerkt(stueckzahl, material_ID)

# --------------------------------- Callbacks -----------------------------------

callbacks = {
    "werkstoff_speichern": werkstoff_speichern,
    "werkstoff_auslesen": werkstoff_auslesen,
    "material_speichern": material_speichern,
    "werkstoff_bezeichnung_auslesen": werkstoff_bezeichnung_auslesen,
    "dicke_auslesen": dicke_auslesen,
    "material_auslesen": material_auslesen,
    "material_loeschen": material_loeschen,
    "bestand_verfuegbar_aktualisieren": bestand_verfuegbar_aktualisieren,
    "vorgemerkt_verfuegbar_aktualisieren": vorgemerkt_verfuegbar_aktualisieren,
    "bestand_vorgemerkt_aktualisieren": bestand_vorgemerkt_aktualisieren,
    "export_materialbestand_csv": export_materialbestand_csv
}

if __name__ == "__main__":
    root = hauptfenster_erzeugen(callbacks)
    root.mainloop()