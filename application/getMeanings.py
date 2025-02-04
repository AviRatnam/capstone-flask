
def get_meanings(summarized_text, distractor_list):
    import nltk
    from nltk.tokenize import word_tokenize
    from nltk.corpus import stopwords
    import string
    from string import punctuation
    from flashtext import KeywordProcessor
    from sklearn.metrics.pairwise import cosine_similarity
    from sklearn.feature_extraction.text import CountVectorizer
    from collections import defaultdict

    stopwords = stopwords.words('english')

    from PyDictionary import PyDictionary
    dict = PyDictionary()

    def classify_word(word)  #input is array of words
        new_words = {}
        text_tokenized = word_tokenize(text)
        pos_word = {k.lower():v for k,v in nltk.pos_tag(text_tokenized)}
        vocab_pos = defaultdict(list)
        for w,t in nltk.pos_tag(text):
            vocab_pos[t].append(w.lower())

        for word, word_type in pos_word.items():
            if(word not in set(punctuation)):
                if(word_type[0] in ['V','N','J','P','R']):
                    print(word,":", word_type)
                    new_words.update({word:word_type})

        return new_words
    
    def get_meaning(keywords):
        meanings = {}
        for i in keywords:
            meanings.update({i:dict.meaning(i)})
        return meanings
    
    def clean_string(text):
        text = ''.join([word for word in text if word not in string.punctuation])
        text = text.lower()
        text = ' '.join([word for word in text.split() if word not in stopwords])
        return text  

    def cosine_sim_vectors(vec1,vec2):
        vec1 = vec1.reshape(1,-1)
        vec2 = vec2.reshape(1,-1)
        return cosine_similarity(vec1,vec2)[0][0]
    
    def get_meaning_brute(words,definitions):
        keyword = words
        sentences = [text]
        finaldef = {}

        # for i in range(len(definition)):
        for key in definitions:
            for i in definitions[key]:
            sentences.append(i)

        cleaned_text = list(map(clean_string,sentences))  #cleaning each sentence
        vectorizer  = CountVectorizer().fit_transform(cleaned_text)
        vectors = vectorizer.toarray()
        csim = cosine_similarity(vectors)  #similarity between sentences

        for i in range(1,len(sentences)):  # comparing all sentences with each other
            result = cosine_sim_vectors(vectors[0],vectors[i])
            if (result != 0 and result !=1):
            finaldef[keyword] = sentences[i]

        return finaldef
    
    def get_word_meanings():
        list_of_defs_brute=[]

        for i in imp_keywords:
            if(meanings[i] != None):
            list_of_defs_brute.append((get_meaning_brute(i,meanings[i])))

        return list_of_defs_brute