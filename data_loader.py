import pandas as pd
from config import Config

class DataLoader:

    def __init__(self, auto_data_file='autoData.csv', kosten_file='jahrlicheKosten.csv', wertverlust_file='wertverlust.csv'):
        self.auto_data_file = auto_data_file
        self.kosten_file = kosten_file
        self.wertverlust_file = wertverlust_file
    
    def load_data(self):
        self.auto_data_df = pd.read_csv(self.auto_data_file, delimiter=';', decimal=',')
        self.auto_kosten_df = pd.read_csv(self.kosten_file, delimiter=';', decimal=',')
        self.wertverlust_im_jahr_df = pd.read_csv(self.wertverlust_file, delimiter=';', decimal=',')
        
        self.auto_data_df = self.auto_data_df.set_index(self.auto_data_df.columns[0]).T
        self.auto_kosten_df = self.auto_kosten_df.set_index(self.auto_kosten_df.columns[0]).T

        self.auto_kosten_df['Nova'] = self.auto_kosten_df['Nova'].replace('[€]', '', regex=True).astype(float)
        self.auto_kosten_df['Versicherung_jahrlich'] = self.auto_kosten_df['Versicherung_jahrlich'].replace('[€]', '', regex=True).astype(float)
        self.auto_kosten_df['WerkstattkostenJahrlich'] = self.auto_kosten_df['WerkstattkostenJahrlich'].replace('[€]', '', regex=True).astype(float)
        self.auto_kosten_df['Preis'] = self.auto_kosten_df['Preis'].replace('[€]', '', regex=True).astype(float)
        self.auto_kosten_df['Grundpreis'] = self.auto_kosten_df['Grundpreis'].replace('[€]', '', regex=True).astype(float)
        self.auto_data_df['Verbrauch_Gesamt_(NEFZ)'] = self.auto_data_df['Verbrauch_Gesamt_(NEFZ)'].astype(float)

