import nltk
from collections import defaultdict
import word2int as convert
import inflect

# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')

class Reader:
    def __init__(self):
        command = input("enter your command: ")
        command = command.lower()
        self.tags = command
        self.currentVerb = ""
        self.currentNum = 1
        self.flag = 0
        self.result = defaultdict(list)

    def getDict(self):
        p = inflect.engine()
        tokens = nltk.word_tokenize(self.tags)
        tags = nltk.pos_tag(tokens)
        print(tags)
        basicActions = ["walk", "jump", "turn", "crouch"]
        for word, POS in tags:
            if word not in basicActions:
                s1 = set(word.split("-"))
                s2 = set(convert.american_number_system.keys())
                if s1 & s2:
                    self.currentNum = convert.word_to_num(word)
                    continue
                if word in convert.american_number_system.keys():
                    self.currentNum = convert.american_number_system[word]
                if POS == "VB" or POS == "VBD" or POS == "JJ":
                    self.flag = 1
                    self.currentVerb = word
                if POS == "CD":
                    try:
                        self.currentNum = convert.word_to_num(word)
                    except ValueError:
                        self.currentNum = 1
                if self.flag == 1 and (POS == "NN" or POS == "NNS"):
                    if p.singular_noun(word):
                        self.result[self.currentVerb].append([p.singular_noun(word), self.currentNum])
                    else:
                        self.result[self.currentVerb].append([word, self.currentNum])
                    self.currentNum = 1
            elif word in basicActions:
                self.result[word] = []
        return self.result
