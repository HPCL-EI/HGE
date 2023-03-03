import os

from ponyge.operators.initialisation import initialisation
from ponyge.operators.mutation import mutation
from ponyge.algorithm.parameters import Parameters

from bt.nodes import simpleAction
from algorithms import expand,bt2bnf,general_bnf,bt_grammar_expansion

from bt.nodes import create_bt_from_xml
import time
import numpy as np

def body_fitness(ind, parameter):


    body_str = ind.phenotype
    bt_settings = parameter.params['BTSETTINGS']
    cam = parameter.params['CAM']
    exp_name = parameter.params['EXPERIMENT_NAME']
    args = parameter.params['ARGS']
    bt_bnf_path = f'{args.path}/BT_grammars/grammars/{body_str}.bnf'
    # print(bt_bnf_path)
    # cache BT grammar
    
    action_list = cam(body_str,args,parameter.params['SIMPLE_ACTION'])
    
    # Planning
    if bt_settings.planning:
        if not os.path.exists(bt_bnf_path):
            start_time = time.time()
            t, grammar = bt_grammar_expansion(bt_settings.goal_state, bt_settings.start_state, action_list)
            # t, T = expand(bt_settings.goal_state, bt_settings.start_state, action_list, [])
            planning_time = time.time() - start_time
            parameter.params['PLANNING_TIME'] += planning_time
            if not t:
                return parameter.params['BTSETTINGS'].invalid_fitness
            with open(f'{bt_bnf_path}', 'w') as f:
                f.writelines(grammar)
    else:
        if not action_list:
            return parameter.params['BTSETTINGS'].invalid_fitness
        general_bnf(bt_bnf_path,
                    parameter.params['CONDITION_LIST'],
                    [a.name for a in action_list])

    bt_start_time = time.time()

    # train BTs
    BT_parameter = Parameters()
    BT_parameter_list = ['--parameters', f'{exp_name},bt.txt']
    BT_parameter.params['GRAMMAR_FILE'] = f'{args.path}/BT_grammars,{body_str}.bnf'
    BT_parameter.params['RANDOM_SEED'] = parameter.params['RANDOM'].randint(0,99999999)
    BT_parameter.params['BTSETTINGS'] = bt_settings
    BT_parameter.params['SIM_TIME'] = 0
    BT_parameter.set_params(BT_parameter_list)

    BT_parameter.params['POPULATION_SIZE'] = args.population_size
    BT_parameter.params['GENERATIONS'] = args.generations
    BT_parameter.params['BODY_MORPHOLOGY'] = body_str

    bt_time = time.time() - bt_start_time
    parameter.params['BT_TIME'] += bt_time


    if parameter.params['SINGLE']:
        individuals = initialisation(BT_parameter, 1)
        fit = bt_fitness(individuals[0], BT_parameter)
    else:
        individuals = BT_parameter.params['SEARCH_LOOP'](BT_parameter)
        fit = individuals[0].fitness

    parameter.params['BEST_BT'] = individuals[0].phenotype
    ind.best_bt = individuals[0].phenotype
    
    parameter.params['SIM_TIME'] += BT_parameter.params['SIM_TIME']

    if args.exp == 'game':
        max_bt_fit = 0
        for m, c in enumerate(map(int,body_str.split('-'))):
            max_bt_fit += np.max(bt_settings.score_map[m,c,:])
        if max_bt_fit:
            parameter.params['BT_FIT_RATIO'][0] += fit / max_bt_fit
        parameter.params['BT_FIT_RATIO'][1] += 1
        
    return fit

def bt_fitness(ind, parameter):
    bt_str = ind.phenotype
    bt_settings = parameter.params['BTSETTINGS']
    fit = 0
    world = {'s': bt_settings.start_state,'a':None}

    bt = create_bt_from_xml(bt_str,
                            world,
                            bt_settings.parse_state,
                            bt_settings.parse_action
                            )

    start_time = time.time()
    while True:
        bt.tick()
        if world['a'] is None:
            fit = parameter.params['BTSETTINGS'].invalid_fitness
            break
        fit += bt_settings.action_fit(world['a'].name, parameter)
        world['s'] = (world['s'] | world['a'].add) - world['a'].del_set
        if bt_settings.goal_state.issubset(world['s']):
            break
        world['a'] = None
    
    sim_time = time.time() - start_time
    parameter.params['SIM_TIME'] += sim_time
    
    return fit
