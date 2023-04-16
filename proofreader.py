# Importing libraries
from nltk.tokenize import word_tokenize
from detokenize import detokenize_sentence
from kamus import *
import torch
from ner import *
from format_correction import correction_formatter

# Proofreader
def proofreader_v3(input):
    kalimat = word_tokenize(input)
    subwords, subword_to_word_indices = word_subword_tokenize(kalimat, tokenizer)

    # NERGrit
    subwords = torch.LongTensor(subwords).view(1, -1).to(ner_model.device)
    subword_to_word_indices = torch.LongTensor(subword_to_word_indices).view(1, -1).to(ner_model.device)
    logits = ner_model(subwords, subword_to_word_indices)[0]
    preds = torch.topk(logits, k=1, dim=-1)[1].squeeze().numpy()

    # NERP
    subwords2 = torch.LongTensor(subwords).view(1, -1).to(ner_model2.device)
    subword_to_word_indices2 = torch.LongTensor(subword_to_word_indices).view(1, -1).to(ner_model2.device)
    logits2 = ner_model2(subwords2, subword_to_word_indices2)[0]
    preds2 = torch.topk(logits2, k=1, dim=-1)[1].squeeze().numpy()

    # Labels from NER model
    nergrit = [i2w[preds[i]] for i in range(len(preds))]
    nerp = [i2w_2[preds2[i]] for i in range(len(preds2))]

    # Result
    lst_correction = []
    
    # index
    start_idx = 0
    

    for i in range(len(kalimat)):
        offset = input.find(kalimat[i], start_idx)

        # Capitalize awal kalimat          
        if i == 0:
            #    kalimat[i] = kalimat[i].title()
            if not kalimat[i].istitle():
                replacement = kalimat[i].title()
                deleteCount = len(kalimat[i])

                lst_correction.append(correction_formatter(offset, deleteCount, replacement))

        else:  
            # Capitalize awal kalimat pada petikan langsung
            if kalimat[i-1] in ['"', '``', '\'\'', '.']:
                #   kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    replacement = kalimat[i].title()
                    deleteCount = len(kalimat[i])
                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue

            # Capitalize person, place, organization
            if nergrit[i] != 'O' and not kalimat[i].isupper():
                # kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].title()

                    if nergrit[i-1] != 'O' and len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                        offset = lst_correction[-1]['offset']
                        deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                        replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                        lst_correction.pop()
                        lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                        continue

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue

            # Capitalize peristiwa sejarah dan hari raya
            if i < len(kalimat) - 1:
                if 'EVT' in nerp[i] and not kalimat[i].isupper() and \
                            kalimat[i] not in ['hari', 'bulan'] and \
                            ('EVT' in nerp[i-1] or 'EVT' in nerp[i+1]):
                    # kalimat[i] = kalimat[i].title()
                    if not kalimat[i].istitle():
                        deleteCount = len(kalimat[i])
                        replacement = kalimat[i].title()

                        if 'EVT' in nerp[i-1] and len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                            print(replacement)
                            offset = lst_correction[-1]['offset']
                            deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                            replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                            lst_correction.pop()
                            lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                            continue

                        lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                        continue
                    
            # Capitalize nama hari dan bulan
            if kalimat[i] in hari_bulan:
                # kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].title()

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue
            
            
            # Capitalize suku dan bangsa
            if kalimat[i] in suku_bangsa:
                # kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].title()

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue
            
            
            # Capitalize nama bahasa dan aksara
            if kalimat[i] in bahasa_aksara:
                # kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].title()

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue
            
            
            # Capitalize istilah agama
            if kalimat[i] in istilah_agama:
                # kalimat[i] = kalimat[i].title()
                if not kalimat[i].istitle():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].title()

                    if i != 1 and len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                        offset = lst_correction[-1]['offset']
                        deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                        replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                        lst_correction.pop()
                        lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                        continue

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue
            
            # Capitalize kenampakan alam diikuti nama and Non-Capitalize kenampakan alam tidak diikuti nama
            if i < len(kalimat) - 1:
                if kalimat[i].casefold() in kenampakan_alam:
                    if 'PLACE' in nergrit[i+1]:
                        #   kalimat[i] = kalimat[i].title()
                        if not kalimat[i].istitle():
                            deleteCount = len(kalimat[i])
                            replacement = kalimat[i].title()

                            if i != 1 and len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                                offset = lst_correction[-1]['offset']
                                deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                                replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                                lst_correction.pop()
                                lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                                continue

                            lst_correction.append(correction_formatter(offset, kalimat[i], replacement))
                            continue
                    else:
                        #   kalimat[i] = kalimat[i].lower()
                        if not kalimat[i].islower():
                            deleteCount = len(kalimat[i])
                            replacement = kalimat[i].lower()

                            if i != 1 and len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                                offset = lst_correction[-1]['offset']
                                deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                                replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                                lst_correction.pop()
                                lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                                continue

                            lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                            continue
            
            # Capitalize singkatan gelar
            if kalimat[i].lower() in gelar_lower:
                # kalimat[i] = gelar[gelar_lower.index(kalimat[i].lower())]
                if kalimat[i] != gelar[gelar_lower.index(kalimat[i].lower())]:
                    deleteCount = len(kalimat[i])
                    replacement = gelar[gelar_lower.index(kalimat[i].lower())]  

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue

            # Non-Capitalize kata tugas
            if kalimat[i] in kata_tugas:
                # kalimat[i] = kalimat[i].lower()
                if not kalimat[i].islower():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].lower()

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue

            # Non-Capitalize anak dari
            if kalimat[i] in anak_dari and 'PERSON' in nergrit[i-1]:
                # kalimat[i] = kalimat[i].lower()
                if not kalimat[i].islower():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].lower()

                    if len(lst_correction) > 0 and offset - (lst_correction[-1]['offset'] + lst_correction[-1]['deleteCount'] - 1) == 2:
                        offset = lst_correction[-1]['offset']
                        deleteCount = deleteCount + lst_correction[-1]['deleteCount'] + 1
                        replacement = lst_correction[-1]['replacement'] + ' ' + replacement

                        lst_correction.pop()
                        lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                        continue

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue

            # Non-Capitalize satuan
            if kalimat[i] in satuan and kalimat[i-1].isdigit():
                #   kalimat[i] = kalimat[i].lower()
                if not kalimat[i].islower():
                    deleteCount = len(kalimat[i])
                    replacement = kalimat[i].lower()

                    lst_correction.append(correction_formatter(offset, deleteCount, replacement))
                    continue 

        # calculate the index
        start_idx = offset + 1

    return lst_correction