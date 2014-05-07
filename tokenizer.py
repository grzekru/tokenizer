# -*- coding: utf-8 -*-

import sys
import re
import codecs

settingsFile = codecs.open("regexy.txt","r","utf-8")
settings = settingsFile.read().split('\n')
names = list()
tokens = list()
maxlen = 0

for i in range(0,len(settings)):
    settings[i] = settings[i].replace('\n','')
    settings[i] = settings[i].replace('\r','')
    names.append(settings[i][0:settings[i].find(":")])
    settings[i] = settings[i][settings[i].find(":")+1:len(settings[i])]

for line in sys.stdin:
    spans = list()
    line = line.replace('\n','')
    line = line.replace('\r','')

    for s in settings:
        p = re.compile(s)
        m = p.search(line)
        if (m is not None):
            spans.append([m.span()[0],m.span()[1]])

    tok = re.split("([^\w\dąęćżźłńóĄĘĆŻŹŁŃÓ0-1])",line)
    #tok = list(filter((' ').__ne__,tok))
    tok = list(filter(('').__ne__,tok))

    for s in spans:

        indexy = list()
        tleng = 0
        indexy.append(0)
        for i in range(0,len(tok)):
            tleng = tleng + len(tok[i])
            indexy.append(tleng)

        start = -1
        stop = -1
        licz = 0

        for idx in indexy:
            if (idx>=s[0] and idx<=s[1]-1 and start==-1):
                start = licz
            if (idx>=s[0]+1 and idx<=s[1]):
                stop = licz-1
            licz = licz + 1

        for i in range(start+1,stop+1):
            tok[start] = tok[start] + tok[i]
        for i in range(start+1,stop+1):
            del tok[start+1] 

    tok = list(filter((' ').__ne__,tok))

    def typ(t):
        for i in range(0,len(settings)):
            p = re.compile(settings[i])
            m = p.search(t)
            if (m is not None):
                if (m.group()==t):
                    return names[i]

        if (t=="."):
            return "Kropka"
        if (t==","):
            return "Przecinek"
        if (t=="!"):
            return "Wykrzyknik"
        if (t=="?"):
            return "Znak zapytania"
        if (t=="i"):
            return "Spójnik"
        if (t=="i"):
            return "Przyimek"

        p = re.compile("\d+")
        m = p.search(t)
        if (m is not None):
            if (m.group()==t):
                return "Liczba"

        p = re.compile("[\wąęćżźłńóĄĘĆŻŹŁŃÓ]+")
        m = p.search(t)
        if (m is not None):
            if (m.group()==t):
                return "Słowo"

        return "BRAK"
   
    for t in tok:
        if (len(t)>maxlen):
            maxlen = len(t)

    for t in tok:
        tokens.append(t)

for t in tokens:
    print(t + " "*(maxlen-len(t)) + "\t" + typ(t))
