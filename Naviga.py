Catalogo = dict()
goon = 1
SelectedList = list()

def AddToList(listaElementi):
    global Catalogo
    global SelectedList
    SelectAll = 0
    print("Totale elementi da scegliere: " + str(len(listaElementi)))
    for x in listaElementi:
        if (SelectAll ==1):
            SelectedList.append(x)
            continue
        print()
        print("Seleziono il seguente elemento?")
        print("nome: " + Catalogo[x]["nome"] + "\t\t| Id: " + str(Catalogo[x]["id"]))
        print(Catalogo[x]["descrizione"])
        tmp = 1
        while(tmp):
            answ = (input("S Seleziona, C continua, M maggiori informazioni, A seleziona tutti")).lower()
            if (answ == "s"):
                SelectedList.append(x)
                tmp = 0
            elif (answ == "c"):
                tmp = 0
            elif (answ == "m"):
                print("DS: " + Catalogo[x]["DS_link"])
                print("Categorie:")
                for i  in Catalogo[x]["categoria"]:
                    print("\t" + i)
            elif(answ == "a"):
                SelectAll = 1
                SelectedList.append(x)
                tmp = 0

def FindId(Id):
    global Catalogo
    i = 0
    for x in Catalogo:
        if x["id"] == Id:
            return i
        i = i+1
    return -1

def Completa(mod, field, val):
    global Catalogo
    val = val.lower()
    clist = list()
    i = 0
    for x in Catalogo:
        if field in x:
            if type(x[field]) == str:
                if val in x[field].lower():
                    if (mod == 0):
                        if x[field].lower() not in clist:
                            clist.append(x[field].lower())
                    elif (mod == 1):
                        clist.append(i)
            elif type(x[field]) == list:
                for p in x[field]:
                    if val in p.lower():
                        if (mod == 0):
                            if p.lower() not in clist:
                                clist.append(p.lower())
                        elif (mod == 1):
                            if (i not in clist):
                                clist.append(i)
        i = i+1
    return clist

def Cerca():
    print("Le possibili scelte di cosa cercare sono:\n0\tId del circuito;\n1\tnome del circuito;\n2\tcategoria del circuito;\n3\tLuogo\nq to exit")
    answ = ""
    while (answ!="q"):
        answ = input("Cosa cerco?")
        try:
            answ = int(answ)
        except:
            continue
        if ((answ>=0) and (answ<4)):
            break
    if (answ == "q"):
        return
    if (answ == 0):
        print("Cerco in base all'id")
        Id = input("Inserire id cercato")
        try:
            Id = int(Id)
        except:
            print("Errore, l'id è un numero")
            return
        search = FindId(Id)
        if(search == -1):
            print("non ho trovato nessun elemento con l'id cercato")
        else:
            print("Trovato 1 elemento")
            t=list()
            t.append(search)
            AddToList(t)
    elif (answ== 1):
        tmp = 1
        while(tmp):
            answ = (input("Inserire nome del circuito da cercare")).lower()
            if(answ!=""):
                for x in Completa(0,"nome", answ):
                    print("Possibile: " + x)
            answ2 = input("Cerco?[y/n]")
            if (answ2 == "y"):
                AddToList(Completa(1,"nome", answ))
                tmp = 0
            elif (answ2 == 'q'):
                tmp = 0
    elif (answ== 2):
        tmp = 1
        while(tmp):
            answ = (input("Inserire categoria del circuito da cercare")).lower()
            if(answ!=""):
                for x in Completa(0,"categoria", answ):
                    print("Possibile: " + x)
            answ2 = input("Cerco?[y/n]")
            if (answ2 == "y"):
                AddToList(Completa(1,"categoria", answ))
                tmp = 0
            elif (answ2 == 'q'):
                tmp = 0
    elif (answ== 3):
        tmp = 1
        while(tmp):
            answ = (input("Inserire luogo del circuito da cercare")).lower()
            if(answ!=""):
                for x in Completa(0,"luogo", answ):
                    print("Possibile: " + x)
            answ2 = input("Cerco?[y/n]")
            if (answ2 == "y"):
                AddToList(Completa(1,"luogo", answ))
                tmp = 0
            elif (answ2 == 'q'):
                tmp = 0

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

def Elenca():
    global Catalogo
    global SelectedList
    salta = 0
    for x in SelectedList:
        elem = Catalogo[x]
        PrintChip(elem, 1)
        if (salta == 0):
            answ = ""
            while(answ!="y"):
                answ = (input("Contiuo?[y/e/s]")).lower()
                if (answ == "e"):
                    return
                elif (answ == "s"):
                    salta = 1
                    answ = "y"


def Imposta():
    global SelectedList
    global Catalogo
    print("!! seleezionati " + str(len(SelectedList)) + "elementi")
    tmp = 1
    while(tmp):
        answ = input("Cosa faccio? [u ->deseleziona, r -> rimuovi, q -> esci, p -> printa]")
        if (answ == "u"):
            tmp = 0;
            SelectedList = list()
        elif(answ == "p"):
            Elenca()
        elif(answ == "r"):
            ListaId= list()
            for x in SelectedList:
                ListaId.append(Catalogo[x]["id"])
            for x in ListaId:
                Catalogo.pop(FindId(x))
            SelectedList = list()
            tmp = 0
        elif (answ == "q"):
            tmp = 0

def selezione():
    global goon
    print("Modalità naviagazione:")
    goon = 1
    answ = ""
    while (goon):
        answ = input("Prossima azione? [C -> cerca, I -> imposta, Q -> ritorna a modalità precedente]")
        if ((type(answ)!=str)or(len(answ)<1)):
            print("Formato o lunghezza non validi")
            continue
        if(len(answ)>1):
            print("input troppo lungo troncato")
            answ = answ[0]
        answ = answ.lower()
        if (answ == "c"):
            #Se c/C ricerca
            Cerca()
        elif(answ == "i"):
            #Se I/i Imposta
            Imposta()
        elif(answ == "q"):
            goon = 0

def naviga(cat):
    global Catalogo
    Catalogo = cat
    selezione()
    return (Catalogo)
