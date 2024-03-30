from nltk import CFG, Production, Nonterminal
from nltk import Tree

## need restriction to only 
gg = '''HTML ->  L0 H L1 B L2 
L0 -> '<html><head>'
L1 -> '</head><body>'
L2 -> '</body></html>'
H ->  L3 T L4 
L3 -> '<title>'
L4 -> '</title>'
C -> T
B -> C B
B -> D
B -> C
D -> 'None'
C -> L8 T L9 
T -> L11
T -> L10
L10 -> 'None'
'''

gg2 = '''
HTML ->  L0 H L1 B L2 
L0 -> '<html><head>'
L1 -> '</head><body>'
L2 -> '</body></html>'
H ->  L3 T L4 
L3 -> '<title>'
L4 -> '</title>'
C -> T
B -> C
B -> C B
C ->  L5 
L5 -> '<img>'
C ->  L6 T L7 
L6 -> '<br>'
L7 -> '</br>'
C ->  L8 T L9 
L8 -> '<hr>'
L9 -> '</hr>'
T -> L10
L10 -> 'None'
T ->  L11 
L11 -> 'z'
'''

def check_nullable(grammar, child, nullable, depth):
    flag = False
    for p in grammar.productions(): ## aqui se esta cortando
        # check for production rules generated by child variable
        if str(child) == str(p.lhs()):
            # base case 
            if('None' in p.rhs()):
                nullable.add(p.lhs())
                return(True)
            
            # recursive step
            else:
                for child2 in p.rhs():

                    if(child2 != p.lhs()):
                       
                        found_none = check_nullable(grammar, child2, nullable, depth+1)
                        #print(depth, p.lhs(), p.rhs(), "checking: ", child2, found_none)
                        # backtracking
                        if(found_none):
                            #print(p)
                            flag = True
                            nullable.add(p.lhs())

    return(flag)

def removing_nullable(rhs, element):
    a = []
    for g in rhs:
        if(str(g) != str(element)):
            a.append(g)
    return(tuple(a))

def remove_all_epsilons(grammar):
    nullable = set()   
    if (check_nullable(grammar, "HTML", nullable, 0)):
        nullable.add(grammar.start())
            
    print("Nullable: ", nullable, "\n")

    new_prods = grammar.productions().copy()
    # add new rules without each of the nullables
    for p in grammar.productions():
        for rr in p.rhs():
            if rr in nullable:
                #print("null", p)
                lhs = p.lhs()
                rhs = removing_nullable(p.rhs(), rr)
                if(len(rhs) == 0):
                    continue
                
                # check for redundancies such as B -> B
                if(lhs != rhs[0] or len(rhs) != 1):
                    new_production = Production(lhs, rhs)
                    new_prods.append(new_production)
                
        # remove direct 'None'
        if ('None' in p.rhs()):
            new_prods.remove(p)
        
    new_grammar = CFG(grammar.start(), new_prods)
    return(new_grammar)

# grammar = CFG.fromstring(gg)  
# print("\n", "Before eliminating epsilons: ")
# for p in grammar.productions():          
#         print(p)  
         
# new_grammar = remove_all_epsilons(grammar)

# print("\n", "After eliminating epsilons: ")
# for p in new_grammar.productions():          
#         print(p)