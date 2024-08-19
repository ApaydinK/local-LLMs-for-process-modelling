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
            "role": "system",
            "content": "You are an expert in process trees. Process trees allow to model processes that comprise a control-flow hierarchy. "
                       "A process tree is a mathematical tree, where the internal vertices are operators, and leaves are activities.  "
                       "Operators specify how their children, i.e., sub-trees, need to be combined from a control-flow perspective. "
                       "There are four operators and each operator has two children:  "
                       "The sequence operator -> specifies sequential behavior, e.g., ->(X, Y) means that first X is executed and then Y. "
                       "The choice operator X specifies a choice, e.g., X(X, Y) means that either X is executed or Y is executed. "
                       "The parallel operator + specifies simultaneous behavior or indifferent executing order, e.g., +(X, Y) means that X is executed while Y is also executed or that X and Y are both executed independently from another. "
                       "The loop operator * specifies repetitive behaviour, e.g., *(X, Y) means that after X is executed, Y could be executed. If Y is executed then X has to be executed again. This implies that the loop only can be left after X is executed. "

        },
        {
            "role": "user",
            "content": f'Your task is to describe an illustrative and realistic process in detail based on a process tree. '
                       f'This is what I exemplary would expect you to do: '
                       f"\n process tree 1: ->( 'Order Pizza', ->( X( *( 'Cut Toppings', 'Assemble Slices' ), 'Design Pattern' ), ->( 'Bake Crust', 'Serve Fresh' ) ) )"
                       f'\n The expected description 1: Every process begins when a pizza is ordered. Some pizzas only require designing a pattern before the crust is baked and everything is served fresh, other pizzas require toppings that needs to be cut before the crust is baked and the pizza is freshly served. Rarely toppings need not only to be cut but also followed by an assembly of the topping slices. If the slices need to be assembled then toppings need to be cut again. As soon as all toppings are cut and no further assembling of slices is needed, the curst can be baked and the pizza can be served fresh. '
                       f"\n process tree 2: *( 'Hire Engineer', ->( 'Review Proposal', *( 'Design Blueprint', ->( 'Implement Plan', 'Approve Budget' ) ) ) )"
                       f"\n The expected description 2: The process starts with hiring an engineer, which either ends the process directly or triggers a review of an proposal by the engineer. Sometimes our engineers review a proposal so that they can design a blueprint afterwards. If the bluebprint involves to hire a new engineer than another engineer is hired and the process could end again or as well trigger the reviewal of a new proposal from the new engineer. If the blueprint does not demand to hiere a new engineer than a plan is implemented which always leads to approvement of the budget. This implementing plan and approving budget procedure than leads back to design blueprint from where the process continues as described. "
                       f"\n Now describe an illustrative and realistic process in detail based on this process tree: {process_tree} "

        }
    ])

    # print( response['message']['content'])
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


from FileHandling import retrieve_file_path
import os

number_of_generated_examples = 100

current_path = os.path.dirname(os.path.abspath(__file__))
description_path = os.path.join(os.path.dirname(current_path), 'pm4py_fewshot_prompting')


def load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting():
    # load process tree
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)

        retrieve_file_path("ptml", process_id)

        description_of_simulated_process_tree_path = f"{description_path}/{process_id}_process_tree_description_based_on_few_shot_prompting.txt"
        description_text_file = open(description_of_simulated_process_tree_path, "x")
        # TODO Write Few Shot Prompt for in Context learning
        response = ollama.chat(model='llama3', messages=[
            {
                'role': 'user',
                'system': 'test',
                'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                           f'You are an expert in process modeling, especially by using process trees and you can easily '
                           f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
                           f'The description should be in human-readable text without operators or process tree. No yapping.'
                           f' This is what I exemplary expect you to do: '
                           f" process tree 1: +( 'analyze', *( 'implement', +( 'assess', 'produce' ) ) ), X( 'review', 'execute' ) ), +( 'refine', 'monitor' ) )"
                           f' The expected description 1: This process starts with analyze, a critical step to understand the context and requirements. It then moves to refine, ensuring all aspects are perfected. Next, implement leads to two nested activities: assess to evaluate the situation and produce to create outputs. Finally, it offers alternative paths: review to check for quality or execute to carry out tasks, ensuring flexibility in workflow management.'
                           f" process tree 2: +( 'Plan Project', *( 'Define Scope', +( 'Design System Architecture', +( 'Develop Features', X( 'Integrate Components', +( 'Test Modules', 'Review Code' ) ) ) ) ) ), X( 'Create Documentation', +( 'Conduct Testing', X( 'User Acceptance Testing', 'Performance Testing' ) ) ) ), +( 'Deploy Solution', +( 'Monitor Performance', 'Implement Maintenance' ) )"
                           f" The expected description 2: This process begins with Plan Project and Define Scope, establishing the project's framework. It then moves to Design System Architecture and Develop Features, creating and building the system. It branches into Integrate Components with options for Test Modules and Review Code. Concurrently, Create Documentation and Conduct Testing with choices for User Acceptance Testing and Performance Testing. Finally, the process includes Deploy Solution, followed by Monitor Performance and Implement Maintenance to ensure ongoing system functionality and updates."
                           f" process tree 3: +( 'Browse Products', *( 'Select Items', +( 'Add to Cart', 'Complete Payment' ) ) ), X( 'Pack Order', 'Track Shipment' ) ), +( 'Deliver Package', 'Collect Feedback' )"
                           f' The expected description 3: This e-commerce process starts with browse products, allowing customers to explore products. Next, they select items, leading to a nested sequence where they order their chosen products and then pay for them. The process provides alternatives: ship the products or track the order status. Finally, it concludes with deliver, ensuring the products reach the customer, and feedback, where customers can provide their input on the experience, ensuring a complete and customer-centric workflow. '
                ,
            },
        ])
        description_text_file.write(f"process tree structure: {process_tree}")
        description_text_file.write("")
        description_text_file.write(response['message']['content'])
        description_text_file.close()
        print(response['message']['content'])


# load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting()

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


# simulate_process_trees_and_generate_new_descriptions()
# load_process_trees_and_generate_new_descriptions_based_on_few_shot_prompting()

"""
messages=[
        {
            'role': 'user',
            'system': 'test',
            'content': f'The operators used in a proces tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. '
                       f'You are an expert in process modeling, especially by using process trees and you can easily '
                       f'interpret process models. Describe an illustrative and realistic process in detail based on this process tree: {process_tree}'
                       f'The description should be in human-readable text without operators or process tree. No yapping.'
                       f' This is what I exemplary expect you to do: '
                       f"\n process tree 1: ->( 'Order_Pizza', ->( X( *( 'Cut_Toppings', 'Assemble_Slices' ), 'Design_Pattern' ), ->( 'Bake_Crust', 'Serve_Fresh' ) ) )"
                       f'\n The expected description 1: Every Process begins when a pizza is ordered. Some pizzas only require designing a pattern before the crust is baked and everything is served fresh, other pizzas require toppings that needs to be cut before the crust is baked and the pizza is freshly served. Rarely toppings need not only to be cut but also followed by an assembly of the topping slices. If the slices need to be assembled then toppings need to be cut again. As soon as all toppings are cut and no further assembling of slices is needed, the curst can be baked and the pizza can be served fresh. '
                       f"\n process tree 2: *( 'Hire Engineer', ->( 'Review Proposal', *( 'Design Blueprint', ->( 'Implement Plan', 'Approve Budget' ) ) ) )"
                       f"\n The expected description 2: The process starts with hiring an engineer, which either ends the process directly or triggers a review of an proposal by the engineer. Sometimes our engineers review a proposal so that they can design a blueprint afterwards. If the bluebprint involves to hire a new engineer than another engineer is hired and the process could end again or as well trigger the reviewal of a new proposal from the new engineer. If the blueprint does not demand to hiere a new engineer than a plan is implemented which always leads to approvement of the budget. This implementing plan and approving budget procedure than leads back to design blueprint from where the process continues as described. "
        },
    ]
"""
