# from Levenshtein import distance
from Code import String_to_model as s
from pm4py.objects.process_tree.utils import generic as pt_utils
import pm4py
from typing import Set
import pandas as pd
from FileHandling import retrieve_file_path
import os
from dotenv import load_dotenv

load_dotenv()


def export_all_process_models_and_process_descriptions():
    data = []
    total_number_of_processes = int(os.environ.get("NUMBER_OF_PROCESS_MODELS"))

    for process_id in range(total_number_of_processes):
        number_of_activities = process_id % 5 + 5
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        process_tree_string = str(process_tree)
        process_tree_string_with_special_operator_tokens = process_tree_string.replace("->(", "->_token(").replace("X(", "X_token(").replace("+(", "+_token(").replace("*(", "*_token(")
        process_tree_description_path = retrieve_file_path("process_tree_description", process_id)

        system_prompt = """The operators used in a process tree are: ->(...) sequence, X(...) choice, +(...) parallel, *(...) loop. 
        You are an expert in process modeling, especially by using process trees and you can generate process trees based on process descriptions. 
        Given a process description between <description> and </description>, identify activities and identify the control flow in which the activities are performed. Then generate a process tree based on the identified activities and use the defined operators to model the control flow. Respond with the generated process tree between <processtree> and </processtree>."""

        instruction_prompt = """Process trees allow us to model processes that comprise a control-flow hierarchy. 
        A process tree is a mathematical tree, where the internal vertices are operators, and leaves are activities. 
        Operators specify how their children, i.e., sub-trees, need to be combined from a control-flow perspective. 
        There are four operators and each operator has two children: 
        The sequence operator -> specifies sequential behavior, e.g., ->(S1, S2) means that first S1 is executed and then S2. 
        The choice operator X specifies a choice, e.g., X(C1, C2) means that either C1 is executed or C2 is executed. 
        The parallel operator + specifies simultaneous behavior or indifferent executing order, e.g., +(P1, P2) means that P1 is executed while P2 is also executed or that P1 and P2 are both executed independently from another. 
        The loop operator * specifies repetitive behaviour, e.g., *(R1, R2) means that after R1 is executed, R2 could be executed. If R2 is executed then R1 has to be executed again. This implies that the loop only can be left after R1 is executed.
        
        Now your task is to analyze a process description to identify activities within the process description and the relationship between the activities within the process description. 
        Then model a process tree that represents the process within the process description. Use the operators defined above to to model the control flow and use one verb and one noun if possible to model the activities. 
        You can reason step by step to analyze the process description and model the process tree. However, in the end finish your response with 'process_tree=[insert the modelled process tree here].
        The process description you need to analyze and model a process tree for is: '
        """

        instruction_prompt_with_special_tokens_and_same_placeholders = """Process trees allow us to model processes that comprise a control-flow hierarchy. 
        A process tree is a mathematical tree, where the internal vertices are operators, and leaves are activities. 
        Operators specify how their children, i.e., sub-trees, need to be combined from a control-flow perspective. 
        There are four operators and each operator has two children: 
        The sequence operator ->_token specifies sequential behavior, e.g., ->_token(X, Y) means that first X is executed and then Y. 
        The choice operator X_token specifies a choice, e.g., X_token(X, Y) means that either X is executed or Y is executed. 
        The parallel operator +_token specifies simultaneous behavior or indifferent executing order, e.g., +_token(X, Y) means that X is executed while Y is also executed or that X and Y are both executed independently from another. 
        The loop operator *_token specifies repetitive behaviour, e.g., *_token(X, Y) means that after X is executed, Y could be executed. If Y is executed then X has to be executed again. This implies that the loop only can be left after X is executed.

        Now your task is to analyze a process description to identify activities within the process description and the relationship between the activities within the process description. 
        Afterwards model a process tree that represents the process within the process description. Use the operators defined above to to model the control flow and use one verb and one noun if possible to model the activities. 
        You can reason step by step to analyze the process description and model the process tree. However, in the end finish your response with process_tree=[insert the modelled process tree here].
        The process description you need to analyze and model a process tree for is:
        """

        instruction_prompt_with_special_tokens_and_same_placeholders = "Process trees allow us to model processes that comprise a control-flow hierarchy. A process tree is a mathematical tree, where the internal vertices are operators, and leaves are activities.  Operators specify how their children, i.e., sub-trees, need to be combined from a control-flow perspective. There are four operators and each operator has two children:  The sequence operator ->_token specifies sequential behavior, e.g., ->_token(X, Y) means that first X is executed and then Y.  The choice operator X_token specifies a choice, e.g., X_token(X, Y) means that either X is executed or Y is executed.  The parallel operator +_token specifies simultaneous behavior or indifferent executing order, e.g., +_token(X, Y) means that X is executed while Y is also executed or that X and Y are both executed independently from another.  The loop operator *_token specifies repetitive behaviour, e.g., *_token(X, Y) means that after X is executed, Y could be executed. If Y is executed then X has to be executed again. This implies that the loop only can be left after X is executed. Now your task is to analyze a process description to identify activities within the process description and the relationship between the activities within the process description.  Afterwards model a process tree that represents the process within the process description. Use the operators defined above to to model the control flow and use one verb and one noun if possible to model the activities.  You can reason step by step to analyze the process description and model the process tree. However, in the end finish your response with process_tree=[insert the modelled process tree here]. The process description you need to analyze and model a process tree for is: "

        output = "process_tree="+process_tree_string_with_special_operator_tokens

        with open(process_tree_description_path, "r") as file:
            process_description = file.read()
            # Append data to the list
            input = process_description
            text_for_fine_tuning = f"SYSTEM: {system_prompt}\n INPUT: Generate a Process tree based on this process description: <description> {process_description} </description> \n ASSISTANT: The process tree for the given process description is: <processtree>{process_tree}</processtree>",

            # ShareGPT Style conversation
            conversations = [
                {"from": "system", "value": instruction_prompt_with_special_tokens_and_same_placeholders},
                {"from": "human", "value": process_description},
                {"from": "gpt", "value": output},
                # {"role": "user", "content": "And what's its most famous landmark?"}
            ]

            data.append([process_id, number_of_activities, instruction_prompt, instruction_prompt_with_special_tokens_and_same_placeholders, input, output, str(process_tree), conversations, text_for_fine_tuning])



    # Create a DataFrame
    df = pd.DataFrame(data, columns=["Process ID", "Number of Activities", "instruction", "instruction prompt with special tokens and same placeholders", "input", "output", "process tree", "conversations", "text (other format)"])
    df = df.sort_values(by=['Number of Activities', "Process ID"], ascending=True)
    # Export DataFrame to CSV
    csv_training_data_file_path = "process_models_and_process_descriptions_instruction_input_output.csv"
    df.to_csv(csv_training_data_file_path, index=False)
    df.to_parquet("process_models_and_process_descriptions_instruction_input_output.parquet")

    print(f"Data successfully exported to {csv_training_data_file_path}")





def jaccard_set(set1: Set[str], set2: Set[str]) -> Set[str]:
    return set1.intersection(set2)


def jaccard_index(set1: Set[str], set2: Set[str]) -> float:
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


def extract_activities(tree: pm4py.visualization.process_tree) -> Set[str]:
    # Extract activities using the built-in function
    activities = pt_utils.get_leaves(tree)

    # Extract the labels from the leaves
    activity_labels = [activity.label for activity in activities if activity.label is not None]

    # Sort the list alphabetically and then turn the list into a set for set operations
    activity_labels.sort()
    activity_labels = set(activity_labels)
    return activity_labels


"""
# Using Jaccard index on process tree strings; second string has a few underlines ("_")
s1 = "X( ->( 'Create Menu', +( 'Prepare Order', 'Pack Goods' ) ), X( 'Process Payment', +( 'Verify Card', 'Authorize Transaction' ) ) )"
s2 = "X( ->( 'Create Menu', +( 'Prepare Order', 'Pack Goods' ) ), X( 'Process_Payment', +( 'Verify_Card', 'Authorize_Transaction' ) ) )"

# Turning strings passed by the program into trees
t1 = s.string_to_tree(s1)
t2 = s.string_to_tree(s2)

# Extracting activities from the tree
a1 = extract_activities(t1)
a2 = extract_activities(t2)

# Printing results for showcase
print("===================================")
print("A1: ", a1)  # set of activities in process tree 1
print("A2: ", a2)  # set of activities in process tree 2
# print("Levenshtein-distance: ", distance(s1, s2))  # string distance on both process tree strings
print("Jaccard-Set: ", jaccard_set(a1, a2))  # common elements in both sets
print("Jaccard-Index: ", jaccard_index(a1, a2))  # percentage of common elements on all elements
"""

export_all_process_models_and_process_descriptions()