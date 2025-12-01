# Sebastian Buchner 
# Software zur Lagerverwaltung
# Version 1.0 vom 11.10.2025
# ---------------------------

# Dummy-Implementierung von insert_material für den Test
def insert_material(werkstoff, dicke, breite, laenge, bezeichnung):
    # Wir geben einfach die Werte zurück, um sie zu prüfen
    return werkstoff, dicke, breite, laenge, bezeichnung

# Funktion, die wir testen
def material_speichern(werkstoff, dicke, breite, laenge, bezeichnung):
    if (
        len(werkstoff) > 0 and 
        len(dicke) > 0 and 
        len(breite) > 0 and 
        len(laenge) > 0 and 
        len(bezeichnung) > 0):
        try:
            dicke = float(dicke.replace(",", "."))
            breite = int(breite)
            laenge = int(laenge)
        except ValueError:
            return
        return insert_material(werkstoff, dicke, breite, laenge, bezeichnung)

# --- Tests ---
# Test 1: normale Eingaben
def test_normal_input():
    result = material_speichern("Stahl", "1,5", "100", "200", "Platte")
    assert result[0] == "Stahl", "Werkstoff sollte 'Stahl' sein"
    assert result[1] == 1.5, "Dicke sollte 1.5 sein"
    assert result[2] == 100, "Breite sollte 100 sein"
    assert result[3] == 200, "Länge sollte 200 sein"
    assert result[4] == "Platte", "Bezeichnung sollte 'Platte' sein"

# Test 2: leere Felder => None
def test_empty_field():
    assert material_speichern("", "1,5", "100", "200", "Platte") is None
    assert material_speichern("Stahl", "", "100", "200", "Platte") is None
    assert material_speichern("Stahl", "1,5", "", "200", "Platte") is None
    assert material_speichern("Stahl", "1,5", "100", "", "Platte") is None
    assert material_speichern("Stahl", "1,5", "100", "200", "") is None

# Test 3: ungültige Zahlen => None
def test_invalid_numbers():
    assert material_speichern("Stahl", "abc", "100", "200", "Platte") is None
    assert material_speichern("Stahl", "1,5", "x", "200", "Platte") is None
    assert material_speichern("Stahl", "1,5", "100", "y", "Platte") is None


# cd "/Users/seb/Library/Mobile Documents/com~apple~CloudDocs/Coden/IHK Software Developer/lagerverwaltung/version1"
# pytest test_material_speichern.py

