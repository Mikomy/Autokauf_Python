
@Author Miklos Komlosy
version 01.01

Start --> autoAnalysis.py

Der Programm führt eine Analyse der jährlichen Kosten und Wertverluste von Autos durch und stellt die Ergebnisse grafisch dar.
Hier ist eine kurze Beschreibung der verschiedenen Teile meines Programms:

Module
Config (DataLoader):

Lädt die Daten aus CSV-Dateien (autoData.csv, jahrlicheKosten.csv, wertverlust.csv).
Bereitet die Daten vor, indem es sie in DataFrames umwandelt und notwendige Anpassungen vornimmt (z.B. Entfernen von Währungszeichen).


Calculations:

Berechnet verschiedene Kosten und Wertverluste der Autos.
Führt spezifische Berechnungen wie die Amortisation und den jährlichen Wertverlust durch.
Berechnet zusätzliche Kosten und erstellt eine sortierte DataFrame basierend auf den berechneten Kosten.


Plotter:

Erzeugt verschiedene Diagramme, um die Ergebnisse grafisch darzustellen.
Dazu gehören Diagramme wie plot_wertverlust_prozent, plot_wertverlust_autos, plot_kreisdiagramme und plot_bewertete_eigenschaften.
plot_kreisdiagramme zeigt die Verteilung der jährlichen Kosten und das verbleibende Urlaubsgeld in einem Kreisdiagramm an.