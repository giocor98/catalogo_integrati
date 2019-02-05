import urllib.request as ur
import Naviga as Nv
from bs4 import BeautifulSoup
import json
import os

#Variabile per far continuare l'esecuzione
goon = 1
main_link = "http://www.alldatasheet.com/view.jsp?Searchword="
Catalogo = list()
Actual_Circuit_Impostation = dict()
CatalogFile = "./data/Catalog.json"
TmpFile = "./data/.tmpCatalog.json"
FirstId = 0

def SaveCatalog():
    global Catalogo
    global CatalogFile
    global TmpFile
    try:
        with open(CatalogFile, 'w') as filehandle:
            json.dump(Catalogo, filehandle)
        try:
            os.remove(TmpFile)
            print("Eliminato file temporaneo")
        except:
            print("Non c'è file temporaneo.\nCatalogo salvato correttamente")
    except:
        print("!!! Attenzione,  non sono riuscito a trovare il file per salvare!!")
        print("nome file: " + CatalogFile)
        answ = input("Premere 'r' per riprovare a salvare...")
        if answ =="r":
            SaveCatalog()


def SaveTmp():
    global Catalogo
    global TmpFile
    try:
        with open(TmpFile, 'w') as filehandle:
            json.dump(Catalogo, filehandle)
    except:
        print("non hosalvato sul file temporaneo")

def ReadCatalog():
    global Catalogo
    global CatalogFile
    global FirstId
    global TmpFile
    try:
        try:
            f = open(TmpFile, 'r')
            a = (input("Ripristino il file emporano?")).lower()
            if a == "y":
                Catalogo = json.load(f)
                f.close()
                return
            f.close()
        except:
            Catalogo= Catalogo
        with open(CatalogFile, 'r') as filehandle:
            Catalogo = json.load(filehandle)
        FirstId = Catalogo[-1]["id"] + 1
    except:
        print("!!! Attenzione: non sono riuscito a trovare il catalogo!!")

def SearchName(name):
    global Catalogo
    i = 0
    for x in Catalogo:
        if x["nome"].lower() == name.lower():
            return i
        i = i+1
    return "NULL"


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

#funzionne che printa il chip passatole per parametro; p_cat indica se deve printare pure le categorie del chip o meno
def PrintChip(Chip, p_cat= 0):
    print("Nome : " + Chip["nome"] + "\t\t\t|| id: " + str(Chip["id"]))
    print("Descrizione : " + Chip["descrizione"])
    if (p_cat !=0):
        print("Categorie:")
        for cat in Chip["categoria"]:
            print("\t\t"+ cat)
    print("DS : " + Chip["DS_link"])
    print("Nummero pezzi : " + str(Chip["N_pezzi"]))
    print("Locazione : " + Chip["luogo"])
    if (Chip["soglia_critica"]>0):
        print("Soglia Critica: " + str(Chip["soglia_critica"]))
        if (Chip["soglia_critica"]<Chip["N_pezzi"]):
            print("!!Siamo sotto la soglia critica!!")

def PrintCatalog():
    global Catalogo
    print("Esistono " + str(len(Catalogo)) + " circuiti catalogati:")
    for C in Catalogo:
        PrintChip(C)
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
    global FirstId
    Circuit = dict()
    i = SearchName(spec["nome"])
    if type(i) == int:
        print("!!!! ATTENZIONE !!!\nEsiste già un circuito con lo stesso nome:")
        PrintChip(Catalogo[i])
        tmp = 1
        while tmp:
            answ = (input("Cosa faccio? c-> cra nuovo, a -> aggiunngi pezzi al precedennte")).lower()
            if answ == "a":
                answ = input("quanti pezzi aggiungo?")
                try:
                    answ = int(answ)
                    Catalogo[i]["N_pezzi"] = Catalogo[i]["N_pezzi"] + answ
                    tmp = 0
                    print("attualmente ci sono " + str(Catalogo[i]["N_pezzi"]) + " pezzi")
                    return
                except:
                    print("Inserimento non valido")
            elif answ == "c":
                tmp = 0
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
    Circuit["id"] = FirstId
    FirstId = FirstId+1
    Catalogo.append(Circuit)
    SaveTmp()
    return

def ManualInsert():
    spec = dict()
    print("Inserimento manuale del ciruito")
    spec["nome"] = input("Inserire nome del cirtuito")
    spec["descrizione"] = input("Innserire descrizione del circuito")
    spec["DS_link"] = input("Inserire link a DataSheet ('' se non disponibile)")
    answ = input("Completo l'inserimento?[y/n]")
    if (answ.lower() == "y"):
        AddCircuit(spec)
    return

def insert():
    global  main_link
    #inserisce il circuito nel catalogo
    nome = input("Inserire nome del circuito ['' per ucire]\n")
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
    global Catalogo
    #Setta Variabili globali:
    SetActualImpostation()
    #Carica catalogo
    ReadCatalog()

    #scegliere azione:
    while (goon !=0):
        #Sceglie azione
        action = input("Prossima azione? [I -> inserisci, Q -> exit, N -> naviga]\n")
        if (type(action)!= str):
            print("Errore: scelta non valida: non è una stringa")
            print(action)
            continue

        if (len(action)<1):
            continue

        try:
            action = action.lower()
        except:
            print("Errore: scelta non valida, q/Q per uscire [non hai inserito una stringa]")
            print(action)
            continue

        if (len(action)>1):
            #se la stringa immessa ha lunghezza superiore a 1
            print("Errore: Stringa troppo lunga")
            continue

        if(action == "i"):
            #se scelto i/I inserisci circuito
            insert()
        elif(action == "s"):
            #se scelto s/S vado a impostare il Actual_Circuit_Impostation
            ImpostaActualImpostation()
        elif(action == "p"):
            #se scelto p/P printa il catalogo
            PrintCatalog()
        elif (action=="n"):
            Catalogo = Nv.naviga(Catalogo)
        elif (action == "e"):
            #Se scelto e/E informo che per uscire bisogna usare q
            print("Per uscire devi premere q")
        elif (action=="m"):
            ManualInsert()
        elif(action == "q"):
            #se scelto q/Q salvo il catalogo e esco
            answ = ""
            while((answ!="y") and (answ!="n")):
                answ = (input("Vuoi salvare il catalogo aggiornato? [y/n]")).lower()
            if (answ == "y"):
                SaveCatalog()
            answ =""
            while((answ!="y") and (answ!="n")):
                answ = (input("Vuoi uscire dal programma? [y/n]")).lower()
            if (answ == "y"):
                goon = 0
        else:
            print("Errore: scelta non valida, q/Q per uscire")
            continue

main()
# http://www.alldatasheet.com/view.jsp?Searchword=ATMEGA328
