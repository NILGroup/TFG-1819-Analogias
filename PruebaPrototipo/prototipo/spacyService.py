import spacy
import re
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import prototipo.spacyModel as spacyInstance



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

'''
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
'''

def genderAndNumberAPI(word):
    #print(word)
    #print("ENTRO A GENDER")
    obj = requests.get('https://holstein.fdi.ucm.es/nlp-api/analisis/'+word, verify=False).json()
    #print("PASADO PETICION")
    #print(obj['morfologico']['genero'])
    #print(obj['morfologico']['numero'])
    #print("LLEGO A LA API")
    #print(obj['morfologico']['parte'])

    if obj['morfologico']['parte'] == "nombre" or obj['morfologico']['parte'] == "adjetivo" :
        if 'genero' in obj['morfologico']:
            return obj['morfologico']['parte'], obj['morfologico']['genero'], obj['morfologico']['numero']
        else:
            return obj['morfologico']['parte'], "masculino", obj['morfologico']['numero']
    else:
        return obj['morfologico']['parte'], "", ""

def genderAndNumberSpacy(word):
    nlp = spacyInstance.SpacyIMP.__getModel__()
    doc = nlp(word)
    #print(doc[0].tag_)
    result_gender = re.match("NOUN__Gender=Masc", doc[0].tag_)
    #result_number = re.match("|Number=Sing", doc[0].tag_)
    result_number = re.match("Number=Plur", doc[0].tag_)

    #print(result_number)
    if result_gender != None:
        gender = "masculino"
        y = doc[0].tag_.replace('NOUN__Gender=Masc|', '')
        if re.match('Number=Plur', y) != None:
            number = "plural"
        else:
            number = "singular"
    else:
        gender = "femenino"
        y = doc[0].tag_.replace('NOUN__Gender=Fem|', '')
        if re.match('Number=Plur', y) != None:
            number = "plural"
        else:
            number = "singular"



    return gender, number




def phraseMaker(word):
    #print(word)
    #print("LLEGO")
    type, gender, number = genderAndNumberAPI(word)


    if type == "nombre" or "adjetivo":
        if gender == "masculino" and number == "singular":
            return "es un " + word
        elif gender == "masculino" and number == "plural":
            return "son unos " + word
        elif gender == "femenino" and number == "singular":
            return "es una " + word
        else:
            return "son unas " + word
    else:
        return "es " + word



def phraseMakerForHyponyms(word):
    #print(word)
    type, gender, number = genderAndNumberAPI(word)

    if type == "nombre" or "adjetivo":
        if gender == "masculino" and number == "singular":
            return "es como un " + word
        elif gender == "masculino" and number == "plural":
            return "son como unos " + word
        elif gender == "femenino" and number == "singular":
            return "es como una " + word
        else:
            return "son como unas " + word
    else:
        return "es como " + word