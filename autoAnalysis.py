from data_loader import DataLoader
from calculations import Calculations
from plotter import Plotter
import config
import pandas as pd

# @Author Miklos Komlosy
# version 01.01

# Der Programm führt eine Analyse der jährlichen Kosten und Wertverluste von Autos durch und stellt die Ergebnisse grafisch dar.



class AutoAnalysis:
    def __init__(self):
        self.data_loader = DataLoader(config.Config.AUTO_DATA_FILE, config.Config.KOSTEN_FILE, config.Config.WERTVERLUST_FILE)
        self.data_loader.load_data()
        self.calculations = Calculations(self.data_loader.auto_data_df, self.data_loader.auto_kosten_df, self.data_loader.wertverlust_im_jahr_df)
        self.plotter = Plotter(self.calculations.auto_kosten_df, self.data_loader.wertverlust_im_jahr_df)
    
    def run_analysis(self):
        self.calculations.perform_calculations()
        self.plotter.plot_wertverlust_prozent()
        self.plotter.plot_wertverlust_autos(self.data_loader.auto_data_df)
        self.plotter.plot_kreisdiagramme()
        self.plotter.plot_bewertete_eigenschaften()

# Ergebnisse anzeigen
        print('Autovergleich, am 29.05.2024')
        print(self.calculations.auto_kosten_df[['Kosten', 'ZusatzSpritkosten', 'AktuellerWert', 'Preis', 'TotalKosten1Jahre', 'ZusatzlicheKostenaufwand', 'Kofferraumvolumen_liter', 'Zuladung_kg']])
        print(' ')

        # Export results to Excel
        excel_datei_name = 'autovergleich_ergebnisse.xlsx'
        with pd.ExcelWriter(excel_datei_name) as writer:
            self.calculations.auto_kosten_df[['Kosten', 'ZusatzSpritkosten', 'AktuellerWert', 'Preis', 'TotalKosten1Jahre', 'ZusatzlicheKostenaufwand', 'Kofferraumvolumen_liter', 'Zuladung_kg']].to_excel(writer, sheet_name='Ergebnisse', index=True)
        print(f'Die Ergebnisse wurden erfolgreich in "{excel_datei_name}" gespeichert.')

# Ergebnisse anzeigen
        print('Wenn alle Autos heute 5 Jahre alt wäre')
        print(self.calculations.auto_kosten_df[[ 'Preis', 'Wertverlust_pro_Jahr', 'JahrlicheKosten5bis10Alter', 'TotalKosten1Jahre', 'ZusatzlicheKosten', 'Kofferraumvolumen_liter', 'Zuladung_kg']])


# Ergebnisse in eine Excel-Datei exportieren
        excel_datei_name = 'Wenn_alle_Autos_heute_5_Jahre_alt_wäre.xlsx'
        with pd.ExcelWriter(excel_datei_name) as writer:
            self.calculations.auto_kosten_df[[ 'preis_in_alter_5', 'Wertverlust_pro_Jahr', 'JahrlicheKosten5bis10Alter', 'TotalKosten1Jahre', 'ZusatzlicheKosten', 'Kofferraumvolumen_liter', 'Zuladung_kg']].to_excel(writer, sheet_name='Ergebnisse', index=True)
        # Sie können weitere DataFrames hinzufügen, indem Sie weitere to_excel-Anweisungen verwenden, wenn Sie mehrere Tabellen in derselben Excel-Datei haben möchten.
        print(f'Die Ergebnisse wurden erfolgreich in "{excel_datei_name}" gespeichert.')

# Nutzung der Klassen
if __name__ == '__main__':
    analysis = AutoAnalysis()
    analysis.run_analysis()
