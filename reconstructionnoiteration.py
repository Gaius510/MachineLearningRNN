# -*- coding: utf-8 -*-
"""ReconstructionNoIteration.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1dlqn26OyAJTL7CNpBGTCZl9JC4rvNNxd

# Rekonstruktion von Morse-Codes mithilfe von LSTM-Netwerken

Ziel dieses Projektes ist es, die Leerzeichen beziehungsweise die Pausen zwischen den Darstellungen einzelner Buchstaben im Morsecode mithilfe eines rekurrenten LSTM-Netzwerkes zu rekonstruieren. Obwohl durch das Weglassen der Leerzeichen im Prinzip Information verloren geht, ergeben meistens nur bestimmte Positionen der Leerzeichen sinnvolle Wörter.
"""

import tensorflow as tf
import numpy as np

"""## Morse-Kodierung

Zuerst schreiben wir eine Funktion `to_morse`, die ein Wort in Morse-Code übersetzt
"""

morse_code = {
    'A': '.-',     'B': '-...',   'C': '-.-.',   'D': '-..',    'E': '.',      'F': '..-.',
    'G': '--.',    'H': '....',   'I': '..',     'J': '.---',   'K': '-.-',    'L': '.-..',
    'M': '--',     'N': '-.',     'O': '---',    'P': '.--.',   'Q': '--.-',   'R': '.-.',
    'S': '...',    'T': '-',      'U': '..-',    'V': '...-',   'W': '.--',    'X': '-..-',
    'Y': '-.--',   'Z': '--..' }

def to_morse_word(word):
    word = word.upper()
    
    return ' '.join([morse_code[x] for x in word])

"""Test der Funktion:"""

to_morse_word("SOS")

"""## Eingabe und Ausgabe des neuronalen Netzwerkes

Wir müssen uns zuerst fragen, wie die Ein- und Ausgabe des Netzwerkes kodiert sein soll. Wie alle neuronalen Netze besteht die Eingabe eines LSTM-Modells nicht aus Zeichen, sondern aus Gleitkommazahlen.

Die Eingabe soll ein Morse-Code sein. Da die Leerzeichen weggelassen wurden, besteht dieser nur aus zwei Zeichen. Ein häufiges Verfahren für die Kodierung kategorischer Daten ist das *one-hot encoding*. Die folgende Funktion implementiert diese Codierung der Eingabe, wobei die Leerzeichen im Morsecode automatisch weggelassen werden.

**Look-ahead** Es ist schwierig für das neuronale Netz, zu entscheiden, wo die Morse-Codes unterbrochen werden sollen, ohne wenigstens ein paar Zeichen vorwärts schauen zu können. Daher verschiebe ich einfach Ein- und Ausgabe mithilfe eines einstellbaren look-aheads gegeneinander. Anders gesagt, das neuronale Netz muss erst einige Zeichen später signalisieren, dass ein Leerzeichen eingefügt werden soll.
"""

lookahead = 10

"""Die Eingabe wird als `float`-Array kodiert, damit man sie direkt ins neuronale Netzwerk einspeisen kann."""

def encode_input(morse):
    encodings = { '.': [1, 0, 0], '-': [0, 1, 0], 'X': [0, 0, 1] }
    return np.array([encodings[x] for x in (morse #+ lookahead*"X" 
                                           )if x != ' ']).astype(float)

encode_input(to_morse_word("SOS"))

"""Die Ausgabe des Netzwerkes möchte ich so machen, dass das Netz für jedes Eingabezeichen entscheiden soll, ob nach diesem Zeichen ein Leerzeichen wahrscheinlich ist. Die gewünschte Ausgabe ist also `1`, wenn auf ein Zeichen im ursprünglichen Morsecode ein Leerzeichen folgt, und sonst `0`. Für das letzte Zeichen macht es Sinn, `1` vorzuschreiben, da das Wortende ja auch ein Buchstabenende ist. Die folgende Funktion implementiert die gewünschte Ausgabe:"""

def compute_target(morse):
    return np.array(#lookahead*[0] + 
        [int((b == " ") | (b == "X")) for a,b in zip(morse[:-1], morse[1:]) if a != " "] + [1]).astype(float)

compute_target(to_morse_word("SOS"))

"""Bei "SOS" haben alle Buchstaben drei Zeichen, deshalb besteht die gewünscht Ausgabe aus drei gleichen Teilen.

## Trainings-Daten generieren
"""

with open("unix_cambridge.txt", "r") as f:
    words = f.read()

assert all([x.upper() in morse_code or x == "\n" for x in words])

words = words.split("\n")[:-1]

def get_random_word():
    return words[np.random.randint(len(words))]

def make_training_data(length):
    word = get_random_word()
    morse = to_morse_word(word)
    inputs = encode_input(morse)
    targets = compute_target(morse)
    inputs = inputs[:length]
    targets = targets[:length]
    return inputs, targets

def make_batches(n_batches, length):
    inputs, targets = [np.zeros((n_batches, length, k)) for k in [3,1]]
    for i in range(n_batches):
        inputs[i], targets[i,:,0] = make_training_data(length)
    return inputs, targets

morse_all = [to_morse_word(w) for w in words]

np.amax([len(x) for x in morse_all])

words_all = np.zeros((len(words), 50 + lookahead, 3))
outs_all = np.zeros((len(words), 50 + lookahead, 1))

morse_all[1]

for i in range(len(words)):
    c = morse_all[i]
    print(len(c), encode_input(c).shape)
    enc = encode_input(c)
    outs_all[i,lookahead:lookahead+enc.shape[0],0] = compute_target(c)
    words_all[i, :enc.shape[0]] = enc
    words_all[i, enc.shape[0]:] = [0,0,1]

words_all.shape, outs_all.shape

"""## Trainings-Daten aus Text"""

with open("unix_cambridge.txt", "r") as f:
    text = f.read()
text = "".join([x for x in text if x == "\n" or x == " " or (x.upper() in morse_code)])
text = text.replace("\n", " ")
text = " ".join(text.split())
print(text)

" ".join("abc def ghi".split())

text[:500]

def make_batch(length, n_batches=32):
    pos = np.random.randint(len(text) - length + 50)
    subtext = text[pos : pos + length + 50]
    idx = subtext[:50].find(" ")
    if idx > 0:
        subtext = subtext[idx : length + idx]
    morse = to_morse_word(subtext)
    inputs = encode_input(morse)
    targets = compute_target(morse)
    inputs = inputs[:length]
    targets = targets[:length]
    return inputs, targets

def make_batches(n_batches, length):
    inputs, targets = [np.zeros((n_batches, length, k)) for k in [3,1]]
    for i in range(n_batches):
        inputs[i], targets[i,:,0] = make_batch(length, n_batches=32)
    return inputs, targets

print(make_batch)

"""## Morse-Dekodieren zum Testen"""

morse_inverse = { code: letter for letter, code in morse_code.items() }

def morse_decode_word(with_spaces):
    codes = with_spaces.split(" ")
    return "".join([morse_inverse[x] if x in morse_inverse else "?" for x in codes])
def morse_decode(s):
    return " ".join([morse_decode_word(x) for x in s.split("X")])

def remove_spaces(s):
    return "".join([x for x in s if x != " "])

def insert_spaces(s_no_spaces, output=None):
    inp_encode = encode_input(s_no_spaces + lookahead*"X")
    if output is None:
        output = model(inp_encode.reshape(1,-1,3)).numpy()[0,:,0][lookahead:]
    with_spaces = ""
    for i in range(len(s_no_spaces)):
        char = s_no_spaces[i]
        with_spaces += char
        if output[i] > 0 and i < len(s_no_spaces) - 1 and s_no_spaces[i+1] != "X" and s_no_spaces[i] != "X":
            with_spaces += " "
    return with_spaces

"""## Möglichkeiten generieren"""

len(np.unique(np.array([remove_spaces(to_morse_word(x)) for x in words], dtype=str)))

len(words)

"""## Definition und Training des Modells"""

model = tf.keras.Sequential()
model.add(tf.keras.layers.LSTM(300, return_sequences=True))
#model.add(tf.keras.layers.Dense(150, activation='relu'))
#model.add(tf.keras.layers.LSTM(250, return_sequences=True))
#model.add(tf.keras.layers.Dense(500, activation='relu'))
model.add(tf.keras.layers.LSTM(400, return_sequences=True))
model.add(tf.keras.layers.Dense(1000, activation='relu'))
#model.add(tf.keras.layers.Dense(2000, activation='relu'))
#model.add(tf.keras.layers.LSTM(60, return_sequences=True))
model.add(tf.keras.layers.Dense(1))

model.compile(optimizer=tf.optimizers.Adam(), loss = tf.losses.BinaryCrossentropy(from_logits=True))

n_iter = 10
for i in range(n_iter):
    print("STEP {} / {}".format(i, n_iter))
    model.fit(words_all, outs_all, epochs=20)
    
    for i in range(15, 25):
        word = words[i]
        rec = morse_decode(insert_spaces(remove_spaces(to_morse_word(word))))
        print(word, rec)

morse_orig = to_morse_word("hamburg")
print(morse_orig)

nospace = remove_spaces(morse_orig)
print(nospace)

reconstructed = insert_spaces(nospace)
print(reconstructed)

morse_decode(reconstructed)

# Save the entire model to a HDF5 file.
# The '.h5' extension indicates that the model should be saved to HDF5.
model.save('1.h5')

import nltk
import tensorflow as tf


from nltk.translate.bleu_score import corpus_bleu

# Load the saved model and test data
model = tf.keras.models.load_model('1.h5')
X_test = words_all
y_test = outs_all

# Make predictions on test set
y_pred = model.predict(X_test)

# Convert the predicted and reference sequences into lists of strings
y_pred_strings = [[str(word) for word in sentence] for sentence in y_pred]
y_ref_strings = [[[str(word) for word in sentence]] for sentence in y_test]

# Calculate the BLEU score
bleu_score = corpus_bleu(y_ref_strings, y_pred_strings)

print("BLEU score: ", bleu_score)

print(outs_all.shape)

print(words_all.shape)

from sklearn.metrics import accuracy_score, precision_score, f1_score
import numpy as np
from tensorflow import keras


outs_all_flat = outs_all.reshape((71716*60,))
words_all_flat = words_all.reshape((71716*60, 3))

# Load the test data
x_test = words_all_flat
y_test = outs_all_flat

# Load the saved model
model = keras.models.load_model('1.h5')

# Reshape the true labels and predicted labels
y_true = y_test.reshape(-1, 3)
x_test = x_test.reshape(-1, 60, 3)

y_pred = model.predict(x_test).reshape(-1, 3)

# Apply a threshold to obtain binary predictions
threshold = 0.5
binary_predicted_labels = (y_pred >= threshold).astype(int)

# Calculate the F1 score, accuracy, and precision
f1 = f1_score(y_true, binary_predicted_labels, average='weighted')
accuracy = accuracy_score(y_true, binary_predicted_labels)
precision = precision_score(y_true, binary_predicted_labels, average='weighted')

# Print the evaluation scores
print("F1 score:", f1)
print("Accuracy:", accuracy)
print("Precision:", precision)