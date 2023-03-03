from bt.nodes import Sequence,Selector,Action,Condition
from copy import deepcopy
# Base Control Node

class ExpandCondition(set):
    def __init__(self,state):
        super(ExpandCondition, self).__init__(state)
        self.name = '+'.join(state)
        self.expanded_pairs = {}
        self.un_judged_actions = []
        self.reachable = False



def bt_grammar_expansion(s_g, s_0, action_set):
    stack = []
    expanded_dict = {}
    top = ExpandCondition(s_g)
    grammar = [f'<r> ::= <{top.name}>\n']
    top.un_judged_actions = deepcopy(action_set)
    stack.append(top)
    while stack:
        top = stack[-1]
        if top.un_judged_actions:
            a = top.un_judged_actions.pop()
            if not top & ((a.pre | a.add) - a.del_set) <= set() and (top - a.del_set) == top:
                c = ExpandCondition((a.pre | top) - a.add)
                if c.name in expanded_dict.keys():
                    if expanded_dict[c.name].reachable:
                        if c.name not in top.expanded_pairs.keys():
                            top.expanded_pairs[c.name] = [a.name]
                        else:
                            top.expanded_pairs[c.name].append(a.name)
                else:
                    if c.issubset(s_0):
                        grammar.append(f'<{c.name}> ::= [cond]{c.name}[/cond]\n')
                        c.reachable = True
                        if c.name not in top.expanded_pairs.keys():
                            top.expanded_pairs[c.name] = [a.name]
                        else:
                            top.expanded_pairs[c.name].append(a.name)
                        expanded_dict[c.name] = c
                    else:
                        top.un_judged_actions.append(a)
                        c.un_judged_actions = deepcopy(action_set)
                        stack.append(c)
        else:
            if top.expanded_pairs:
                grammar.append(f'<{top.name}> ::= [Selector][cond]{top.name}[/cond][Sequence]<s_{top.name}>[/Sequence][/Selector]\n')
                grammar.append(f'<s_{top.name}> ::= {" | ".join([f"<{c_name}>[act]<a_{c_name}_{top.name}>[/act]" for c_name in top.expanded_pairs.keys()])}\n')
                grammar += [f'<a_{c_name}_{top.name}> ::= {" | ".join(top.expanded_pairs[c_name])}\n'  for c_name in top.expanded_pairs.keys()]
                
                top.reachable = True
            expanded_dict[top.name] = top
            stack.pop()

    return top.reachable,grammar

def expand(s_g, s_0, action_set, traversed_set):
    if s_g.issubset(s_0):
        c = Condition(s_g)
        return True, c
    T_root = Selector()
    T_root.add_child(Condition(s_g))
    # T_root.valid = False
    
    for a in action_set:
        if not s_g & ((a.pre | a.add) - a.del_set) <= set() and (s_g - a.del_set) == s_g:
            c = (a.pre | s_g) - a.add
            if not c in traversed_set:
                new_traversed_set = traversed_set + [c]
                # print('==========')
                # print(s_g,a.name,c)
                # print(traversed_set)
                t, T_a = expand(c, s_0, action_set, new_traversed_set)
                if t:
                    T_sub = Sequence()
                    # print(T_a)
                    # print(a)
                    a_node = Action()
                    a_node.load_from_simple(a)
                    T_sub.add_children([T_a, a_node])
                    T_root.add_child(T_sub)
    return len(T_root.children) > 1, T_root


def bt2bnf(T_root, f, condition_num=1, action_num=1):
    if isinstance(T_root, Condition):
        return f'[cond]{T_root.name}[/cond]', condition_num, action_num
    else:
        condition_name = f'<c{condition_num}>'
        action_name = f'<a{action_num}>'
        f.write(f'{condition_name}::=[Selector][cond]{T_root.children[0].name}[/cond]{action_name}[/Selector]\n')
        
        action_num += 1
        str_list = []
        for a in T_root.children[1:]:
            condition_num += 1
            name, condition_num, action_num = bt2bnf(a.children[0], f, condition_num, action_num)
            str_list.append(f'[Sequence]{name}[act]{a.children[1].name}[/act][/Sequence]')
        f.write(f'{action_name}::={" | ".join(str_list)}\n')
        return condition_name, condition_num, action_num


# def bt2bnf(T_root, f, condition_num=1, action_num=1):
#     if isinstance(T_root, Condition):
#         return T_root.name, condition_num, action_num
#     else:
#         condition_name = f'<c{condition_num}>'
#         action_name = f'<a{action_num}>'
#         f.write(f'{condition_name}::=f({T_root.children[0].name},{action_name})\n')
#
#         action_num += 1
#         str_list = []
#         for a in T_root.children[1:]:
#             condition_num += 1
#             name, condition_num, action_num = bt2bnf(a.children[0], f, condition_num, action_num)
#             str_list.append(f's({name},[{a.children[1].name}])')
#         f.write(f'{action_name}::={" | ".join(str_list)}\n')
#         return condition_name, condition_num, action_num
#

def general_bnf(file_path, condition_list, action_list):
    head = '''<s> ::= [?xml version=%1.0% encoding=%UTF-8%?]<cf>
<cf> ::= <sequence> | <selector>
<sequence> ::= [Sequence]<execution>[/Sequence] | [Sequence]<cf><cf>[/Sequence] | [Sequence]<sequence> <cf>[/Sequence]
<selector> ::= [Selector]<execution>[/Selector] | [Selector]<cf><cf>[/Selector] | [Selector]<selector> <cf>[/Selector]
<execution>::=<conditions>[act]<action>[/act]
<conditions>::=[cond]<condition>[/cond]<conditions>|[cond]<condition>[/cond]
'''
    with open(file_path,'w') as f:
        f.write(head)
        f.write(f'<condition>::={" | ".join(condition_list)}\n')
        f.write(f'<action>::={" | ".join(action_list)}')
