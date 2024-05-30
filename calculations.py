import datetime

class Calculations:
    def __init__(self, auto_data_df, auto_kosten_df, wertverlust_im_jahr_df):
        self.auto_data_df = auto_data_df
        self.auto_kosten_df = auto_kosten_df
        self.wertverlust_im_jahr_df = wertverlust_im_jahr_df
        self.heutiges_jahr = datetime.datetime.now().year
    
    def perform_calculations(self):
        self.auto_kosten_df['Kosten'] = (self.auto_kosten_df['Nova'] / 5 + self.auto_kosten_df['Versicherung_jahrlich'] + self.auto_kosten_df['WerkstattkostenJahrlich'])
        self.auto_kosten_df['ZusatzSpritkosten'] = (150 * (self.auto_data_df['Verbrauch_Gesamt_(NEFZ)'] - 3.9))
        self.auto_kosten_df['Alter'] = self.heutiges_jahr - self.auto_data_df['BauJahr'].astype(int)
        self.auto_kosten_df['ZusatzSpritkostenNachElektro'] = (150 * (self.auto_data_df['Verbrauch_Gesamt_(NEFZ)'] - 2.65))
        
        self.auto_kosten_df['AktuellerWert'] = self.auto_kosten_df.apply(self.berechne_amortisation, axis=1)
        self.auto_kosten_df['SumPreis1Jahre'] = self.auto_kosten_df['Kosten'] + self.auto_kosten_df['ZusatzSpritkosten']
        self.auto_kosten_df['TotalKosten5Jahre'] = self.auto_kosten_df['Preis'] + self.auto_kosten_df['ZusatzSpritkosten'] * 5 + self.auto_kosten_df['Kosten'] * 5 - (self.auto_kosten_df['Preis'] * 0.5)
        self.auto_kosten_df['TotalKosten1Jahre'] = self.auto_kosten_df['TotalKosten5Jahre'] / 5
        self.auto_kosten_df['preis_in_alter_5'] = 0

        zweit_guenstigster_preis = self.auto_kosten_df['TotalKosten1Jahre'].nsmallest(2).iloc[-1]
        self.auto_kosten_df['ZusatzlicheKostenaufwand'] = self.auto_kosten_df['TotalKosten1Jahre'] - zweit_guenstigster_preis
        
        self.auto_kosten_df['Wertverlust_pro_Jahr'] = round(self.auto_kosten_df.apply(self.berechne_wertverlust_nach_fuenf_jahren, axis=1), 1)
        self.auto_kosten_df['JahrlicheKosten5bis10Alter'] = round(self.auto_kosten_df['Wertverlust_pro_Jahr'] + self.auto_kosten_df['ZusatzSpritkosten'] + self.auto_kosten_df['Nova'] + self.auto_kosten_df['WerkstattkostenJahrlich'], 1)

        zweit_guenstigster_preis = self.auto_kosten_df['JahrlicheKosten5bis10Alter'].nsmallest(1).iloc[-1]
        self.auto_kosten_df['ZusatzlicheKosten'] = self.auto_kosten_df['JahrlicheKosten5bis10Alter'] - zweit_guenstigster_preis

# Bestimme den zweitgünstigsten Preis
        zweit_guenstigster_preis = self.auto_kosten_df['TotalKosten1Jahre'].nsmallest(2).iloc[-1]
        self.auto_kosten_df['ZusatzlicheKostenaufwand'] = self.auto_kosten_df['TotalKosten1Jahre'] - zweit_guenstigster_preis

# Füge Kofferraumvolumen und Zuladung hinzu
        self.auto_data_df['Kofferraumvolumen_liter'] = self.auto_data_df['Kofferraumvolumen_normal_liter']
        self.auto_data_df['Zuladung'] = self.auto_data_df['Zuladung']

# Füge Kofferraumvolumen und Zuladung zum DataFrame hinzu
        self.auto_kosten_df['Kofferraumvolumen_liter'] = self.auto_data_df['Kofferraumvolumen_normal_liter']
        self.auto_kosten_df['Zuladung_kg'] = self.auto_data_df['Zuladung']

# Sortiere die Tabelle nach dem zusätzlichen Kostenaufwand
        self.auto_kosten_df_sorted = self.auto_kosten_df.sort_values(by='ZusatzlicheKostenaufwand')
        
    def berechne_amortisation(self, row):
        alter = row['Alter']
        if alter < len(self.wertverlust_im_jahr_df):
            wertverlust_prozent = self.wertverlust_im_jahr_df.iloc[alter]['procent']
        else:
            wertverlust_prozent = self.wertverlust_im_jahr_df.iloc[-1]['procent']
        return row['Grundpreis'] * (wertverlust_prozent)
    
    def berechne_wertverlust_nach_fuenf_jahren(self, row):
        alter = row['Alter']
        sollAlter = 5

        if alter < len(self.wertverlust_im_jahr_df):
            kalkulierteGrundPreis = row['Preis'] / self.wertverlust_im_jahr_df.iloc[alter]['procent']
            preis_in_alter_5 = round(kalkulierteGrundPreis * self.wertverlust_im_jahr_df.iloc[sollAlter]['procent'], 1)
            row.at['preis_in_alter_5'] = preis_in_alter_5
            amortisation = (preis_in_alter_5 - (kalkulierteGrundPreis * 0.2))
            return amortisation / 5
        else:
            return round(row['Preis'], 1)
