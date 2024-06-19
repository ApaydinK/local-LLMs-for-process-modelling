"""
author Kaan Apaydin
This file contains code for describing the process model.
"""

import ollama
import pm4py
from pm4py.objects.process_tree.obj import ProcessTree, Operator
import pm4py.algo.simulation.playout.process_tree.algorithm as pm4py_simulation


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
                       f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
            ,
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
from UI_customTK import retrieve_file_path
number_of_generated_examples = 100
def load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting(process_tree: ProcessTree):
    # load process tree
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        tree = pm4py.read_ptml(ptml_file_path)

    retrieve_file_path("ptml", 1)

    description_text_file = open(description_of_process_tree_path, "x")
    # TODO Write Few Shot Prompt for in Context learning
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'system': 'test',
            'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                       f'You are an expert in process modeling, especially by using process trees and you can easily '
                       f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
                       f' This is what I exemplary expect you to do: '
                       f' <<process tree >>'
                       f' The expected description'
                       f' <<process tree2 >>'
                       f' The expected description2'
                       f' <<process tree3 >>'
                       f' The expected description3'
            ,
        },
    ])
    # print( response['message']['content'])
    # Save new descriptions
    description_text_file.write(f"process tree structure: {process_tree}")
    description_text_file.write(response['message']['content'])
    description_text_file.close()


def simulate_process_trees_and_generate_new_descriptions():
    # load process tree
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        tree = pm4py.read_ptml(ptml_file_path)
        print(tree)
    """
    # playout = pm4py_simulation.extensive(process_tree)
    tree = pm4py.read_ptml("tests/input_data/running-example.ptml")
    description_text_file = open(description_of_process_tree_path, "x")
    # TODO Write Few Shot Prompt for in Context learning
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'system': 'test',
            'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                       f'You are an expert in process modeling, especially by using process trees and you can easily '
                       f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
                       f' This is what I exemplary expect you to do: '
                       f' <<process tree >>'
                       f' The expected description'
                       f' <<process tree2 >>'
                       f' The expected description2'
                       f' <<process tree3 >>'
                       f' The expected description3'
            ,
        },
    ])
    # print( response['message']['content'])
    # Save new descriptions
    description_text_file.write(f"process tree structure: {process_tree}")
    description_text_file.write(response['message']['content'])
    description_text_file.close()"""

simulate_process_trees_and_generate_new_descriptions()