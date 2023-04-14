import nltk
nltk.download('punkt') 
import random
import numpy as np
import pandas as pd
import torch
from torch import optim
from tqdm import tqdm

# from modules.word_classification import BertForWordClassification
from transformers import BertConfig, BertTokenizer
from nltk.tokenize import word_tokenize

def word_subword_tokenize(sentence, tokenizer):
    # Add CLS token
    subwords = [tokenizer.cls_token_id]
    subword_to_word_indices = [-1] # For CLS

    # Add subwords
    for word_idx, word in enumerate(sentence):
        subword_list = tokenizer.encode(word, add_special_tokens=False)
        subword_to_word_indices += [word_idx for i in range(len(subword_list))]
        subwords += subword_list

    # Add last SEP token
    subwords += [tokenizer.sep_token_id]
    subword_to_word_indices += [-1]

    return subwords, subword_to_word_indices

# load the NER model
mypath = 'D:\Semester 8\Tugas Akhir\Capital Letter Backend\model\\'

ner_model = torch.load(mypath + 'ner_model.pt', map_location=torch.device('cpu'))
ner_model2 = torch.load(mypath + 'ner_model2.pt', map_location=torch.device('cpu'))
tokenizer = BertTokenizer.from_pretrained('indobenchmark/indobert-base-p1')

# Labels
w2i = {'I-PERSON': 0, 'B-ORGANISATION': 1, 'I-ORGANISATION': 2, 'B-PLACE': 3, 'I-PLACE': 4, 'O': 5, 'B-PERSON': 6}
i2w = {0: 'I-PERSON', 1: 'B-ORGANISATION', 2: 'I-ORGANISATION', 3: 'B-PLACE', 4: 'I-PLACE', 5: 'O', 6: 'B-PERSON'}

w2i_2 = {'I-PPL': 0, 'B-EVT': 1, 'B-PLC': 2, 'I-IND': 3, 'B-IND': 4, 'B-FNB': 5, 'I-EVT': 6, 'B-PPL': 7, 'I-PLC': 8, 'O': 9, 'I-FNB': 10}
i2w_2 = {0: 'I-PPL', 1: 'B-EVT', 2: 'B-PLC', 3: 'I-IND', 4: 'B-IND', 5: 'B-FNB', 6: 'I-EVT', 7: 'B-PPL', 8: 'I-PLC', 9: 'O', 10: 'I-FNB'}