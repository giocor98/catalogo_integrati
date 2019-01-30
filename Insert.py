import urllib.request as ur
from bs4 import BeautifulSoup
import json
#import urllib2

#Variabile per far continuare l'esecuzione
goon = 1
main_link = "http://www.alldatasheet.com/view.jsp?Searchword="
Catalogo = list()
Actual_Circuit_Impostation = dict()
CatalogFile = "./data/Catalog.json"

def SaveCatalog():
    global Catalogo
    global CatalogFile
    try:
        with open(CatalogFile, 'w') as filehandle:
            json.dump(Catalogo, filehandle)
    except:
        print("!!! Attenzione,  non sono riuscito a trovare il file per salvare!!")
        print("nome file: " + CatalogFile)
        answ = input("Premere 'r' per riprovare a salvare...")
        if answ =="r":
            SaveCatalog()

def ReadCatalog():
    global Catalogo
    global CatalogFile
    try:
        with open(CatalogFile, 'r') as filehandle:
            Catalogo = json.load(filehandle)
    except:
        print("!!! Attenzione: non sono riuscito a trovare il catalogo!!")


def SetActualImpostation(luogo = "", categoria = list(), SogliaCritica = 0, numero_pezzi = 0):
    global Actual_Circuit_Impostation
    Actual_Circuit_Impostation["nome"] = ""
    Actual_Circuit_Impostation["descrizione"] = ""
    Actual_Circuit_Impostation["categoria"] = categoria
    Actual_Circuit_Impostation["DS_file"] = ""
    Actual_Circuit_Impostation["DS_link"] = ""
    Actual_Circuit_Impostation["N_pezzi"] = numero_pezzi
    Actual_Circuit_Impostation["luogo"] = luogo
    Actual_Circuit_Impostation["soglia_critica"] = SogliaCritica

def ImpostaActualImpostation():
    #Imposto il Actual_Circuit_Impostation
    info = [{"param" : "luogo" , "type" : "str"}, {"param" : "categoria" , "type" : "list"}, {"param" : "SogliaCritica" , "type" : "int"}, {"param" : "numero_pezzi" , "type" : "int"}]
    par = list()
    i = 0
    for i in range(4):
        answ = input("Imposta " + info[i]["param"] + ": ")
        if answ == "":
            break
        if info[i]["type"] == "str":
            par.append(answ)
        elif info[i]["type"] == "list":
            par.append(answ.split())
        elif info[i]["type"] == "int":
            par.append(int(answ))
    if len(par) == 1:
        SetActualImpostation(par[0])
    elif len(par) == 2:
        SetActualImpostation(par[0], par[1])
    elif len(par) == 3:
        SetActualImpostation(par[0], par[1], par[2])
    elif len(par) == 4:
        SetActualImpostation(par[0], par[1], par[2], par[3])
    return

def PrintCatalog():
    global Catalogo
    print("Esistono " + str(len(Catalogo)) + " circuiti catalogati:")
    for C in Catalogo:
        print("Nome : " + C["nome"])
        print("Descrizione : " + C["descrizione"])
        #print("categorie : " + C["categoria"])
        print("DS : " + C["DS_link"])
        print("Nummero pezzi : " + str(C["N_pezzi"]))
        print("Locazione : " + C["luogo"])
        print("Soglia : " + str(C["soglia_critica"]))
        print()
        print()

def CalcCategoria (desc):
    global Actual_Circuit_Impostation
    cat = list()
    for x in Actual_Circuit_Impostation["categoria"]:
        cat.append(x)
    for x in desc.split():
        cat.append(x)
    return cat

def AddCircuit(spec):
    global Catalogo
    Circuit = dict()
    Circuit["nome"] = spec["nome"]
    Circuit["descrizione"] = spec["descrizione"]
    Circuit["categoria"] = CalcCategoria(spec["descrizione"])
    Circuit["DS_file"] = "NONE"
    Circuit["DS_link"] = spec["DS_link"]
    n = ""
    if (Actual_Circuit_Impostation["N_pezzi"]> 0):
        n = input("Settati " + str(Actual_Circuit_Impostation["N_pezzi"]) + " pezzi, confermi? (y/null per confermare)")
        if ((n == "y") or(n == "")):
            n = Actual_Circuit_Impostation["N_pezzi"]
    if (n== ""):
        while (1):
            n = input("Numero pezzi ")
            try:
                n = int(n)
                break
            except:
                if n=="e":
                    return
                else:
                    continue
    Circuit["N_pezzi"] = n
    Circuit["luogo"] = Actual_Circuit_Impostation["luogo"]
    Circuit["soglia_critica"] = Actual_Circuit_Impostation["soglia_critica"]

    Catalogo.append(Circuit)
    return

def insert():
    global  main_link
    #inserisce il circuito nel catalogo
    nome = input("Inserire nome del circuito ['' per ucire]")
    if ((type(nome) != str) or (len(nome) == 0)):
        #se il nome inserito no è valido ritorna al chiamante
        return

    #costruisco il link a cui cercare i DS
    link = main_link+nome

    #Scarico la pagina html
    resp = ur.urlopen(link)
    html = resp.read()

    #Parso l'html
    parsed_html = BeautifulSoup(html, "html.parser")
    table = parsed_html.findAll("table", {"class" : "main"})

    #creo la lista per contenere le info sul circuito
    row = list()

    for x in table:
        IsThisTable = 0
        righe = x.findAll("tr")
        #Cerco gli elementi della taabella che mi servono
        for y in righe:
            if (IsThisTable == 1):
                stL = y.findAll("td")
                st = dict()
                if (len(stL)==3):
                    st["nome"] = (str(stL[0].getText())).strip()
                    st["descrizione"] = (str(stL[2].getText())).strip()
                    st["DS_link"] = (str((stL[1].find("a"))["href"])).strip()
                    row.append(st)
                elif (len(stL)==4):
                    st["nome"] = (str(stL[1].getText())).strip()
                    st["descrizione"] = (str(stL[3].getText())).strip()
                    st["DS_link"] = (str((stL[2].find("a"))["href"])).strip()
                    row.append(st)


            if ("Electronic Manufacturer" in str(y)):
                IsThisTable = 1

    #Scrivo quanti elementi ho trovato
    print ("Trovati: " + str(len(row)))

    answ = ""
    #Chiedo se la descrizione corrisponde
    while ((answ !="y") and (answ!= "n") and (answ != "e")):
        answ  = input("Il circuito è un '" + row[0]["descrizione"] +"'? (y/n)")
        try:
            answ = answ.lower()
            answ = answ[0]
        except:
            continue
    #Se l'untente schiaccia e esce dalla funzione
    if (answ == "e"):
        return
    #Se la descrizione corrisponde
    if (answ == "y"):
        #aggiungo il circuito di row(0)
        AddCircuit(row[0])
    else:
        #faccio scegliere la corrispondenza migliore
        n = 0
        print("Ecco cosa ho trovato:")
        for elem in row:
            print(str(n) + "\t: " + elem["nome"] + " ; " + elem["descrizione"])
            n = n+1
        while (1):
            answ = input("Quale scelgo? [inserire il numero o 'e' per uscire]")
            try:
                answ = int(answ)
                break
            except:
                if (answ == 'e'):
                    return
                continue
        if ((answ >= 0) and (answ < len(row))):
            AddCircuit(row[answ])
    return


def main():
    global goon
    #Setta Variabili globali:
    SetActualImpostation()
    #Carica catalogo
    ReadCatalog()

    #scegliere azione:
    while (goon !=0):
        #Sceglie azione
        action = input("Prossima azione? [I -> inserisci, E -> exit]\n")
        if (type(action)!= str):
            print("Errore: scelta non valida: non è una stringa")
            print(action)
            continue

        if (len(action)<1):
            continue

        try:
            action = action.lower()
        except:
            print("Errore: scelta non valida, e/E per uscire [non hai inserito una stringa]")
            print(action)
            continue

        if (len(action)>1):
            #se la stringa immessa ha lunghezza superiore a 1
            print("Errore: Stringa troppo lunga")
            continue

        if(action == "i"):
            #se scelto i/I inserisci circuito
            insert()
        elif(action == "e"):
            #se scelto e/E esce dal programma
            goon = 0;
        elif(action == "s"):
            #se scelto s/S vado a impostare il Actual_Circuit_Impostation
            ImpostaActualImpostation()
        elif(action == "p"):
            #se scelto p/P printa il catalogo
            PrintCatalog()
        elif(action == "q"):
            #se scelto q/Q salvo il catalogo
            answ = ""
            while((answ!="y") and (answ!="n")):
                answ = (input("Vuoi salvare il catalogo aggiornato? [ y/n]")).lower()
            if (answ == "y"):
                SaveCatalog()
        else:
            print("Errore: scelta non valida, e/E per uscire")
            continue
    answ = ""
    while((answ!="y") and (answ!="n")):
        answ = (input("Do you want to save before quitting? [ y/n]")).lower()
    if (answ == "y"):
        SaveCatalog()





main()
# http://www.alldatasheet.com/view.jsp?Searchword=ATMEGA328
