import pm4py
import random
import asyncio
from pm4py.objects.process_tree.obj import ProcessTree, Operator
import ActivityNames
import json

class CustomRandomProcessTree:

    def __init__(self, list_of_activities: list[str]):

        # Convert list of activities into a list of Process Tree Leafs labeled with the activities
        self.list_of_activities = list_of_activities
        self.remaining_activities = list_of_activities

        # start building the tree
        all_operators = (Operator.SEQUENCE, Operator.PARALLEL, Operator.XOR, Operator.OR, Operator.LOOP)
        root_operator_node = random.choice(all_operators)
        loop = asyncio.get_event_loop()
        starting_activity = loop.run_until_complete(ActivityNames.async_llm_picks_best_starting_activity(root_operator_node))
        #starting_activity = ActivityNames.llm_picks_best_starting_activity(root_operator_node)
        self.process_tree = ProcessTree(operator=root_operator_node)
        #minimum_number_of_children_for_root = 1 if root_operator_node != Operator.LOOP else 0
        self.open_leafs = 0 #TODO correct calculation for minimum number of children for root and set it as the value for number of open leafs
        self.process_tree.children = self.build_child_trees_of_root(parent=self.process_tree)


    def build_child_trees_of_root(self, parent):
        child_trees = []
        while self.remaining_activities:
            self.open_leafs += 1
            child_trees.append(self.build_child_tree(parent))
        return child_trees

    def build_child_tree(self, parent):

        next_node_type = random.choice(("operator", "activity"))

        # we track how many open leafs need to be filled while constructing the tree, if there are
        # as many open leafs as there are remaining activities, then all open leafs need to be filled with an activity
        if len(self.remaining_activities) == self.open_leafs:
            next_node_type = "activity"

        if next_node_type == "activity":
            activity = random.choice(self.remaining_activities)
            # delete chosen leaf node from the list of remaining leaf nodes
            self.remaining_activities.pop(self.remaining_activities.index(activity))
            self.open_leafs -= 1
            return ProcessTree(label=activity, parent=parent)

        if next_node_type == "operator":
            all_operators = (Operator.SEQUENCE, Operator.PARALLEL, Operator.XOR, Operator.OR, Operator.LOOP)
            operator = random.choice(all_operators)
            minimum_number_of_children = 2 if operator != Operator.LOOP else 1
            number_of_children = minimum_number_of_children
            maximum_number_of_children = len(self.remaining_activities) - self.open_leafs - 1
            while number_of_children <= maximum_number_of_children:
                if random.choice((True, False)):
                    number_of_children += 1
                else:
                    break
            self.open_leafs -= 1
            self.open_leafs += number_of_children
            subtree = ProcessTree(operator=operator, parent=parent)
            subtree.children = [self.build_child_tree(parent=subtree) for _ in range(number_of_children)]
            return subtree

    def return_process_tree(self):
        return self.process_tree


def pm4py_process_tree_generator(parameters: dict = None):
    """
    :param parameters: dictionary containing everything about the process tree. The standard parameters are:
    parameters = {
        "mode": 20,
        "min": 10,
        "max": 30,
        "sequence": 0.25,
        "choice": 0.25,
        "parallel": 0.25,
        "loop": 0.25,
        "or": 0.0,
        "silent": 0.2,
        "duplicate": 0,
        "no_models": 1
    }
    :return: process tree
    """
    tree = pm4py.generate_process_tree()
    return tree


"""
following a little example on how you would manually build a process tree
"""
# Leaf nodes (activities)
A = ProcessTree(label='a')
B = ProcessTree(label='b')
C = ProcessTree(label='c')
D = ProcessTree(label='d')
E = ProcessTree(label='e')
F = ProcessTree(label='f')

# Inner nodes (operators)
seq_node = ProcessTree(operator=Operator.SEQUENCE, children=[E, F])
choice_node = ProcessTree(operator=Operator.XOR, children=[D, seq_node])
loop_node = ProcessTree(operator=Operator.LOOP, children=[choice_node])
root_node = ProcessTree(operator=Operator.SEQUENCE, children=[A, loop_node])

loop_node.parent = root_node
A.parent = root_node
choice_node.parent = loop_node
seq_node.parent = choice_node
D.parent = choice_node
E.parent = seq_node
F.parent = seq_node

# pm4py.view_process_tree(root_node)
# print(root_node)

def pm4py_process_tree_string_to_object(process_tree_string):
    with open("../pm4py_generated_models_and_descriptions/0_process_tree_revised_byChatGPT.txt", "r") as file:
        process_description = file.read()
    pm4py.convert_to_process_tree(process_tree_string)
