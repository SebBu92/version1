# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 11.10.2025
# ---------------------------

# Allgemeine Imports
import os
import sys
import sqlite3

# Funktionen 

def get_db_path(): 
    if getattr(sys, 'frozen', False): 
        base_dir = os.path.dirname(os.path.abspath(sys.argv[0])) 
    else: 
        base_dir = os.path.dirname(os.path.abspath(__file__)) 
    return os.path.join(base_dir, "material.db")

def verbindung_aufbauen():
    return sqlite3.connect(get_db_path())

connection = verbindung_aufbauen()
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS werkstoff(
    werkstoff TEXT PRIMARY KEY)""")

cursor.execute(""" 
CREATE TABLE IF NOT EXISTS material(
    material_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    werkstoff TEXT, 
    dicke REAL,
    breite INTEGER,
    laenge INTEGER,
    bezeichnung TEXT,
    bestand INTEGER,
    vorgemerkt INTEGER,
    verfuegbar INTEGER,
    FOREIGN KEY (werkstoff) REFERENCES werkstoff(werkstoff)
)
""")
connection.close()

# ------------------------------ Insert Anweisungen ------------------------------

def insert_werkstoff(werkstoff):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO werkstoff (werkstoff)
    VALUES (?)""", (werkstoff,))
    connection.commit()
    connection.close()

def insert_material(werkstoff, dicke, breite, laenge, bezeichnung):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    INSERT INTO material 
    (werkstoff, dicke, breite, laenge, bezeichnung, bestand, vorgemerkt, verfuegbar) 
    VALUES (?, ?, ?, ?, ?, 0, 0, 0)""", 
    (werkstoff, dicke, breite, laenge, bezeichnung)
    )
    connection.commit()
    connection.close()

# ------------------------------- Get Anweisungen --------------------------------

def get_werkstoff():
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM werkstoff
    """)
    werkstoffe = cursor.fetchall()
    connection.close()
    return werkstoffe

def get_werkstoff_bezeichnung():
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT material_ID, werkstoff, bezeichnung FROM material
    """)
    werkstoff_bezeichnung = cursor.fetchall()
    connection.close()
    return werkstoff_bezeichnung

def get_materialdicke():
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT dicke FROM material
    """)
    materialdicke = cursor.fetchall()
    connection.close()
    return materialdicke

def get_material():
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM material
    """)
    material = cursor.fetchall()
    connection.close()
    return material

def get_material_filter_werkstoff_dicke(werkstoff, dicke):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM material
    WHERE werkstoff = ? AND dicke = ?""", (werkstoff, dicke))
    material_filter_werkstoff_dicke = cursor.fetchall()
    connection.close()
    return material_filter_werkstoff_dicke

def get_material_filter_werkstoff(werkstoff):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM material
    WHERE werkstoff = ?""", (werkstoff,))
    material_filter_werkstoff = cursor.fetchall()
    connection.close()
    return material_filter_werkstoff

def get_material_filter_dicke(dicke):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    SELECT * FROM material
    WHERE dicke = ?""", (dicke,))
    material_filter_dicke = cursor.fetchall()
    connection.close()
    return material_filter_dicke

# ------------------------------ Delete Anweisungen ------------------------------

def delete_material(material_ID):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    DELETE FROM material WHERE material_ID = ?""", (material_ID,))
    connection.commit()
    connection.close()

# ------------------------------ Update Anweisungen ------------------------------

def update_bestand_verfuegbar(stueckzahl, material_ID):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE material 
    SET bestand = bestand + ?, verfuegbar = verfuegbar + ? 
    WHERE material_ID = ?""", (stueckzahl, stueckzahl, material_ID,))
    connection.commit()
    connection.close()
    
def update_vorgemerkt_verfuegbar(stueckzahl, material_ID):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE material
    SET vorgemerkt = vorgemerkt + ?, verfuegbar = verfuegbar - ?
    WHERE material_ID = ?""", (stueckzahl, stueckzahl, material_ID))
    connection.commit()
    connection.close()

def update_bestand_vorgemerkt(stueckzahl, material_ID):
    connection = verbindung_aufbauen()
    cursor = connection.cursor()
    cursor.execute("""
    UPDATE material
    SET bestand = bestand - ?, vorgemerkt = vorgemerkt - ?
    WHERE material_ID = ?""", (stueckzahl, stueckzahl, material_ID))
    connection.commit()
    connection.close()