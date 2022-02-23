userInput=['x','=','a','+','b','*','c','+','d'] # User input
# terminalSymbolsGrammar=input("Enter Terminal Symbols space Saperated: ").split() # Terminal Symbols in grammar
# NonterminalSymbolsGrammar=input("Enter Non Terminal Symbols space Saperated: ").split() # Non Terminal Symbols in grammar
terminalSymbolsGrammar=['=', '+', '*', 'id']
nonTerminalSymbolsGrammar=['S','E','T','F']
userInputWithoutIndentifiers=['id' if i not in ['=','+','*'] else i for i in userInput] # replace every identifer with 'id'
stack=['0']
userInputWithoutIndentifiers.append('$')
pointerToUserInput=0
table=[i.strip().split('\t') for i in open('LR0_grammar_table.txt','r')]
print('----------------------------------------------Grammar Table------------------------------------------------')
[print(i) for i in table] # printing table
grammar=[i.strip() for i in open('LR0_grammar.txt','r')]
print('----------------------------------------------Grammar------------------------------------------------')
print(grammar)
rules={}
indexesForId=[i for i,j in enumerate(userInputWithoutIndentifiers) if j=='id'][1:];identiferPointer=0;threeAddressCode=[];variables=0
print(indexesForId)
while True:
    row=int(stack[-1])+1 # Plus one because in talbe zero row is for terminal and non terminals
    col= ([i for i,j in enumerate(table[0][1:]) if j==userInputWithoutIndentifiers[pointerToUserInput]][0])+1 #plus one      because zero column is for row indexing
    operationToPerform=table[row][col]
    if operationToPerform[0]=='s':  # means shift operation
        print('--------------------Shift operation Perform---------------')
        print('Stack Before Shift: ',stack)
        print('Input Before Shift: ',userInputWithoutIndentifiers[pointerToUserInput:])
        print('row: ',row-1,'col: ',col-1)
        stack.append(userInputWithoutIndentifiers[pointerToUserInput]) # shift input to stack
        pointerToUserInput+=1 # pointer increment because we shift the current input to stack
        stack.append(operationToPerform[1]) # append the number with shift
        print('Operation Perfomed: ',table[row][col])
        print('Stack After Shift: ',stack)
        print('Input After Shift: ',userInputWithoutIndentifiers[pointerToUserInput:])

    elif operationToPerform[0]=='r': # means reductiton operation
        print('--------------------Reduce operation Perform---------------')
        print('Stack Before Reduce: ',stack)
        print('Input Before Reduce: ',userInputWithoutIndentifiers[pointerToUserInput:])
        print('row: ',row-1,'col: ',col-1)
        print('Operation Perfomed: ',table[row][col])
        production=grammar[int(operationToPerform[1])] # remember grammar prodcution numbering starts with 0
        print('Reduced Production: ',production)
        temp='';calculateTerminalOrNonTerminal=[] # logic to handle terminal sysmbol with length more than one
        for i in production[3:]:
            if i in nonTerminalSymbolsGrammar:
                calculateTerminalOrNonTerminal.append(i)
            elif i not in terminalSymbolsGrammar and i not in nonTerminalSymbolsGrammar:
                temp+=i
                if temp in terminalSymbolsGrammar:
                    calculateTerminalOrNonTerminal.append(temp)
                    temp=''
            else:
                calculateTerminalOrNonTerminal.append(i)
        pop=len(calculateTerminalOrNonTerminal)*2 # pop to pop from stack
        print('POP from stack: ',pop)
        for i in range(pop):
            stack.pop()
        stack.append(production[0]) # append left of prodcution in stack
        row=int(stack[-2])+1 # Plus one because in talbe zero row is for terminal and non terminals
        col= ([i for i,j in enumerate(table[0][1:]) if j==stack[-1]][0])+1 #plus one because zero column is for row indexing
        if table[row][col]=='-':
            print('error')
            break
        stack.append(table[row][col])
        print('Stack After Reduce: ',stack)
        print('Input After Reduce: ',userInputWithoutIndentifiers[pointerToUserInput:])
        if production=='F->id':
            rules['F.place']=str(userInput[indexesForId[identiferPointer]])
            print('Rule: ','F = ',userInput[indexesForId[identiferPointer]])
            identiferPointer+=1
        elif production=='T->F':
            rules['T.place']=rules['F.place']
            print('Rule: ','T = ',rules['F.place'])
        elif production=='T->T*F':
            genratedVar='T'+str(variables)
            variables+=1
            threeAddressCode.append(genratedVar+'='+rules['T.place']+'*'+rules['F.place'])
            rules['T.place']=rules['T.place']+'*'+rules['F.place']
            rules['T.place']=genratedVar 
        elif production=='E->T':
            rules['E.place']=rules['T.place']
            print('Rule: ','E = ',rules['T.place'])
        elif production=='E->E+T':
            genratedVar='T'+str(variables)
            variables+=1
            threeAddressCode.append(genratedVar+'='+rules['E.place']+'+'+rules['T.place'])
            rules['E.place']=rules['E.place']+"+"+rules['T.place']
            rules['E.place']=genratedVar
    elif operationToPerform=='-':
        print('error')
        break
    elif operationToPerform=='accept':
        print('Sucess')
        break
print('-------------------------------------------Three Address Code-------------------------------')
for i in threeAddressCode:
    print(i)