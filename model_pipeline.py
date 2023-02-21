import json
import pickle
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
from keras import Sequential
from keras import models
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer


def json_load(path_file: str) -> dict:
    """json file upload function"""
    with open(path_file, 'r') as file:
        return json.load(file)

def pickle_load(path_file: str) -> Tokenizer:
    """pickle file (tokenizer) upload function"""
    with open(path_file, 'rb') as file:
        return pickle.load(file)


TOKENIZER_SAVE_PATH = json_load('paths.json')['TOKENIZER_SAVE_PATH']
MODEL_SAVE_PATH = json_load('paths.json')['MODEL_SAVE_PATH']
MAX_TEXT_LEN = 200

model: Sequential
tokenizer: Tokenizer

def model_predict(text: str) -> str:
    """LSTM model prediction function for this sample"""
    try:
        sequence = tokenizer.texts_to_sequences([text])
        sequence = pad_sequences(sequence, maxlen=MAX_TEXT_LEN)
        if sequence.max() == 0:
            return 'Enter the words in English'
        else:
            predict = model.predict(sequence, verbose=0)
            if predict > 0.5:
                return 'Positive feedback'
            else:
                return 'Negative feedback'
    except AttributeError:
        return 'Enter the text'


if __name__ == "__main__":
    model = models.load_model(MODEL_SAVE_PATH)
    tokenizer = pickle_load(TOKENIZER_SAVE_PATH)
    model_predict('')
