import tokenize

def Tokenizar(archivo):
    tokensList = []
    pos = 0
    with tokenize.open(archivo) as f:
        tokens = tokenize.generate_tokens(f.readline)
        for token in tokens:
            if token[0] != 61 and token[0] != 4:
                diccToken = {'type':token[0],'value':token[1]}
                tokensList.append(diccToken)
                pos += 1
    print(tokensList)
    return tokensList
            

def sigToken(token,tokensList):
    sigTok = tokensList[tokensList.index(token)+1]
    return sigTok
    
def analizeDefVar(token,sigTok,tokensList):
    if sigTok['type'] == 1:
            tokensList.pop(tokensList.index(token))
            token = sigTok
            sigTok = sigToken(token,tokensList)
            if sigTok['type'] == 2:
                tokensList.pop(tokensList.index(token))
                tokensList.pop(tokensList.index(sigTok))
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
                        tokensList[0] = {'type': 'error', 'value': 'error'}
                else:
                    tokensList[0] = {'type': 'error', 'value': 'error'}  
            else:
                tokensList[0] = {'type': 'error', 'value': 'error'} 
    else:
        tokensList[0] = {'type': 'error', 'value': 'error'}
    return tokensList
    
def analizeStr(token,tokensList):
    sigTok = sigToken(token,tokensList)
    if token['value'] == "defVar":
        tokensList = analizeDefVar(token,sigTok,tokensList)
            
    elif token['value'] == "defProc":
        tokensList = analizeDefProc(token,sigTok,tokensList)
    
    return tokensList
    
def read(token,tokensList):
    if token["type"] == 1:
        tokensList = analizeStr(token,tokensList)
    elif token["type"] == 2:
        print("num")
    elif token["type"] == 54:
        print("operator")
    #print(tokensList)
    return tokensList

def ejecutar():
    lista = Tokenizar('hello.txt')
    while not lista[0]['type'] == 0 or not lista[0]['type'] == 'error':
        print(lista[0]['type'])
    
        lista = read(lista[0],lista)
        #print(lista)
     
ejecutar()
