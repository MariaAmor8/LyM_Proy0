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
    
def analizeDefVar(token,sigTok,tokensList,lstVar):
    """
    alg para analizar la estructura de definir variable -> falta incluir las variables en el lenguaje
    """
    if sigTok['type'] == 1:
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            #diccVar = {'NomVar': token['value'],'Valor':sigTok['value']}
            if sigTok['type'] == 2:
                diccVar = {'NomVar': token['value'],'Valor':sigTok['value']}
                lstVar.append(diccVar)
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

def analizeCommandValue(token,sigTok,tokensList):
    if sigTok['value'] == '(':
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigSigTok = sigToken(sigTok,tokensList)
        if sigTok['type'] == 2 and sigSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
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

def analizeWalkLeap(token,sigTok,tokensList):
    directions = ['north','south','west','east', 'left','right','around']
    ssTok = sigToken(sigTok,tokensList)
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

def analizeJump(token,sigTok,tokensList):
    if sigTok['value'] == '(':
        tokensList.pop(tokensList.index(token))
        token = sigTok
        sigTok = sigToken(token,tokensList)
        sigSigTok = sigToken(sigTok,tokensList)
        sigSigsigTok = sigToken(sigSigTok,tokensList)
        SSSSigTok= sigToken(sigSigsigTok,tokensList)
        if sigTok['type'] == 2 and sigSigTok['value'] == ',' and sigSigsigTok['type'] == 2 and SSSSigTok['value'] == ')':
            tokensList.pop(tokensList.index(token))
            tokensList.pop(tokensList.index(sigTok))
            tokensList.pop(tokensList.index(sigSigTok))
            tokensList.pop(tokensList.index(sigSigsigTok))
            tokensList.pop(tokensList.index(sigSigsigTok))
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
        tokensList= analizeStr(tokensList[0],tokensList,lstVar)
        if tokensList != False:
            if tokensList[0]['value'] == '}':
                tokensList.pop(0)
            else:
                tokensList = False
    else:
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

def analizeDefProc(token,sigTok,tokensList):
    if sigTok['type'] == 1:
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            if sigTok['value'] == '(':
                tokensList.pop(tokensList.index(token))
                token = sigTok
                sigTok = sigToken(token,tokensList)
                if sigTok['type'] == 1:
                    tokensList.pop(tokensList.index(token))
                    token = sigTok
                    sigTok = sigToken(token,tokensList)
                    sigSigTok = sigToken(sigTok,tokensList)
                    while sigTok['value'] == ',' and token['type'] == 1 and sigSigTok['type'] == 1:
                        tokensList.pop(tokensList.index(token))
                        tokensList.pop(tokensList.index(sigTok))
                        token = sigSigTok
                        sigTok = sigToken(token,tokensList)
                        if sigTok['value'] != ')':
                            sigSigTok = sigToken(sigTok,tokensList)
                    if sigTok['value'] == ')':
                        tokensList.pop(tokensList.index(token))
                        tokensList.pop(tokensList.index(sigTok))
                    else:
                        tokensList = False
                
                elif sigTok['value'] == ')':
                    tokensList.pop(tokensList.index(token))
                    tokensList.pop(tokensList.index(sigTok))
                else:
                    tokensList = False 
            else:
                tokensList = False
    else:
        tokensList = False
        
    return tokensList
    
def analizeStr(token,tokensList,lstVar):
    sigTok = sigToken(token,tokensList)
    if token['value'] == "defvar":
        tokensList = analizeDefVar(token,sigTok,tokensList,lstVar)
            
    elif token['value'] == "defproc":
        tokensList = analizeDefProc(token,sigTok,tokensList)
        
    elif token['value'] == 'turn':
        tokensList = analizeTurn(token,sigTok,tokensList)
        
    elif token['value'] == 'turnto' or token['value'] == 'facing':
        tokensList = analizeTurnTo(token,sigTok,tokensList)
        
    elif token['value'] == 'drop' or token['value'] == 'get'or token['value'] == 'grab' or token['value'] == 'letgo':
        tokensList = analizeCommandValue(token,sigTok,tokensList)

    elif token['value']=='jump':
        tokensList=analizeJump(token,sigTok,tokensList)
    
    elif token['value']=='walk' or token['value']=='leap':
        tokensList=analizeWalkLeap(token,sigTok,tokensList)
        
    elif token['value'] == 'nop':
        tokensList = analizeNop(token,sigTok,tokensList)
        
    elif token['value'] == 'can':
        tokensList = analizeCan(token,sigTok,tokensList,lstVar)
        
    elif token['value'] == 'not':
        tokensList = analizeNot(token,sigTok,tokensList,lstVar)
        
    elif token['value'] == 'if':
        tokensList = analizeConditional(token,sigTok,tokensList,lstVar)
        
    elif token['value'] == 'while':
        tokensList = analizeLoop(token,sigTok,tokensList,lstVar)
        
    else:
        tokensList = False
    
    return tokensList
    
def read(token,tokensList,lstVar):
    if token["type"] == 1:
        tokensList = analizeStr(token,tokensList,lstVar)
    else:
        tokensList = False
    return tokensList

def ejecutar():
    lista = Tokenizar('hello.txt')
    lstVar = []
    while lista:
        lista = read(lista[0],lista,lstVar)
        #si no se cumple alguna condición en la estructura analizada, en vez de una lista, se retorna false
        try:
            if lista[0]['type'] == 0 or lista == []:
                lista = False
                rta = True
        except:
            rta = False
    print("lista de variables -> " + str(lstVar))
    print(rta)
     
ejecutar()
