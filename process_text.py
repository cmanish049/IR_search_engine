import string
import json
import pandas as pd
import nltk
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')
nltk.download('stopwords')
nltk.download('punkt')
from nltk import pos_tag
from nltk.corpus import wordnet
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import warnings
from constants import CSV_NAME

warnings.filterwarnings('ignore')

# Remove stop words

sw = stopwords.words("english")
lemmatizer = WordNetLemmatizer()

def tp1(txt):
    txt = txt.lower()   # Make lowercase
    txt = txt.translate(str.maketrans('',
                                      '',
                                      string.punctuation))   # Remove punctuation marks
    txt = lematize(txt)
    return txt

def fwpt(word):
    tag = pos_tag([word])[0][1][0].upper()
    hash_tag = {"V": wordnet.VERB, "R": wordnet.ADV,"N": wordnet.NOUN,"J": wordnet.ADJ}
    return hash_tag.get(tag, wordnet.NOUN)

def lematize(text):
        tkns = nltk.word_tokenize(text)
        ax = ""
        for each in tkns:
            if each not in sw:
                ax += lemmatizer.lemmatize(each, fwpt(each)) + " "
        return ax

def apply_index(inputs, index):
    words = inputs.Title.split()
    SN = int(inputs.SN)
    for word in words:
        if word in index.keys():
            if SN not in index[word]:
                index[word].append(SN)
        else:
            index[word] = [SN]
    return index

def full_index(df, index):
    for x in range(len(df)):
        inpt = df.loc[x,:]
        ind = apply_index(inputs=inpt, index=index)
    return ind

def construct_index(df, index):
    queue = preprocess_df(df)
    ind = full_index(df=queue, index=index)
    return ind

def index_2(df, x_path):
    if len(df) > 0:
        with open(x_path, 'r') as file:
            prior_index = json.load(file)
        new_index = construct_index(df = df, index = prior_index)
        with open(x_path, 'w') as new_f:
            json.dump(new_index, new_f, sort_keys=True, indent=4)


scraped_db = pd.read_csv(CSV_NAME).rename(columns={'Unnamed: 0':'SN'}).reset_index(drop=True)
scraped_db.head()

def preprocess_df(df):
    df.Title = df.Title.apply(tp1)
    df.Author = df.Author.str.lower()
    df = df.drop(columns=['Author','Published'], axis=1)
    return df

processed_db = scraped_db.copy()
processed_db = preprocess_df(processed_db)
processed_db.head()


# single_row = scraped_db.loc[1,:].copy()
# tp1(single_row['Title'])
# lematize(tp1(single_row['Title']))

indexed = full_index(processed_db,
                     index = {})
indexes = construct_index(df=scraped_db,
                          index = {})
with open('indexes.json', 'w') as new_f:
    json.dump(indexes, new_f, sort_keys=True, indent=4)

with open('indexes.json', 'r') as file:
    data = json.load(file)

def split_query(terms):
    each = tp1(terms)
    return each.split()

def union(lists):
    union = list(set.union(*map(set, lists)))
    union.sort()
    return union

def intersection(lists):
    intersect = list(set.intersection(*map(set, lists)))
    intersect.sort()
    return intersect

def vertical_search_engine(df, query, index):
    query_split = split_query(query)
    retrieved = []
    for word in query_split:
        if word in index.keys():
            retrieved.append(index[word])
    if len(retrieved) > 0:
        high_rank_result = intersection(retrieved)
        low_rank_result = union(retrieved)
        c = [x for x in low_rank_result if x not in high_rank_result]
        high_rank_result.extend(c)
        result = high_rank_result

        final_output = df[df.SN.isin(result)].reset_index(drop=True)

        dummy = pd.Series(result, name = 'SN').to_frame()
        result = pd.merge(dummy, final_output, on='SN', how = 'left')
    else:
        result = 'No result found'
    return result