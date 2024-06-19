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

from pm4py.statistics.variants.log import get

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
import os
number_of_generated_examples = 100

current_path= os.path.dirname(os.path.abspath(__file__))


def load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting():
    # load process tree
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)

        retrieve_file_path("ptml", process_id)

        description_of_simulated_process_tree_path = f"../pm4py_generated_models_and_descriptions/{process_id}_process_tree_description_based_on_few_shot_prompting.txt"
        description_text_file = open(description_of_simulated_process_tree_path, "x")
        # TODO Write Few Shot Prompt for in Context learning
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'system': 'test',
                'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                           f'You are an expert in process modeling, especially by using process trees and you can easily '
                           f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
                           f' This is what I exemplary expect you to do: '
                           f" process tree 1: +( 'analyze', *( 'implement', +( 'assess', 'produce' ) ) ), X( 'review', 'execute' ) ), +( 'refine', 'monitor' ) )"
                           f' The expected description 1: This process starts with analyze, a critical step to understand the context and requirements. It then moves to refine, ensuring all aspects are perfected. Next, implement leads to two nested activities: assess to evaluate the situation and produce to create outputs. Finally, it offers alternative paths: review to check for quality or execute to carry out tasks, ensuring flexibility in workflow management.'
                           f" process tree 2: +( 'plan', *( 'design', +( 'develop', 'integrate' ) ) ), X( 'test', 'document' ) ), +( 'deploy', 'maintain' )" 
                           f' The expected description 2: This process starts with plan, setting the foundation for subsequent steps. It then proceeds to design, leading into a nested sequence where develop creates the core functionality and integrate combines components. The next phase offers alternatives: test to ensure quality or document to record details. Finally, it moves to deploy to launch the product and maintain for ongoing support, ensuring a comprehensive and adaptable workflow.'
                           f" process tree 3: +( 'browse', *( 'select', +( 'order', 'pay' ) ) ), X( 'ship', 'track' ) ), +( 'deliver', 'feedback' ) " 
                           f' The expected description 3: This e-commerce process starts with browse, allowing customers to explore products. Next, they select items, leading to a nested sequence where they order their chosen products and then pay for them. The process provides alternatives: ship the products or track the order status. Finally, it concludes with deliver, ensuring the products reach the customer, and feedback, where customers can provide their input on the experience, ensuring a complete and customer-centric workflow. '
                ,
            },
        ])
        description_text_file.write(f"process tree structure: {process_tree}")
        description_text_file.write("")
        description_text_file.write(response['message']['content'])
        description_text_file.close()
        print(response['message']['content'])

#load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting()

def simulate_process_trees_and_generate_new_descriptions():
    # load process tree
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        print(process_tree)

        playout = pm4py_simulation.apply(process_tree, parameters={})
        variants_dict = get.get_variants_from_log_trace_idx(playout)
        variants_with_amount_list = get.get_variants_sorted_by_count(variants_dict)
        variants = [variant_and_amount[0] for variant_and_amount in variants_with_amount_list]
        print(variants)

        description_of_simulated_process_tree_path = f"../pm4py_generated_models_and_descriptions/{process_id}_process_tree_description_based_on_simulation.txt"
        description_text_file = open(description_of_simulated_process_tree_path, "x")

        # TODO Write Few Shot Prompt for in Context learning
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'system': 'test',
                'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                           f'You are an expert in process modeling, especially by using process trees and you can easily '
                           f'interpret process models. Describe an illustrative and realistic process in detail based on '
                           f'this process tree and the simulated process instances: {process_tree} '
                           f'\n'
                           f'Each tuple in the following list represents a process instance: '
                           f'{variants} '
                           f'\n'
                           f'Make sure that your process description matches the simulated instances, '
                           f'i.e. all  instances should be possible when following your description of the process.'
                ,
            },
        ])
        # print( response['message']['content'])
        # Save new descriptions
        description_text_file.write(f"process tree structure: {process_tree}")
        description_text_file.write("")
        description_text_file.write(response['message']['content'])
        description_text_file.close()
        print(response['message']['content'])

#simulate_process_trees_and_generate_new_descriptions()
load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting()