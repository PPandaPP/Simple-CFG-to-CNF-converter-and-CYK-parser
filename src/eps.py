from nltk import CFG, Production, Nonterminal
from nltk import Tree
from itertools import combinations

def check_nullable(grammar, child, nullable, depth, visited):
    for p in grammar.productions(): ## aqui se esta cortando
        if(p in visited):
            # print("Visited", visited, "current", p)
            continue
        # check for production rules generated by child variable
        if str(child) == str(p.lhs()):
            # base case 
            if('None' in p.rhs() and len(p.rhs()) == 1):
                nullable.add(p.lhs())
                return(True)
            
            # recursive step
            else:
                count_nullable_children = 0
                for child2 in p.rhs():
                    if(child2 != p.lhs()):
                        visited.append(p)
                        found_none = check_nullable(grammar, child2, nullable, depth+1, visited)
                        #print(depth, p.lhs(), p.rhs(), "checking: ", child2, found_none)
                        # backtracking
                        if(found_none):
                            count_nullable_children += 1 
                # if all variables can derive epsilon, is nullable #            
                if(count_nullable_children == len(p.rhs())):
                    nullable.add(p.lhs())
                    return(True) 
    return(False)

##### Helper function to remove all possible combinations of nullable ####
def removing_combis(og, nullable):
    # perms will hold all possible combinations of nullable #
    perms = []
    for i in range(1, len(nullable)+1):
        # seq is a list of combinations of size i of nullable #
        seq = list(combinations(nullable, i))
        for element in seq:
            perms.append(list(element))
    # finals will hold the combinations of removing each element in seq #
    finals = []
    for remove_list in perms:
        res = [i for i in list(og) if i not in remove_list]
        if tuple(res) not in finals:
            finals.append(tuple(res))
    
    return(finals)

def remove_all_epsilons(grammar):
    nullable = set()  
    if(check_nullable(grammar, grammar.start(), nullable, 0, [])):
        nullable.add(grammar.start())
            
    # tienen valor cero #
    # print("Nullable: ", nullable, "\n")
    
    # print("before processing:", grammar.productions())  
    new_prods = grammar.productions().copy()

    # add new rules without each of the nullables
    for p in grammar.productions():
        for rr in p.rhs():
            if rr in nullable:
                lhs = p.lhs()
                # rules list has all the combinations when removing each of the variables in nullable #
                rules_list = removing_combis(p.rhs(), nullable)
                
                if(len(rules_list) == 0 or len(rules_list[0]) == 0):
                    continue
                # add each combination #
                for element in rules_list:
                    if(len(element) > 0):
                        # create rule of type Production() #
                        new_production = Production(lhs, element)
                        if(new_production not in new_prods):
                            new_prods.append(new_production)
    # print(new_prods)   
    
    to_rem2 = []
    for element in new_prods:
        if len(element.rhs()) == 1 and (element.rhs()[0] == 'None' or element.rhs()[0] == element.lhs()):
            to_rem2.append(element)

    for element in to_rem2:
        if element in new_prods:
           new_prods.remove(element)

    # create new grammar with these rules # 
    new_grammar = CFG(grammar.start(), new_prods)
    return(new_grammar)