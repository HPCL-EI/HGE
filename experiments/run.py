import argparse
import copy
import pickle
import time
import numpy as np
from joblib import Parallel, delayed
from joblib import cpu_count

from ponyge.operators.initialisation import initialisation
from ponyge.algorithm.parameters import Parameters

import importlib

import os
import shutil

from fitness import body_fitness, bt_fitness
# from game.bt_fitness import generate_score_map, bt_fitness

from bt.nodes import create_bt_from_xml,simpleAction
from bt.display import render_dot_tree

def setDir(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    else:
        shutil.rmtree(filepath)
        os.makedirs(filepath)

def generate_body_grammar(args):
    body_grammar_path = f'{args.path}/grammars/body.bnf'
    with open(body_grammar_path, 'w') as f:
        f.write(f'<root>::={"-".join([f"<{m}>" for m in range(args.M)])}\n')
        for m in range(args.M):
            f.write(f'<{m}>::={" | ".join([f"{c}" for c in range(args.C)])}\n')

class BTSettings(dict):
    def __repr__(self):
        return 'bt_settings'

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exp', default="game", choices=["house","game"])
    parser.add_argument('--algo', default="GE+PGE", choices=["R+R",'R+PR',"R+GE",'R+PGE',"GE+R",'GE+PR',"GE+GE","GE+PGE"])
    parser.add_argument('--M', default=5, type=int)
    parser.add_argument('--C', default=10, type=int)
    parser.add_argument('--W', default=10, type=int)
    parser.add_argument('--body_population_size', default=10, type=int)
    parser.add_argument('--body_generations', default=10, type=int)
    parser.add_argument('--population_size', default=10, type=int)
    parser.add_argument('--generations', default=10, type=int)
    parser.add_argument('--seed', default=0, type=int)
    args = parser.parse_args()

    # generate game
    exp_name = args.exp

    scenario_name = ''
    if exp_name == 'house':
        scenario_name = 'House'
    if exp_name == 'game':
        scenario_name = f'{args.M}-{args.C}-{args.W}'

    args.path =  f'{exp_name}/results/{scenario_name}/{args.algo} {args.population_size}-{args.generations}/{args.seed}'
    setDir(f'{args.path}')
    setDir(f'{args.path}/BT_grammars/grammars')
    setDir(f'{args.path}/grammars' )

    # settings
    settings = importlib.import_module(f'{exp_name}.settings')
    settings.generate_body_grammar(args)   # generate body BNF
    start_state,goal_state = settings.generate_task(args)
    
    bt_settings = BTSettings()
    bt_settings.bt_fitness = bt_fitness
    bt_settings.score_map = settings.generate_score_map(args)
    bt_settings.action_fit = settings.action_fit
    bt_settings.planning = 'P' in args.algo
    bt_settings.start_state = start_state
    bt_settings.goal_state = goal_state
    bt_settings.parse_state = settings.parse_state
    bt_settings.parse_action = settings.parse_action
    bt_settings.invalid_fitness = settings.invalid_fitness
    
    #
    # if bt_settings.planning and args.M > 4:
    #     exit()
    # init Body Grammar
    parameter = Parameters()
    parameter_list = ['--parameters', f'{exp_name},body.txt']
    parameter.params['GRAMMAR_FILE'] = f'{args.path},body.bnf'
    parameter.params['EXPERIMENT_NAME'] = f'{exp_name}'
    parameter.params['RANDOM_SEED'] = args.seed
    parameter.params['BODY_FITNESS'] = body_fitness
    parameter.params['CAM'] = settings.cam
    parameter.params['ARGS'] = args
    parameter.params['RANDOM'] = np.random.RandomState(args.seed)
    parameter.params['SIMPLE_ACTION'] = simpleAction
    parameter.params['SINGLE'] = args.algo[-1] == 'R'
    parameter.params['CONDITION_LIST'] = settings.get_condition_list(args)
    parameter.params['BTSETTINGS'] = bt_settings
    parameter.params['PLANNING_TIME'] = 0
    parameter.params['SIM_TIME'] = 0
    parameter.params['BT_TIME'] = 0
    parameter.params['BT_FIT_RATIO'] = [0,0]
    parameter.set_params(parameter_list)
    parameter.params['POPULATION_SIZE'] = args.body_population_size
    parameter.params['GENERATIONS'] = args.body_generations

    start_time = time.time()
    
    fit = 0
    if args.algo[0] == 'R':
        individuals = initialisation(parameter, 1)
        fit = body_fitness(individuals[0], parameter)
    else:
        individuals = parameter.params['SEARCH_LOOP'](parameter)
        fit = individuals[0].fitness
    
    total_time = time.time() - start_time
    
    print(f'{scenario_name} Algorithm: {args.algo} {args.population_size}-{args.generations}  Seed: {args.seed}  Fitness: {fit:.3f} Total_Time: {total_time:.3f}  Planning Ratio: {parameter.params["PLANNING_TIME"] / total_time:.3f}  BT Ratio: {parameter.params["BT_TIME"] / total_time:.3f}  BT_fit_ratio: {parameter.params["BT_FIT_RATIO"][0] / parameter.params["BT_FIT_RATIO"][1] if parameter.params["BT_FIT_RATIO"][1] else 0} ')

    with open(f'{args.path}/fitness.txt','w') as f:
        f.write(str(fit))
    with open(f'{args.path}/time.txt','w') as f:
        f.write(f'{total_time}\n')
        f.write(f'{parameter.params["BT_TIME"]}\n')
        f.write(f'{parameter.params["PLANNING_TIME"]}\n')
        f.write(f'{parameter.params["SIM_TIME"]}\n')
    with open(f'{args.path}/bt_fit_ratio.txt', 'w') as f:
        f.write(f'{parameter.params["BT_FIT_RATIO"][0] / parameter.params["BT_FIT_RATIO"][1] if parameter.params["BT_FIT_RATIO"][1] else 0}\n')

        
    bt = create_bt_from_xml(individuals[0].best_bt,
                            None,
                            settings.parse_state,
                            settings.parse_action
                            )
    if exp_name == 'house':
        render_dot_tree(bt.root, target_directory=args.path, name=individuals[0].phenotype)
