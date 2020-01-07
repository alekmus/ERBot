from boersebot import pdf_reader
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle
from pathlib import Path
import numpy as np
from sklearn.naive_bayes import MultinomialNB


def tokenize_string(input_string):
    """
    Tokenizes a string and removes stopwords.
    :param input_string: String to tokenize.
    :return: A list of tokens for the input_string.
    """
    # Collect stopwords and cast the list into a set for faster access
    stopwords = set(nltk.corpus.stopwords.words('finnish'))

    # Break the input down to words by splitting on whitespace characters
    words = input_string.split()

    # Initialize a stemmer to reduce the word space in classification
    stemmer = nltk.stem.snowball.SnowballStemmer('finnish')

    # Stem and collect the actual words (excluding numbers and special characters) that are not stopwords
    return [stemmer.stem(word) for word in words if (word not in stopwords) and not word.isdigit()]


def tokenize_samples(samples_location):
    """
    Helper function for building a model with naive bayes classifier.
    Tokenizes all samples in given directory and returns a list containing their tokens.
    NOTICE: returns a list where the tokens are connected into a string separated by spaces so it's easier to
    handle for a scipy vectorizer.
    :param samples_location: Location of samples.
    :return: List of tokens for each sample.
    """
    # Calls tokenize_string on the string representation of each pdf file in the folder and
    # collects their tokens into a list.
    # Disregards the text file that contains their labels which is also stored in the directory.
    return [" ".join(tokenize_string(pdf_reader.pdf_to_string(file.path)))
            for file in os.scandir(samples_location)
            if file.name != "labels.csv"]


def build_dictionary(samples_location):
    """
    Builds a dictionary for the naive bayes classifier
    :param samples_location: Directory location of samples the dictionary will be based on.
    :return: Sklearn CountVectorizer that is fitted to samples' token space.
    """
    tokens = tokenize_samples(samples_location)
    count_vectorizer = CountVectorizer()
    count_vectorizer.fit(tokens)
    return count_vectorizer


def build_training(samples_location, count_vectorizer):
    """
    builds a training set based on directory location that has the samples and a labels.csv which contains the
    label for each file
    :param samples_location: Directory location of samples and label data
    :param count_vectorizer: A Scipy countvectorizer that has been fit with build_dictionary method
    :return: feature vectors and labels for each vector
    """
    # Get the list of labels from the samples_location directory
    with open(samples_location+'/labels.csv') as f:
        label_list = [int(label) for label in f]

    # Initialize the vectors and labels as numpy arrays for more convenient use later
    vectors, labels = [], np.array([])

    for file in os.scandir(samples_location):
        if file.name != 'labels.csv':
            pdf = pdf_reader.pdf_to_string(file.path)
            pages = pdf_reader.pdf_to_pages(pdf)

            for page in pages:
                tokens = " ".join(tokenize_string(page))
                vectors.append(tokens)
                """
                if vectors.size == 0:
                    vectors = count_vectorizer.transform(tokens)
                else:
                    print(count_vectorizer.transform(tokens))
                    vectors = np.concatenate((vectors, count_vectorizer.transform(tokens)), axis=0)
                """
            # Name of each file (without extension) is the index of desired page in the label_list
            i = int(Path(file.path).stem)

            # Formulate the label vector for the whole document at the same time
            # Create a zero vector in the length of the pages and switch the correct page to 1
            er_page = label_list[i]
            page_labels = np.zeros(len(pages))
            if i >= 0:  # Files where there are no correct pages are labeled as -1
                # Take into account that the pdf files are 1-indexed
                page_labels[er_page-1] = 1
            labels = np.concatenate((labels, page_labels), axis=None)

    # The transpose for labels is done again for convenience later on
    return count_vectorizer.transform(vectors), labels


if __name__ == '__main__':
    with open('assets/count_vectorizer.pkl', 'rb') as f:
        cv = pickle.load(f)

    # model = MultinomialNB()
    #
    # X, y = build_training("samples", cv)
    # print(y[17])
    # model.fit(X, y)

    # with open('assets/naive_bayes_clf.pkl', 'wb') as f:
    #     pickle.dump(model, f)

    with open('assets/naive_bayes_clf.pkl', 'rb') as f:
        model = pickle.load(f)
    pdf = pdf_reader.pdf_page_to_string('samples/1.pdf', 14)
    pdf = " ".join(tokenize_string(pdf))
    trans = cv.transform([pdf])
    print(model.predict(cv.transform([pdf])))