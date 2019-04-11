import spacy
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
nlp = spacy.load('es_core_news_sm')


def genderAndNumber(info):

    #print(token.tag_, token.text)
    result_gender = re.match("NOUN__Gender=Masc", info)
    result_number = re.match("|Number=Sing", info)
    #print(result_number)
    if result_gender != None:
        gender = "masculino"
    else:
        gender = "femenino"
    if result_number != None:
        number = "singular"
    else:
        number = "plural"

    return gender, number


def phraseMaker(synset):

    phrases = dict(phrase="", word="")
    phraseList = list()
    wordList = list()
    for syn in synset["synonyms"]:
        doc = nlp(syn)
        if doc[0].pos_ == "NOUN" or doc[0].pos_ == "ADJ" or doc[0].pos_ == "VERB":
            gender, number = genderAndNumberAPI(syn)
            wordList.append(syn)
            if gender == "masculino" and number == "singular":

                phraseList.append("es un")

            elif gender == "masculino" and number == "plural":
                phraseList.append("son unos")
            elif gender == "femenino" and number == "singular":
                phraseList.append("es una")
            else:
                phraseList.append("son unas")

    for syn in synset["hyperonyms"]:


        doc = nlp(syn)
        if doc[0].pos_ == "NOUN" or doc[0].pos_ == "ADJ" or doc[0].pos_ == "VERB":
            gender, number = genderAndNumberAPI(syn)
            wordList.append(syn)
            if gender == "masculino" and number == "singular":

                phraseList.append("es un")

            elif gender == "masculino" and number == "plural":
                phraseList.append("son unos")
            elif gender == "femenino" and number == "singular":
                phraseList.append("es una")
            else:
                phraseList.append("son unas")


    for syn in synset["hyponyms"]:
        doc = nlp(syn)
        if doc[0].pos_ == "NOUN" or doc[0].pos_ == "ADJ" or doc[0].pos_ == "VERB":
            gender, number = genderAndNumberAPI(syn)
            wordList.append(syn)
            if gender == "masculino" and number == "singular":

                phraseList.append("es como un")

            elif gender == "masculino" and number == "plural":
                phraseList.append("son como unos")
            elif gender == "femenino" and number == "singular":
                phraseList.append("es como una")
            else:
                phraseList.append("son como unas")

    phrases["phrase"] = phraseList
    phrases["word"] = wordList
   # print(phrases)
    return phrases


def genderAndNumberAPI(word):
    print("ENTRO A GENDER")
    obj = requests.get('https://holstein.fdi.ucm.es/nlp-api/analisis/'+word, verify=False).json()
    print("PASADO PETICION")
    #print(obj['morfologico']['genero'])
    #print(obj['morfologico']['numero'])
    print(obj['morfologico']['parte'])
    return obj['morfologico']['genero'], obj['morfologico']['numero']



def phraseMakerSynonym(word):
    print(word)
    gender, number = genderAndNumberAPI(word)

    if gender == "masculino" and number == "singular":
        return "es un " + word
    elif gender == "masculino" and number == "plural":
        return "son unos " + word
    elif gender == "femenino" and number == "singular":
        return "es una " + word
    else:
        return "son unas " + word
