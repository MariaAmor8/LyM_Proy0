import tokenize


def Tokenizar(archivo):
    """
    Funcion para tokenizar el archivo leido
    """
    tokensList = []
    with tokenize.open(archivo) as f:
        tokens = tokenize.generate_tokens(f.readline)
        for token in tokens:
            if token[0] != 61 and token[0] != 4:
                diccToken = {'type':token[0],'value':token[1].lower()}
                tokensList.append(diccToken)
    print(tokensList)
    return tokensList
            

def sigToken(token,tokensList):
    """
    funcion que retorna el siguiente token
    """
    sigTok = tokensList[tokensList.index(token)+1]
    return sigTok
    
def analizeDefVar(token,sigTok,tokensList,DiccVar):
    """
    alg para analizar la estructura de definir variable -> falta incluir las variables en el lenguaje
    """
    if sigTok['type'] == 1:
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            if sigTok['type'] == 2:
                DiccVar['lstVar'].append(token['value'])
                DiccVar['diccVar'][token['value']] = sigTok['value']
                tokensList.pop(tokensList.index(token))
                tokensList.pop(tokensList.index(sigTok))
            else:
                tokensList = False 
    else:
        tokensList = False
    return tokensList

def analizeTurn(token,sigTok,tokensList):
    directions = ['left','right','around']
    if sigTok['value'] == '(':
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigSigTok = sigToken(sigTok,tokensList)
        if sigTok['value'] in directions and sigSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
        else:
            tokensList = False 
    else:
        tokensList = False
    return tokensList

def analizeTurnTo(token,sigTok,tokensList):
    directions = ['north','south','west','east']
    if sigTok['value'] == '(':
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigSigTok = sigToken(sigTok,tokensList)
        if sigTok['value'] in directions and sigSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
        else:
            tokensList = False 
    else:
        tokensList = False
    return tokensList

def analizeCommandValue(token,sigTok,tokensList,DiccVar):
    if sigTok['value'] == '(':
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigSigTok = sigToken(sigTok,tokensList)
        if sigTok['type'] == 2 and sigSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
        elif sigTok['type'] == 1 and sigSigTok['value'] == ')' and sigTok['value'] in DiccVar['lstVar']:
            valor = DiccVar['diccVar'][sigTok['value']]
            try:
                nv = int(valor)
                tokensList.pop(tokensList.index(token))
                tokensList.pop(tokensList.index(sigTok))
                tokensList.pop(tokensList.index(sigSigTok))
            except:
                tokensList = False
        else:
            tokensList = False 
    else:
        tokensList = False
    return tokensList

def analizeNop(token,sigTok,tokensList):
    sigSigTok = sigToken(sigTok,tokensList)
    if sigTok['value'] == '(' and sigSigTok['value'] == ')':
        tokensList.pop(tokensList.index(token))
        tokensList.pop(tokensList.index(sigTok))
        tokensList.pop(tokensList.index(sigSigTok))
    else:
        tokensList = False
    return tokensList

def analizeWalkLeap(token,sigTok,tokensList,Diccvar):
    listvar= Diccvar['lstVar']
    dictvar= Diccvar['diccVar']
    directions = ['north','south','west','east', 'left','right','around']
    ssTok = sigToken(sigTok,tokensList)
    if ssTok ['type'] == 1:
            if ssTok['value'] in listvar:
                ssTok['value']= dictvar[ssTok['value']] 
                try:
                    int(ssTok['value'])
                    ssTok['type']= 2
                except ValueError:
                    ssTok['type']= 1
    if sigTok['value'] == '(' and ssTok['type'] == 2:
        sssTok=sigToken(ssTok,tokensList)
        if sssTok['value'] ==')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(ssTok))
            tokensList.pop(tokensList.index(sssTok))
        elif sssTok['value'] ==',':
            ssssTok= sigToken(sssTok,tokensList)
            sssssTok= sigToken(ssssTok,tokensList)
            if ssssTok['value'] in directions and sssssTok['value'] == ')':
                tokensList.pop(tokensList.index(token))
                tokensList.pop(tokensList.index(sigTok))
                tokensList.pop(tokensList.index(ssTok))
                tokensList.pop(tokensList.index(sssTok))
                tokensList.pop(tokensList.index(ssssTok))
                tokensList.pop(tokensList.index(sssssTok))
            else:
                tokensList = False
        else:
            tokensList = False
    else:
            tokensList = False
    return tokensList

def analizeJump(token,sigTok,tokensList, Diccvar):
    listvar= Diccvar['lstVar']
    dictvar= Diccvar['diccVar']
    if sigTok['value'] == '(':
        try:
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            sigSigTok = sigToken(sigTok,tokensList)
            sigSigsigTok=sigToken(sigSigTok,tokensList)
            SSSSigTok= sigToken(sigSigsigTok,tokensList)
        except IndexError:
            tokensList = False 
        if sigTok['type'] == 1:
            if sigTok['value'] in listvar:
                sigTok['value']= dictvar[sigTok['value']] 
                try:
                    int(sigTok['value'])
                    sigTok['type']= 2
                except ValueError:
                    sigTok['type']= 1
        if sigSigsigTok['type'] == 1:
            if sigSigsigTok['value'] in listvar:
                sigSigsigTok['value']= dictvar[sigSigsigTok['value']] 
                try:
                    int(sigSigsigTok['value'])
                    sigSigsigTok['type']= 2
                except ValueError:
                    sigSigsigTok['type']= 1
            
        if sigTok['type'] == 2 and sigSigTok['value'] == ',' and sigSigsigTok['type'] == 2 and SSSSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
            tokensList.pop(tokensList.index(sigSigsigTok))
            tokensList.pop(tokensList.index(SSSSigTok))
        else:
            tokensList = False 
    else:
        tokensList = False
    return tokensList



def analizeCan(token,sigTok,tokensList,lstVar):
    ssTok = sigToken(sigTok,tokensList)
    if sigTok['value'] == '(' and ssTok['type'] == 1:
        tokensList.pop(tokensList.index(token))
        tokensList.pop(tokensList.index(sigTok))
        tokensList= analizeStr(ssTok,tokensList,lstVar)
        if tokensList != False:
            tokensList.pop(0)
    else:
        tokensList = False
    return tokensList

def analizeNot(token,sigTok,tokensList,lstVar):
    ssTok = sigToken(sigTok,tokensList)
    if sigTok['value'] == ':' and ssTok['value'] == 'facing' or ssTok['value'] == 'can':
        tokensList.pop(tokensList.index(token))
        tokensList.pop(tokensList.index(sigTok))
        tokensList= analizeStr(ssTok,tokensList,lstVar)
    else:
        tokensList = False
    return tokensList

def analizeBlock(tokensList,lstVar):
    if tokensList[0]['value'] == '{':
        tokensList.pop(0)
        s = True
        try:
            while tokensList[0]['type'] == 1 and s:
                tokensList = analizeStr(tokensList[0],tokensList,lstVar)
                if tokensList[0]['value'] == ';' and tokensList[1]['type'] == 1:
                    tokensList.pop(0)
                elif tokensList[0]['value'] != ';' and tokensList[0]['type'] == 1 and tokensList[1]['value'] != '}':
                    s = False
            if tokensList[0]['value'] != '}':
                tokensList = False
            else:
                tokensList.pop(0)
        except:
            tokensList = False
    return tokensList
        
def analizeConditional(token,sigTok,tokensList,lstVar):
    if sigTok['value'] == 'facing' or sigTok['value'] == 'can' or sigTok['value'] == 'nop':
        tokensList.pop(tokensList.index(token))
        tokensList= analizeStr(sigTok,tokensList,lstVar)
        if tokensList != False:
            tokensList = analizeBlock(tokensList,lstVar)
            if tokensList[0]['value'] == 'else':
                tokensList.pop(0)
                tokensList = analizeBlock(tokensList,lstVar)
        else:
            tokensList = False
    return tokensList

def analizeRepeat(token,sigTok,tokensList, Diccvar):
    listvar= Diccvar['lstVar']
    dictvar= Diccvar['diccVar']
    if sigTok['type'] == 1:
            if sigTok['value'] in listvar:
                sigTok['value']= dictvar[sigTok['value']] 
                try:
                    int(sigTok['value'])
                    sigTok['type']= 2
                except ValueError:
                    sigTok['type']= 1
    if sigTok['type'] == 2:
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigsigTok = sigToken(sigTok,tokensList)
        if  sigTok['value'] == 'times' and sigsigTok['value'] == '{':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList = analizeBlock(tokensList,Diccvar)
        else:
            tokensList = False
    else:
            tokensList = False
    return tokensList



def analizeLoop(token,sigTok,tokensList,lstVar):
    if sigTok['type'] == 1:
        tokensList.pop(tokensList.index(token))
        if sigTok['value'] == 'can':
            tokensList = analizeCan(tokensList[0],tokensList[1],tokensList,lstVar)
        elif sigTok['value'] == 'not':
            tokensList = analizeNot(tokensList[0],tokensList[1],tokensList,lstVar)
        elif sigTok['value'] == 'facing':
            tokensList = analizeTurnTo(tokensList[0],tokensList[1],tokensList)
        else:
            tokensList = False
        if  tokensList != False and tokensList[0]["value"] == '{':
            tokensList = analizeBlock(tokensList,lstVar)
    else:
        tokensList = False
    return tokensList

def analizeDefProc(token,sigTok,tokensList,DiccProc):
    tok=token['value']
    DiccProc={'listprocc':[], 'diccinfoproc':{}}
    lstprocc=DiccProc['listprocc']
    dictprocc=DiccProc['diccinfoproc']
    lista2=[]
    if sigTok['type'] == 1:
            lstprocc.append(token)
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            if sigTok['value'] == '(':
                tokensList.pop(tokensList.index(token))
                token = sigTok
                sigTok = sigToken(token,tokensList)
                if sigTok['type'] == 1:
                    lista2.append(token['type'])
                    tokensList.pop(tokensList.index(token))
                    token = sigTok
                    sigTok = sigToken(token,tokensList)
                    sigSigTok = sigToken(sigTok,tokensList)
                    while sigTok['value'] == ',' and token['type'] == 1 and sigSigTok['type'] == 1:
                        lista2.append(token['type'])
                        lista2.append(sigTok['type'])
                        tokensList.pop(tokensList.index(token))
                        tokensList.pop(tokensList.index(sigTok))
                        token = sigSigTok
                        sigTok = sigToken(token,tokensList)
                        if sigTok['value'] != ')':
                            sigSigTok = sigToken(sigTok,tokensList)
                        else:
                            lista2.append(sigTok['type'])
                    if sigTok['value'] == ')':
                        tokensList.pop(tokensList.index(token))
                        tokensList.pop(tokensList.index(sigTok))
                    else:
                        tokensList = False
                
                elif sigTok['value'] == ')':
                    lista2.append(token['type'])
                    lista2.append(sigTok['type'])
                    tokensList.pop(tokensList.index(token))
                    tokensList.pop(tokensList.index(sigTok))
                else:
                    tokensList = False 
            else:
                tokensList = False
    else:
        tokensList = False
    dictprocc[tok]=lista2
    print(DiccProc)
    return tokensList


def analizeDefProcP2(token,sigTok,tokensList,lstVar):
    if tokensList[0]['value'] == '{':
        tokensList = analizeBlock(tokensList,lstVar)
    else:
        tokensList = False
    return tokensList
    
def analizeStr(token,tokensList,DiccVar):
    sigTok = sigToken(token,tokensList)
    if token['value'] == "defvar":
        tokensList = analizeDefVar(token,sigTok,tokensList,DiccVar)
            
    elif token['value'] == "defproc":
        tokensList = analizeDefProc(token,sigTok,tokensList)
        if tokensList != False:
            tokensList = analizeDefProcP2(token,sigTok,tokensList,DiccVar)
            
    elif token['value'] == 'turn':
        tokensList = analizeTurn(token,sigTok,tokensList)
        
    elif token['value'] == 'turnto' or token['value'] == 'facing':
        tokensList = analizeTurnTo(token,sigTok,tokensList)
        
    elif token['value'] == 'drop' or token['value'] == 'get'or token['value'] == 'grab' or token['value'] == 'letgo':
        tokensList = analizeCommandValue(token,sigTok,tokensList,DiccVar)

    elif token['value']=='jump':
        tokensList=analizeJump(token,sigTok,tokensList,DiccVar)
    
    elif token['value']=='walk' or token['value']=='leap':
        tokensList=analizeWalkLeap(token,sigTok,tokensList,DiccVar)
        
    elif token['value'] == 'nop':
        tokensList = analizeNop(token,sigTok,tokensList)
        
    elif token['value'] == 'can':
        tokensList = analizeCan(token,sigTok,tokensList,DiccVar)
        
    elif token['value'] == 'not':
        tokensList = analizeNot(token,sigTok,tokensList,DiccVar)
        
    elif token['value'] == 'if':
        tokensList = analizeConditional(token,sigTok,tokensList,DiccVar)
        
    elif token['value'] == 'while':
        tokensList = analizeLoop(token,sigTok,tokensList,DiccVar)
        
    elif token['value'] == '{':
        tokensList = analizeBlock(tokensList,DiccVar)
    
    elif token['value'] == 'repeat':
        analizeRepeat(token,sigTok,tokensList, DiccVar)

    else:
        tokensList = False
    
    return tokensList
    
def read(token,tokensList,DiccVar):
    if token["type"] == 1 or token["type"] == 54:
        tokensList = analizeStr(token,tokensList,DiccVar)
    else:
        tokensList = False
        
    return tokensList

def ejecutar():
    lista = Tokenizar('hello.txt')
    DiccVar = {'lstVar': [],'diccVar':{}}
    while lista:
        lista = read(lista[0],lista,DiccVar)
        #si no se cumple alguna condición en la estructura analizada, en vez de una lista, se retorna false
        try:
            if lista[0]['type'] == 0 or lista == []:
                lista = False
                rta = True
        except:
            rta = False
    print("lista de variables -> " + str(DiccVar))
    print(rta)
     
ejecutar()