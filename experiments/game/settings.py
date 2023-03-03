import re
import numpy as np

def generate_task(args):
    # scenario setting
    start = frozenset([f'{0}'])
    goal = frozenset([f'{args.M}'])
    return start,goal

def generate_body_grammar(args):
    body_grammar_path = f'{args.path}/grammars/body.bnf'
    with open(body_grammar_path, 'w') as f:
        f.write(f'<root>::={"-".join([f"<{m}>" for m in range(args.M)])}\n')
        for m in range(args.M):
            f.write(f'<{m}>::={" | ".join([f"{c}" for c in range(args.C)])}\n')

def generate_score_map(args):
    M = args.M
    C = args.C
    W = args.W
    max_score = 1 / M
    c_map = np.linspace(0,1,C)
    c_map = c_map.reshape(C,1).repeat(W,axis = 1)
    w_map = np.linspace(0,1,W)
    w_map = w_map.reshape(1,W).repeat(C,axis = 0)
    score_map = ( c_map * w_map * max_score).reshape((1,C,W)).repeat(M,axis = 0)
    # print(score_map)
    # score_map = random.rand(M,C,W) * max_score
    # for m in range(M):
    #     score_map[m,random.randint(C),random.randint(W)] = max_score
    # print(score_map)
    return score_map

def get_condition_list(args):
    return [str(s) for s in range(args.M)]

# def generate_score_map(args):
#     M = args.M
#     C = args.C
#     W = args.W
#     random = np.random.RandomState(0)
#     max_score = 1 / M
#     score_map = random.rand(M,C,W) * max_score
#     for m in range(M):
#         score_map[m,random.randint(C),random.randint(W)] = max_score
#     return score_map

invalid_fitness = 0
def action_fit(a_str,parameter):
    m, c, w = map(int, a_str.split('-'))
    return parameter.params['BTSETTINGS'].score_map[m, c, w]

def parse_state(s_str):
    s = frozenset([s_str])
    return s

def parse_action(a_str,simpleAction):
    m, c, w = a_str.split('-')
    a = simpleAction(a_str)
    a.pre = parse_state(m)
    a.add = parse_state(f'{int(m) + 1}')
    a.del_set = parse_state(m)
    return a

def cam(body_str,args,simpleAction):
    action_list = []
    for m, c in enumerate(body_str.split('-')):
        for w in range(args.W):
            a = simpleAction(f'{m}-{c}-{w}')
            a.pre = parse_state(f'{m}')
            a.add = parse_state(f'{m+1}')
            a.del_set = parse_state(f'{m}')
            action_list.append(a)
    return action_list

