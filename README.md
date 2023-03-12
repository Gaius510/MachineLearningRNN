# solid-octo

The project is about Morse code.

Morse code consists of characters. A combination of several characters forms a letter and a combination of several combinations forms a word.

Between these compositions there are spaces, so after each composition that forms an Alphabet there is a space.

The question is, what happens if these spaces are lost or deleted? can this Morse code still be understood and translated back to a word ?

We want to use machine learning approaches, i.e. neural networks, to reconstruct this modified Morse code.

We train our neural network on the dataset,Words and their Morse code sequences and their corresponding modified sequences.

The goal is that , when we give our model a modified Morse code as an input, the model should be able to gives us a correct Morse code where the spaces are in the right places and that can be translated back to a word

My modell is not giving an understandable result when given a random input nor when given an input from dataset we trained it on
