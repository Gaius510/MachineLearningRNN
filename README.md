# solid-octo

The project is about Morse code.

Morse code consists of characters. A combination of several characters forms a letter and a combination of several combinations forms a word.

Between these compositions there are spaces, so after each composition that forms an Alphabet there is a space.

The question is, what happens if these spaces are lost or deleted? can this Morse code still be understood and translated back to a word ?

We want to use machine learning approaches, i.e. neural networks, to reconstruct this modified Morse code.

We train our neural network on the dataset, Words and their Morse code sequences and their corresponding modified sequences.

The goal is that , when we give our model a modified Morse code as an input, the model should be able to gives us a correct Morse code where the spaces are in the right places and that can be translated back to a word


Google Colab Pro is necessary due to the fact that the normal Google Colab takes a lot of time and often disconnects. 

Libraries used are TensorFlow, Numpy, Matplotlib, and Keras. 

To plot the Levenshtein distance histogram, installing !pip install python-Levenshtein is necessary. 

In the folders, you can find the respective dataset for each model. 

In the "Modelle" folder, there is a file called "ModellBig" which has been written with comments to ensure the understandability of the code. 

"SmallModell" has not been commented on because the only difference is the dataset used. In "ModelBig", it is "bigdata set.txt", while in "SmallModell", it is "dataset0.txt". 

Nonseendata are located in the "Datensätze" folder under the name "file1". After checking for overlaps with the training datasets "bigdata set" and "dataset0" using the Python function "filteringwords", we obtained "filtered_words". 

The source for "dataset0" is https://www.cambridgeenglish.org/images/506887-b1-preliminary-2020-vocabulary-list.pdf, last accessed on 26.04.2023. 

The source for "bigdata set" https://github.com/igorbrigadir/stopwords/tree/master

The source for "Nonseendata" is https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt, last accessed on 26.04.2023.
