"""This is the mapper class which maps the xml file."""
# import xml.etree.ElementTree as ET
#
# import py_trees
#
# import esi
# from esi.bt.display import render_dot_tree
#
# from esi.io import load_yaml

# behavior tree
# class BT(object):
#     def __init__(self, root=None):
#         "Initialize the attributes for mapper."
#         self.agent = None
#         if root is not None:
#             self._bt = py_trees.trees.BehaviourTree(root)
#         else:
#             self._bt = None
#
#     def setup(self, agent):
#         self.agent = agent
#
#     def set_root(self, root):
#         self._bt = py_trees.trees.BehaviourTree(root)
#         root.setup(bt=self)
#
#     @property
#     def root(self):
#         return self._bt.root
#
#     def tick(self):
#         if self._bt:
#             self._bt.tick()
#
#     def load_from_xml(self,xmlstring):
#         xmlstring = xmlstring.replace('[', '<')
#         xmlstring = xmlstring.replace(']', '>')
#         xmlstring = xmlstring.replace('%', '"')
#
#         tree = ET.fromstring(xmlstring)
#         root_name = tree.tag
#         root = eval(root_name)()
#         if root_name in ["Sequence", "Selector"]:
#             root.load_from_xml(xtree=tree)
#
#         self.set_root(root)
#
#     # the parameter can be a python structure or a path of tree file
#     def load_from_list(self, node_list=None, path=None):
#         if path:
#             node_list=load_yaml(path)
#             # with open(path, 'r') as f:
#             #     node_list = f.readlines()
#         if not node_list:
#             return
#
#         root_name = node_list[0]
#         root = eval(root_name)()
#         if len(node_list) > 0 and root_name in ["Sequence", "Selector"]:
#             root.load_from_list(node_list=node_list[1])
#         self.set_root(root)
#
#     def visualize(self, name='plotBT'):
#         """Save bt graph to a file."""
#         render_dot_tree(self._bt.root, name=name, target_directory=esi.io.make_out_dir(name))
#
#
# def _test_hand_code():
#     from esi.bt.nodes import Sequence, Selector, TestAction1, TestAction2, TestCondition1, TestCondition2
#
#     bt = BT()
#
#     root = Sequence()
#     sequence = Sequence()
#     selector = Selector()
#     root.add_children([sequence, selector, TestAction1()])
#     sequence.add_children([TestCondition2()])
#     selector.add_children([TestCondition1(), TestAction2()])
#
#     bt.set_root(root)
#     # root.add_children()
#     bt.visualize()
#
#
#
# ### test
# def _test_from_yaml():
#     from esi.bt.nodes.control import Sequence, Selector
#     node_list = load_yaml(esi.ROOT_DIR, "esi", "bt", "_test", "_test_bt.yaml")
#     bt = BT()
#     bt.load_from_list(node_list)
#     bt.visualize()
#
#
# if __name__ == '__main__':
#     from esi.bt.nodes.control import Sequence, Selector
#
#     node_list = load_yaml(esi.ROOT_DIR, "esi", "bt", "_test", "_test_bt.yaml")
#     bt = BT()
#     bt.load_from_list(node_list)
#     bt.visualize()
