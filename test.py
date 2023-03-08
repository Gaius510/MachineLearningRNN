import pandas as pd
from sklearn.model_selection import KFold
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Embedding, LSTM
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Load data
data = pd.read_csv('modified_morse_code_dataset.csv')

# Define number of folds for cross-validation
num_folds = 5

# Create KFold object for cross-validation
kf = KFold(n_splits=num_folds, shuffle=True)

# Define the maximum number of words to keep based on frequency
MAX_NB_WORDS = 1000

# Define the maximum length of each sequence
MAX_SEQUENCE_LENGTH = 50

# Define the embedding dimension
EMBEDDING_DIM = 100

# Define the LSTM output dimension
LSTM_DIM = 128

# Create a tokenizer and fit it on the text data
tokenizer = Tokenizer(num_words=MAX_NB_WORDS)
tokenizer.fit_on_texts(data['morse_code_without_spaces'].values)

# Loop over each fold
for fold_num, (train_indices, test_indices) in enumerate(kf.split(data)):
    # Get training and testing data for this fold
    train_data = data.iloc[train_indices]
    test_data = data.iloc[test_indices]

    # Extract input and target variables from the data
    X_train = train_data['morse_code_without_spaces'].values
    y_train = train_data['morse_code'].values
    X_test = test_data['morse_code_without_spaces'].values
    y_test = test_data['morse_code'].values

    # Convert the text data into sequences of integers
    X_train_seq = tokenizer.texts_to_sequences(X_train)
    X_test_seq = tokenizer.texts_to_sequences(X_test)

    # Pad the sequences to a fixed length
    X_train_padded = pad_sequences(X_train_seq, maxlen=MAX_SEQUENCE_LENGTH)
    X_test_padded = pad_sequences(X_test_seq, maxlen=MAX_SEQUENCE_LENGTH)

    print('X_train shape:', X_train_padded.shape)
    print('y_train shape:', y_train.shape)
    print('X_test shape:', X_test_padded.shape)
    print('y_test shape:', y_test.shape)
    # Define your neural network architecture
    model = Sequential()
    model.add(Embedding(MAX_NB_WORDS, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
    model.add(LSTM(LSTM_DIM))
    model.add(Dense(3, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Train your model on the training data
    model.fit(X_train_padded, y_train, epochs=10, batch_size=32, verbose=0)

    # Test your model on the testing data and compute the accuracy score
    score = model.evaluate(X_test_padded, y_test, verbose=0)
    accuracy = score[1]

    # Print the fold number and accuracy score for this fold
    print('Fold', fold_num + 1)
    print('Accuracy:', accuracy)
