
Google Colab Pro
Grund dafür, dass der normale Google Colab viel Zeit in Anspruch nimmt und oft Verbindung abbrecht.

Bibliotheken: TensorFlow, Numpy, Metaplotlib, Keras.

Um Levenshtein Distanz Histogramm ploten zu können, ist das installieren von !pip install python-Levenshtein notwendig

In den Ordnern findet man zu jedem Modell den jeweiligen Datensatz

Im Ordner Modelle ist die Datei ModellBig. die Datei wurde mit Kommentaren geschreiben, um möglichst die Verständlichkeit des Codes zu ermöglichen.

SmallModell wurde nicht kommentiert, da der Einzige Unterschied ist der Verwendete Datensatz.
Bei ModelBig ist "bigdata set.txt"
Bei SmallModell ist "dataset0.txt"

Nonseendata sind im Datensätze Ordner unter dem Namen file1, nach der Prüfung auf Überschneidungen mit den Trainingsdatensätzen "bigdata set" und "dataset0" anhand python funktion "filteringwords" bekamen wir "filtered_words"

Quelle für dataset0 ist https://www.cambridgeenglish.org/images/506887-b1-preliminary-2020-vocabulary-list.pdf
zuletzt aufgerufen am 26.04.2023

Quelle für bigdata set ist bei der Dokumentation von dem Statistischen Ansatz zu finden.

Quelle für Nonseendata https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt
zuletzt aufgerufen am 26.04.2023