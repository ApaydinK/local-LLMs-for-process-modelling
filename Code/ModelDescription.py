"""
author Kaan Apaydin
This file contains code for describing the process model.
"""

import ollama
import pm4py
from pm4py.objects.process_tree.obj import ProcessTree, Operator


def description_with_local_llm(process_tree):
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f'You are an expert in process modeling, especially by using process trees and you can easily '
                       f'interpret process models. Make a detailed process description based on this process tree: {process_tree}',
        },
    ])
    print(response['message']['content'])


def describe_with_local_llm_and_store_description(process_tree, description_of_process_tree_path):
    description_text_file = open(description_of_process_tree_path, "x")

    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'system': 'test',
            'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                       f'You are an expert in process modeling, especially by using process trees and you can easily '
                       f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}',
        },
    ])
    #print( response['message']['content'])
    description_text_file.write(f"process tree structure: {process_tree}")
    description_text_file.write(response['message']['content'])
    description_text_file.close()


def pm4py_abstraction_of_petri_net(net, im, fm):
    """
    Not natural language text at all unfortunately...
    :param net: Petri Net
    :param im: Initial Markings
    :param fm: Final Markings
    :return: Text that contains the places, transitions and arcs, as well as the initial and final markings but in object form
    """
    abstraction = pm4py.llm.abstract_petri_net(net, im, fm)
    return abstraction


def process_tree_to_text(process_tree: ProcessTree):
    """
    Our own implementation to translate a process tree into natural language text
    :param process_tree: Process Tree
    :return: A description of the process tree
    """
    # whole_process_tree = ProcessTree(operator=Operator.SEQUENCE,
    #                                 children=[A, ProcessTree(operator=Operator.LOOP, children=[
    #                                     ProcessTree(operator=Operator.XOR, children=[D, ProcessTree(
    #                                         operator=Operator.SEQUENCE, children=[E, F])])])])
    translation_for_starting_operators = {
        "sequence": "On the highest level the process contains {number_of_children} that are executed after another.",
        "sequence1": "The process is composed of {number_of_children} that are sequentially done.",
        "sequence2": "..."

    }
