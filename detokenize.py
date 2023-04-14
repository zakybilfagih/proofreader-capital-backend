from sacremoses import MosesDetokenizer

detokenizer = MosesDetokenizer()

def detokenize_sentence(lst):
  detokenized_sentence = detokenizer.detokenize(lst)
  return detokenized_sentence