import matplotlib.pyplot as plt
import numpy as np

class Plotter:
    def __init__(self, auto_kosten_df, wertverlust_im_jahr_df):
        self.auto_kosten_df = auto_kosten_df
        self.wertverlust_im_jahr_df = wertverlust_im_jahr_df
    
    def plot_wertverlust_prozent(self):
        plt.figure(figsize=(12, 8))
        plt.plot(self.wertverlust_im_jahr_df.index, self.wertverlust_im_jahr_df['procent'] * 100, marker='o')
        plt.title('Wertverlust/amortisation über die Jahre')
        plt.xlabel('Jahre')
        plt.ylabel('Prozent des Wertverlustes')
        plt.grid(True)
        plt.savefig('wertverlust_prozent.png')
        plt.show()

    def plot_wertverlust_autos(self, auto_data_df):
        plt.figure(figsize=(12, 8))
        jahre = range(0, 11)
        startjahr = 2018
        jahre_labels = [startjahr + jahr for jahr in jahre]

        for auto in self.auto_kosten_df.index:
            grundpreis = self.auto_kosten_df.at[auto, 'Grundpreis']
            bauJahr = int(auto_data_df.at[auto, 'BauJahr'])
            wert_verlust = []
            for jahr in jahre:
                if (bauJahr + jahr) <= max(jahre_labels):
                    alter = jahr
                    if alter < len(self.wertverlust_im_jahr_df):
                        wertverlust_prozent = self.wertverlust_im_jahr_df.iloc[alter]['procent']
                    else:
                        wertverlust_prozent = self.wertverlust_im_jahr_df.iloc[-1]['procent']
                    wert = grundpreis * (wertverlust_prozent)
                    wert_verlust.append(wert)
                else:
                    break
            plt.plot([bauJahr + j for j in range(len(wert_verlust))], wert_verlust, label=auto)
            plt.scatter(2024, self.auto_kosten_df.at[auto, 'Preis'], color=plt.gca().lines[-1].get_color())

        plt.title('Wertverlust der Autos über die Jahre basierend auf Baujahr und Grundpreis')
        plt.xlabel('Jahre')
        plt.ylabel('Wert in €')
        plt.xticks(jahre_labels)
        plt.legend()
        plt.grid(True)
        plt.savefig('wertverlust_autos.png')
        plt.show()

    def plot_kreisdiagramme(self):
        self.auto_kosten_df = self.auto_kosten_df.drop('Prius_1.8_Hybrid', errors='ignore')
        fig, axes = plt.subplots(nrows=2, ncols=3, figsize=(12, 8))

        def absolute_value(val, sizes):
            a = int(val/100.*sum(sizes))
            return f'€{a}'

        for i, (index, row) in enumerate(self.auto_kosten_df.iterrows()):
            ax = axes[i // 3, i % 3]
            labels = ['Nova', 'Versicherung jährlich', 'Werkstattkosten jährlich', 'Zusatz Spritkosten', 'Wertverlust pro Jahr', 'Bleibt als Urlaubsgeld']
            total_kosten = row['Nova']/5 + row['Versicherung_jahrlich'] + row['WerkstattkostenJahrlich'] + row['ZusatzSpritkostenNachElektro'] + row['Wertverlust_pro_Jahr']
            if total_kosten < 6000:
                urlaubsgeld = 6000 - total_kosten
            else:
                urlaubsgeld = 0
            sizes = [row['Nova']/5, row['Versicherung_jahrlich'], row['WerkstattkostenJahrlich'], row['ZusatzSpritkostenNachElektro'], row['Wertverlust_pro_Jahr'], urlaubsgeld]
            ax.pie(sizes, labels=labels, autopct=lambda p: absolute_value(p, sizes), startangle=140, textprops={'fontsize': 8})
            ax.set_title(f"{index}\nJährliche Kosten von 5 bis 10 Alter: €{row['JahrlicheKosten5bis10Alter']:.2f}")

        plt.suptitle('Kostenverteilung der Autos im 5. Jahr und Total Kosten auf 1 Jahre', fontsize=16)
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        plt.savefig('kostenaufteilung.png')
        plt.show()


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


    def plot_bewertete_eigenschaften(self):
        selected_columns = ['Kofferraumvolumen_liter', 'Zuladung_kg', 'Preis', 'JahrlicheKosten5bis10Alter', 'ZusatzlicheKosten']
        self.auto_kosten_df_sorted = self.auto_kosten_df.sort_values(by='ZusatzlicheKosten')  
        n_cars = len(self.auto_kosten_df_sorted)
        n_cols = len(selected_columns)
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.15
        index = np.arange(n_cars)

        def scale_value(value, min_value, max_value, scale_min=0, scale_max=10):
            return scale_min + (scale_max - scale_min) * (value - min_value) / (max_value - min_value)

        scaled_values = {}
        for column in selected_columns:
            values = self.auto_kosten_df_sorted[column].astype(float).values
            if column == 'Kofferraumvolumen_liter':
                scaled_values[column] = [scale_value(value, 300, 700) for value in values]
            elif column == 'Zuladung_kg':
                scaled_values[column] = [scale_value(value, 300, 700) for value in values]
            elif column == 'Preis':
                scaled_values[column] = [10 - scale_value(value, 10000, 26000) for value in values]
            elif column == 'JahrlicheKosten5bis10Alter':
                scaled_values[column] = [10 - scale_value(value, 2000, 6000) for value in values]
            elif column == 'ZusatzlicheKosten':
                scaled_values[column] = [10 - scale_value(value, 0, 2000) for value in values]

        for i, column in enumerate(selected_columns):
            ax.bar(index + i * bar_width, scaled_values[column], bar_width, label=column)
            for j, value in enumerate(self.auto_kosten_df_sorted[column].astype(float).values):
                ax.annotate(f'{value:.2f}', xy=(index[j] + i * bar_width, scaled_values[column][j]),
                            xytext=(0, 5), textcoords="offset points", ha='center', va='bottom', fontsize=5)

        ax.set_xlabel('Autos')
        ax.set_ylabel('Bewertung')
        ax.set_title('Wenn alle Autos heute 5 Jahre alt wäre')
        ax.set_xticks(index + 0.5)
        ax.set_xticklabels(self.auto_kosten_df_sorted.index, rotation=45, ha='right')
        ax.set_yticks(np.arange(0, 11))
        ax.set_yticklabels(np.arange(0, 11))
        ax.legend()

        plt.tight_layout()
        plt.savefig('bewerteteEigenschaften.png')
        plt.show()

