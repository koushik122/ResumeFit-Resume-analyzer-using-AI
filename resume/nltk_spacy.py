# python -m spacy download en_core_web_sm
import spacy

nlp = spacy.load('en_core_web_sm')
stop_words_spacy = nlp.Defaults.stop_words

# nltk.download('punkt')
# nltk.download('punkt_tab')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('averaged_perceptron_tagger_eng')
# nltk.download('stopwords')

from nltk.corpus import stopwords
stop_words_nltk = set(stopwords.words('english'))

# try:
#     tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
#     print("Punkt tokenizer loaded successfully!")
# except Exception as e:
#     print(f"Error loading Punkt tokenizer: {e}")

# NLTK Data Processing

def lower_case(any_list):
    lowercase_list = [item.lower() for item in any_list]
    return lowercase_list

def nltk_keywords(data):
    from nltk import word_tokenize
    tokens = word_tokenize(data)

    from nltk import pos_tag
    pos_tagged_tokens = pos_tag(tokens)
    keywords = [str(t[0]) for t in pos_tagged_tokens if t[1] in ['NNP', 'NN']]

    keywords = [w for w in keywords if w not in stop_words_nltk]
    keywords = sorted(list(set(x for x in keywords)))

    return keywords

# Spacy Data Processing

def spacy_keywords(data):
    tokens = nlp(data)

    pos_tagged_tokens = [(tok, tok.tag_) for tok in tokens]
    keywords = [str(t[0]) for t in pos_tagged_tokens if t[1] in ['NNP', 'NN']]

    keywords = [w for w in keywords if w not in stop_words_spacy]

    keywords = sorted(list(set(x for x in keywords)))
    return keywords


def keyword(text):
    keywords_resume_spacy_1 = spacy_keywords(text)
    keywords_resume_nltk_1 = nltk_keywords(text)

    keywords_resume_nltk_1=lower_case(keywords_resume_nltk_1)    
    
    keywords_resume_spacy_1=lower_case(keywords_resume_spacy_1)
    

    text_small_case=str(text).lower()

    keywords_resume_spacy_2 = spacy_keywords(text_small_case)
    keywords_resume_nltk_2 = nltk_keywords(text_small_case)

    keywords_resume=sorted(list(set(keywords_resume_nltk_1 + keywords_resume_spacy_1 + keywords_resume_nltk_2 + keywords_resume_spacy_2)))

    return keywords_resume

