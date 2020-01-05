from boersebot import pdf_reader
import nltk
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle


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


if __name__ == '__main__':
    with open('assets/count_vectorizer.pkl', 'rb') as f:
        cv = pickle.load(f)

    print(cv.get_feature_names())