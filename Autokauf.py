import pandas as pd
import datetime

# CSV-Dateien laden
autoData_df = pd.read_csv('autoData.csv', delimiter=';', decimal=',')
autoKosten_df = pd.read_csv('jahrlicheKosten.csv', delimiter=';', decimal=',')
WertverlustImJahr_df = pd.read_csv('wertverlust.csv', delimiter=';', decimal=',')

# Aktuelles Jahr abrufen
heutiges_jahr = datetime.datetime.now().year

#Drucke die ersten paar Zeilen zur Überprüfung
#print("Erste Zeilen der autoData CSV-Datei:\n", autoData_df.head())
#print("Erste Zeilen der jahrlicheKosten CSV-Datei:\n", autoKosten_df.head())
#print("Erste Zeilen der wertverlust CSV-Datei:\n", WertverlustImJahr_df.head())

# Transponiere die Daten, um die Zeilen als Spalten zu behandeln
autoData_df = autoData_df.set_index(autoData_df.columns[0]).T
autoKosten_df = autoKosten_df.set_index(autoKosten_df.columns[0]).T


# Konvertiere relevante Spalten in numerische Werte, nach Entfernung von Währungssymbolen
autoKosten_df['Nova'] = autoKosten_df['Nova'].replace('[€]', '', regex=True).astype(float)
autoKosten_df['Versicherung_jahrlich'] = autoKosten_df['Versicherung_jahrlich'].replace('[€]', '', regex=True).astype(float)
autoKosten_df['WerkstattkostenJahrlich'] = autoKosten_df['WerkstattkostenJahrlich'].replace('[€]', '', regex=True).astype(float)
autoKosten_df['Preis'] = autoKosten_df['Preis'].replace('[€]', '', regex=True).astype(float)
autoKosten_df['Grundpreis'] = autoKosten_df['Grundpreis'].replace('[€]', '', regex=True).astype(float)
autoData_df['Verbrauch_Gesamt_(NEFZ)'] = autoData_df['Verbrauch_Gesamt_(NEFZ)'].astype(float)

# Berechnungen durchführen
autoKosten_df['Kosten'] = (autoKosten_df['Nova'] / 5 + autoKosten_df['Versicherung_jahrlich'] + autoKosten_df['WerkstattkostenJahrlich'])
autoKosten_df['ZusatzSpritkosten'] = (150 * (autoData_df['Verbrauch_Gesamt_(NEFZ)'] - 3.9))
autoKosten_df['Alter'] = heutiges_jahr - autoData_df['BauJahr'].astype(int)



# Berechne den Amortisationswert basierend auf dem Alter
def berechne_amortisation(row):
    alter = row['Alter']
    if alter < len(WertverlustImJahr_df):
        wertverlust_prozent = WertverlustImJahr_df.iloc[alter]['procent']
    else:
        wertverlust_prozent = WertverlustImJahr_df.iloc[-1]['procent']
    return row['Grundpreis'] * (1 - wertverlust_prozent)

autoKosten_df['AktuellerWert'] =  autoKosten_df.apply(berechne_amortisation, axis=1)
autoKosten_df['SumPreis1Jahre'] = autoKosten_df['Kosten'] + autoKosten_df['ZusatzSpritkosten']
autoKosten_df['TotalKosten5Jahre'] = autoKosten_df['Preis'] + autoKosten_df['ZusatzSpritkosten'] * 5 + autoKosten_df['Kosten'] * 5 - (autoKosten_df['Preis'] * 0.2)
autoKosten_df['TotalKosten1Jahre'] = autoKosten_df['TotalKosten5Jahre'] / 5

# Ergebnisse anzeigen
print(autoKosten_df[['Kosten', 'ZusatzSpritkosten', 'AktuellerWert', 'SumPreis1Jahre', 'TotalKosten5Jahre', 'TotalKosten1Jahre']])