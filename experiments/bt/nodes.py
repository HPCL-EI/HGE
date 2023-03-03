import py_trees
from py_trees.composites import Composite
from py_trees.composites import Selector as BaseSelector
from py_trees.composites import Sequence as BaseSequence
from py_trees.behaviour import Behaviour
from py_trees import common
import xml.etree.ElementTree as ET

from copy import deepcopy

from collections import deque

def create_bt_from_xml(xmlstring, world = None,parse_state =None,prase_action=None):
    xmlstring = xmlstring.replace('[', '<')
    xmlstring = xmlstring.replace(']', '>')
    xmlstring = xmlstring.replace('%', '"')
    
    tree = ET.fromstring(xmlstring)
    
    root_name = tree.tag
    root = eval(root_name)()
    if root_name in ["Sequence", "Selector"]:
        root.load_from_xml(tree,world,parse_state,prase_action)
    return py_trees.trees.BehaviourTree(root)

# Base Control Node
class ControlNode(Composite):
    def load_from_xml(self, xtree,world, parse_state,parse_action):
        for tree in xtree:
            if tree.tag == 'cond':
                execution = Condition(parse_state(tree.text))
                execution.world = world
                self.add_child(execution)
            if tree.tag == 'act':
                a_str = tree.text
                a = parse_action(a_str,simpleAction)
                execution = Action()
                execution.load_from_simple(a)
                execution.world = world
                self.add_child(execution)
            if tree.tag == 'Sequence' or tree.tag == 'Selector':
                node = eval(tree.tag)()
                node.load_from_xml(list(tree), world, parse_state, parse_action)
                self.add_child(node)
            
class Selector(ControlNode,BaseSelector):
    def __init__(self):
        super(Selector, self).__init__()
        self.name = '?'
    
class Sequence(ControlNode,BaseSequence):
    def __init__(self):
        super(Sequence, self).__init__()
        self.name = '→'
        
class simpleAction(object):
    def __init__(self,name='Action'):
        self.name = name
        self.pre = set()
        self.add = set()
        self.del_set = set()

class Action(Behaviour):
    def __init__(self,name='Action'):
        super(Action, self).__init__()
        self.name = f'{name}'
        self.pre = set()
        self.add = set()
        self.del_set = set()
        self.world = {}

    def load_from_simple(self,simple):
        self.name = simple.name
        self.pre = simple.pre
        self.add = simple.add
        self.del_set = simple.del_set
    
    def update(self):
        # print(f'action {self.name},  state: {self.world["s"]},  pre: {self.pre},  success: {self.pre in self.world["s"]}')
        if self.pre.issubset(self.world['s']):
            self.world['a'] = self
            return common.Status.RUNNING
        else:
            return common.Status.FAILURE

    
class Condition(Behaviour):
    def __init__(self, state):
        super(Condition, self).__init__()
        self.state = state
        self.name = '+'.join(state)
        self.world = {}
        
    def update(self):
        # print(f'condition {self.name},  state: {self.world["s"]},  pre: {self.state},  success: {self.state.issubset(self.world["s"])}')
        if self.state.issubset(self.world['s']):
            return common.Status.SUCCESS
        else:
            return common.Status.FAILURE

if __name__ == '__main__':
    s = '''
                [Sequence]
                    [Sequence]
                        [Sequence]
                            [cond]0[/cond]
                            [act]1,23,10[/act]
                        [/Sequence]
                        [Selector]
                            [cond]0[/cond]
                            [act]1,23,45[/act]
                        [/Selector]
                    [/Sequence][Selector]
                        [cond]1[/cond]
                        [act]1,23,41[/act]
                    [/Selector]
                [/Sequence]'''
    print(ET.fromstring(s))
