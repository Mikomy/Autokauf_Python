import pandas as pd
import datetime
import matplotlib.pyplot as plt
import numpy as np

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
autoKosten_df['ZusatzSpritkostenNachElektro'] = (150 * (autoData_df['Verbrauch_Gesamt_(NEFZ)'] - 2.65))


# Berechne den Amortisationswert basierend auf dem Alter
def berechne_amortisation(row):
    alter = row['Alter']
    if alter < len(WertverlustImJahr_df):
        wertverlust_prozent = WertverlustImJahr_df.iloc[alter]['procent']
    else:
        wertverlust_prozent = WertverlustImJahr_df.iloc[-1]['procent']
    return row['Grundpreis'] * (wertverlust_prozent)

autoKosten_df['AktuellerWert'] =  autoKosten_df.apply(berechne_amortisation, axis=1)
autoKosten_df['SumPreis1Jahre'] = autoKosten_df['Kosten'] + autoKosten_df['ZusatzSpritkosten']
autoKosten_df['TotalKosten5Jahre'] = autoKosten_df['Preis'] + autoKosten_df['ZusatzSpritkosten'] * 5 + autoKosten_df['Kosten'] * 5 - (autoKosten_df['Preis'] * 0.5)
autoKosten_df['TotalKosten1Jahre'] = autoKosten_df['TotalKosten5Jahre'] / 5
autoKosten_df['preis_in_alter_5'] = 0


# Bestimme den zweitgünstigsten Preis
zweit_guenstigster_preis = autoKosten_df['TotalKosten1Jahre'].nsmallest(2).iloc[-1]
autoKosten_df['ZusatzlicheKostenaufwand'] = autoKosten_df['TotalKosten1Jahre'] - zweit_guenstigster_preis

# Füge Kofferraumvolumen und Zuladung hinzu
autoData_df['Kofferraumvolumen_liter'] = autoData_df['Kofferraumvolumen_normal_liter']
autoData_df['Zuladung'] = autoData_df['Zuladung']

# Füge Kofferraumvolumen und Zuladung zum DataFrame hinzu
autoKosten_df['Kofferraumvolumen_liter'] = autoData_df['Kofferraumvolumen_normal_liter']
autoKosten_df['Zuladung_kg'] = autoData_df['Zuladung']

# Sortiere die Tabelle nach dem zusätzlichen Kostenaufwand
autoKosten_df_sorted = autoKosten_df.sort_values(by='ZusatzlicheKostenaufwand')

# Ergebnisse anzeigen
print('Autovergleich, am 29.05.2024')
print(autoKosten_df_sorted[['Kosten', 'ZusatzSpritkosten', 'AktuellerWert', 'Preis', 'TotalKosten1Jahre', 'ZusatzlicheKostenaufwand', 'Kofferraumvolumen_liter', 'Zuladung_kg']])
print(' ')

# Ergebnisse in eine Excel-Datei exportieren
excel_datei_name = 'autovergleich_ergebnisse.xlsx'
with pd.ExcelWriter(excel_datei_name) as writer:
    autoKosten_df_sorted[['Kosten', 'ZusatzSpritkosten', 'AktuellerWert', 'Preis', 'TotalKosten1Jahre', 'ZusatzlicheKostenaufwand', 'Kofferraumvolumen_liter', 'Zuladung_kg']].to_excel(writer, sheet_name='Ergebnisse', index=True)
    # Sie können weitere DataFrames hinzufügen, indem Sie weitere to_excel-Anweisungen verwenden, wenn Sie mehrere Tabellen in derselben Excel-Datei haben möchten.
print(f'Die Ergebnisse wurden erfolgreich in "{excel_datei_name}" gespeichert.')

#Diagramm 1: Prozente des Wertverlustes über die Jahren
plt.figure(figsize=(10, 6))
plt.plot(WertverlustImJahr_df.index, WertverlustImJahr_df['procent']*100, marker='o')
plt.title('Wertverlust/amortisation über die Jahre')
plt.xlabel('Jahre')
plt.ylabel('Prozent des Wertverlustes')
plt.grid(True)
plt.savefig('wertverlust_prozent.png')
plt.show()

# Diagramm 2: Wertverlust der Autos über die Jahre basierend auf Baujahr und Grundpreis
plt.figure(figsize=(12, 8))
jahre = range(0, 11)
startjahr = 2018
jahre_labels = [startjahr + jahr for jahr in jahre]

for auto in autoKosten_df.index:
    grundpreis = autoKosten_df.at[auto, 'Grundpreis']
    bauJahr = int(autoData_df.at[auto, 'BauJahr'])
    wert_verlust = []
    for jahr in jahre:
        if (bauJahr + jahr) <= max(jahre_labels):
            alter = jahr
            if alter < len(WertverlustImJahr_df):
                wertverlust_prozent = WertverlustImJahr_df.iloc[alter]['procent']
            else:
                wertverlust_prozent = WertverlustImJahr_df.iloc[-1]['procent']
            wert = grundpreis * (wertverlust_prozent)
            wert_verlust.append(wert)
        else:
            break
    plt.plot([bauJahr + j for j in range(len(wert_verlust))], wert_verlust, label=auto)
    plt.scatter(2024, autoKosten_df.at[auto, 'Preis'], color=plt.gca().lines[-1].get_color())

plt.title('Wertverlust der Autos über die Jahre basierend auf Baujahr und Grundpreis')
plt.xlabel('Jahre')
plt.ylabel('Wert in €')
plt.xticks(jahre_labels)
plt.legend()
plt.grid(True)
plt.savefig('wertverlust_autos.png')
plt.show()




# Berechne den Wert nach 5 Jahren basierend auf den Wertverlustprozentsätzen
def berechne_wertverlust_nach_fuenf_jahren(row):
    alter = row['Alter']
    sollAlter = 5
   
    if alter < len(WertverlustImJahr_df):
         kalkulierteGrundPreis = row['Preis'] / WertverlustImJahr_df.iloc[alter]['procent']
         preis_in_alter_5 = round(kalkulierteGrundPreis * WertverlustImJahr_df.iloc[sollAlter]['procent'], 1)
         print(preis_in_alter_5)
         print(row['Preis'])
         row.at['preis_in_alter_5'] = preis_in_alter_5
         amortisation = (preis_in_alter_5 - (kalkulierteGrundPreis * 0.2))
         return amortisation/5
    else:
        return round(row['Preis'], 1)
    

autoKosten_df['Wertverlust_pro_Jahr'] = round(autoKosten_df.apply(berechne_wertverlust_nach_fuenf_jahren, axis=1),1)
autoKosten_df['JahrlicheKosten5bis10Alter'] = round(autoKosten_df['Wertverlust_pro_Jahr'] + autoKosten_df['ZusatzSpritkosten'] + autoKosten_df['Nova'] + autoKosten_df['WerkstattkostenJahrlich'],1)

# Bestimme den zweitgünstigsten Preis
zweit_guenstigster_preis = autoKosten_df['JahrlicheKosten5bis10Alter'].nsmallest(1).iloc[-1]
autoKosten_df['ZusatzlicheKosten'] = autoKosten_df['JahrlicheKosten5bis10Alter'] - zweit_guenstigster_preis

# Filtern Sie die Daten, um 'Prius_1.8_Hybrid' auszuschließen
autoKosten_df = autoKosten_df.drop('Prius_1.8_Hybrid', errors='ignore')

# Kreisdiagramme erstellen
fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(18, 10))

for i, (index, row) in enumerate(autoKosten_df.iterrows()):
    ax = axes[i // 3, i % 3]
    labels = ['Nova', 'Versicherung jährlich', 'Werkstattkosten jährlich', 'Zusatz Spritkosten', 'Wertverlust pro Jahr']
    sizes = [row['Nova'], row['Versicherung_jahrlich'], row['WerkstattkostenJahrlich'], row['ZusatzSpritkostenNachElektro'], row['Wertverlust_pro_Jahr']]
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, textprops={'fontsize': 8})
    ax.set_title(f"{index}\nJährliche Kosten von 5 bis 10 Alter: €{row['JahrlicheKosten5bis10Alter']:.2f}")


# Gesamtüberschrift für die gesamte Abbildung
plt.suptitle('Kostenverteilung der Autos im 5. Jahr und Total Kosten auf 1 Jahre', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig('kostenaufteilung.png')
plt.show()

autoKosten_df_sorted = autoKosten_df.sort_values(by='ZusatzlicheKostenaufwand')
# Ergebnisse anzeigen
print('Wenn alle Autos heute 5 Jahre alt wäre')
print(autoKosten_df_sorted[[ 'Preis', 'Wertverlust_pro_Jahr', 'JahrlicheKosten5bis10Alter', 'TotalKosten1Jahre', 'ZusatzlicheKosten', 'Kofferraumvolumen_liter', 'Zuladung_kg']])

# Ergebnisse in eine Excel-Datei exportieren
excel_datei_name = 'Wenn_alle_Autos_heute_5_Jahre_alt_wäre.xlsx'
with pd.ExcelWriter(excel_datei_name) as writer:
    autoKosten_df_sorted[[ 'preis_in_alter_5', 'Wertverlust_pro_Jahr', 'JahrlicheKosten5bis10Alter', 'TotalKosten1Jahre', 'ZusatzlicheKosten', 'Kofferraumvolumen_liter', 'Zuladung_kg']].to_excel(writer, sheet_name='Ergebnisse', index=True)
    # Sie können weitere DataFrames hinzufügen, indem Sie weitere to_excel-Anweisungen verwenden, wenn Sie mehrere Tabellen in derselben Excel-Datei haben möchten.
print(f'Die Ergebnisse wurden erfolgreich in "{excel_datei_name}" gespeichert.')





# Daten für das Diagramm
selected_columns = ['Kofferraumvolumen_liter', 'Zuladung_kg', 'Preis', 'JahrlicheKosten5bis10Alter', 'ZusatzlicheKosten']
autoKosten_df_sorted = autoKosten_df.sort_values(by='ZusatzlicheKosten')  
n_cars = len(autoKosten_df_sorted)

# Anzahl der Spalten im Subplot
n_cols = len(selected_columns)

# Erstellen der Subplots
fig, ax = plt.subplots(figsize=(12, 8))

# Festlegen der Breite der Balken
bar_width = 0.15

# Positionen für die Balken festlegen
index = np.arange(n_cars)

# Bewertungsskala für jede Eigenschaft definieren
kofferraum_scale_min = 300
kofferraum_scale_max = 700
zuladung_scale_min = 300
zuladung_scale_max = 700
preis_scale_min = 10000
preis_scale_max = 26000
kosten_scale_min = 2000
kosten_scale_max = 6000
zusatzlicheKosten_scale_min = 0
zusatzlicheKosten_scale_max = 2000


# Funktion zur Umrechnung der Werte in Punkte auf der skalierten y-Achse (0-10) für jede Eigenschaft
def scale_value(value, min_value, max_value, scale_min=0, scale_max=10):
    return scale_min + (scale_max - scale_min) * (value - min_value) / (max_value - min_value)

# Skalierung der Werte für jede Eigenschaft
scaled_values = {}
for column in selected_columns:
    values = autoKosten_df_sorted[column].astype(float).values
    if column == 'Kofferraumvolumen_liter':
        scaled_values[column] = [scale_value(value, kofferraum_scale_min, kofferraum_scale_max) for value in values]
    elif column == 'Zuladung_kg':
        scaled_values[column] = [scale_value(value, zuladung_scale_min, zuladung_scale_max) for value in values]
    elif column == 'Preis':
        scaled_values[column] = [10 - scale_value(value, preis_scale_min, preis_scale_max) for value in values]
    elif column == 'JahrlicheKosten5bis10Alter':
        scaled_values[column] = [10 - scale_value(value, kosten_scale_min, kosten_scale_max) for value in values]
    elif column == 'ZusatzlicheKosten':
        scaled_values[column] = [10 - scale_value(value, zusatzlicheKosten_scale_min, zusatzlicheKosten_scale_max) for value in values]

# Plot für jede Spalte erstellen
for i, column in enumerate(selected_columns):
    ax.bar(index + i * bar_width, scaled_values[column], bar_width, label=column)

    # Annotieren der Balken mit ihren genauen Werten
    for j, value in enumerate(autoKosten_df_sorted[column].astype(float).values):
        ax.annotate(f'{value:.2f}', xy=(index[j] + i * bar_width, scaled_values[column][j]),
                    xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=5)


# Achsenbeschriftungen festlegen
ax.set_xlabel('Autos')
ax.set_ylabel('Bewertung')
ax.set_title('Wenn alle Autos heute 5 Jahre alt wäre')
ax.set_xticks(index + 0.5)
ax.set_xticklabels(autoKosten_df_sorted.index, rotation=45, ha='right')
ax.set_yticks(np.arange(0, 11))  # Skalierte y-Achse von 0 bis 10
ax.set_yticklabels(np.arange(0, 11))  # Bewertungsskala von 0 bis 10
ax.legend()

plt.tight_layout()
plt.savefig('bewerteteEigenschaften.png')
plt.show()
