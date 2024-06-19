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
                           f' This is how I would describe process trees, and what I would expect you to do: '
                           f" process tree 1: ->( X( 'Receive_Order', +( 'Place_Order_for_Supply_Chains', 'Fill_Consolidation_Orders' ) ), ->( 'Confirm_Product_Return', 'Process_Returned_Items' ) ) "
                           f' The expected description for process tree 1: The process either starts with receive order or with the two activities "place order for supply chains" and "fill consolidation order" whose order does not matter. Afterwards the sales department confirms the product return, so that the returned items are processed.'
                           f' An alternative expected description for process tree 1: The initial trigger that sets off the entire process is either the receival of an order or a parallel subprocess. The parallel subprocess consists of the activities "place order for supply chains" and "fill consolidation order". Once the receival of an order or the parallel subprocesses finishes, the focus shifts to handling product returns. For this, the product return has to be confirmed. Once the return is confirmed, the returned items are processed.'
                           f" process tree 2: ->( 'Order_Pizza', ->( X( 'Design_Pattern', *( 'Cut_Toppings', 'Assemble_Slices' ) ), ->( 'Bake_Crust', 'Serve_Fresh' ) ) ) " 
                           f' The expected description for process tree 2: Every Process begins when a pizza is ordered. Some pizzas only require designing a pattern before the crust is baked and everything is served fresh, other pizzas require toppings that needs to be cut before the curst is baked and the pizza is freshly served. Rarely toppings need not only to be cut but also followed by an assembly of the topping slices. If the slices need to be assembled then toppings need to be cut again. As soon as all toppings are cut and no further assembling of slices is needed, the curst can be baked and the pizza can be served fresh. '     f" process tree 3: +( 'browse', *( 'select', +( 'order', 'pay' ) ) ), X( 'ship', 'track' ) ), +( 'deliver', 'feedback' ) "
                           f" process tree 3: +( ->( ->( 'design', *( 'compile', +( 'evaluate', 'generate' ) ) ), X( 'validation', 'test' ) ), +( 'optimize', 'process' ) )"
                           f' The expected description for process tree 3: Optimization and processing has to be done once but it does not matter when next to the main work. The main work starts with designing. Then compiling the designed code into an executable form. Evaluate the compiled code against a set of predefined criteria or metrics, such as performance, security, or usability. Sometimes the evaluation is done first and then the generation. If generations and evaluations are performed then this leads to a restart of compile. Finally the compiled code is ready to be either validated by a focus group or tested by the developer. '
                           f" process tree 4: process tree structure: *( X( 'Create_Report', ->( 'Review_Document', ->( 'Prepare_Proposal', X( 'Gather_Data', 'Analyze_Findings' ) ) ) ), +( 'Schedule_Meeting', +( 'Hold_Video_Call', X( 'Invite_Collaborators', 'Brainstorm_Ideas' ) ) ) )"
                           f' The expected description for process tree 4: This process can be finished quickly but sometimes it takes more input and feedback. So sometimes the organization just creates a report and then the process is already finished. In other instances the organization reviews a document and then prepares a research proposal, because they feel so inspired by the new information. The proposal then is finalized by analyzing findings and making any necessary adjustments or gathering additional data to be presented. However, sometimes additional information is needed. In this case, a meeting with the professor is scheduled as well as a video call with the project partner is hold. The meeting with the professor and the project partners are independend from each other. Also a decision has to be made about inviting more collaborators with expertise or simply conduct a brainstorming session to gather ideas from the people already involved in the proposal. If additional information is gathered in this way, then the process is kicked off again, i.e. either a report is created or the new document is reviewed etc. '
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