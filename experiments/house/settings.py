
small_score_map = { 'Cross(spills-wheel2)':-2,
                    'Wade(puddles-wheel2)':-9,
                    'Sweep(toys-scoop)': -4,
                    }

big_score_map ={'Cross(spills-wheel2)':-1,
                'Wade(puddles-wheel2)':-7,
                'Cross(spills-wheel3)':-4,
                'Wade(puddles-wheel3)':-12,
                'RunOver(toys-wheel3)': -3
                }


ca_maps = {'wheel2': ['Cross(spills-wheel2)','Wade(puddles-wheel2)'],
        'wheel3': ['Cross(spills-wheel3)', 'Wade(puddles-wheel3)','RunOver(toys-wheel3)'],
        'scoop': ['Sweep(toys-scoop)']}

condition_list = ['At(yard)','At(lounge)','At(playroom)','Sweeped(toys)']

action_maps = { 'Cross(spills-wheel2)': ['At(yard)', 'At(lounge)', 'At(yard)'],
                'Cross(spills-wheel3)': ['At(yard)', 'At(lounge)', 'At(yard)'],
                'Wade(puddles-wheel2)': ['At(yard)', 'At(playroom)', 'At(yard)'],
                'Wade(puddles-wheel3)': ['At(yard)', 'At(playroom)', 'At(yard)'],
                'RunOver(toys-wheel3)': ['At(lounge)', 'At(playroom)', 'At(lounge)'],
                'Sweep(toys-scoop)': ['At(lounge)', 'At(playroom)+Sweeped(toys)', 'At(lounge)']
        }

invalid_fitness = -999999

def get_condition_list(args):
    return condition_list

def generate_task(args):
    # scenario setting
    start = {'At(yard)'}
    goal = {'At(playroom)'}
    return start,goal

def generate_body_grammar(args):
    body_grammar_path = f'{args.path}/grammars/body.bnf'
    with open(body_grammar_path, 'w') as f:
        f.write(f'''<root>::= motor1-<light_wheels> | motor2-<all_wheels> | motor1-<light_wheels>-scoop
<all_wheels>::= <light_wheels> | wheel3
<light_wheels>::= wheel1 | wheel2''')

def generate_score_map(args):
    return small_score_map

def action_fit(a_str,parameter):
    if 'motor1' in parameter.params['BODY_MORPHOLOGY']:
        # print(parameter.params['BODY_MORPHOLOGY'])
        return small_score_map[a_str]
    else:
        return big_score_map[a_str]

def parse_state(s_str):
    s_list = s_str.split('+')
    s = set(s_list) - {'None'}
    return s


def parse_action(a_str,simpleAction):
    pre, add, del_set = action_maps[a_str]
    a = simpleAction(a_str)
    a.pre = parse_state(pre)
    a.add = parse_state(add)
    a.del_set = parse_state(del_set)
    return a

def cam(body_str,args,simpleAction):
    action_list = []
    for b in body_str.split('-'):
        if b in ca_maps.keys():
            for a_str in ca_maps[b]:
                action_list.append(parse_action(a_str,simpleAction))
    return action_list
