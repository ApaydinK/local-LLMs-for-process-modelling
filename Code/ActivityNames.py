"""
author Kaan Apaydin
This file contains code for generating the activities that should be incorporated into the process models
It contains two lists with the most common verbs and nouns generally and also specifically in a business context
I've also tried using word databases but a random combination there didn't result in anything meaningful
TODO: My Professor had a great idea to prompt an LLM for a next logical activity. Something we should definitely implement
"""
import json
import random
import ollama
import asyncio
from concurrent.futures import ThreadPoolExecutor
from pm4py.objects.process_tree.obj import ProcessTree, Operator


def read_verbs_from_file(file_path):
    """
    function to initialize the list of verbs or nouns below
    :param file_path: the txt file path, where each word is seperated with a sentence break
    :return: list of verbs, all lowercase letters
    """
    verbs = []  # Empty list to hold the verbs
    with open(file_path, 'r') as file:  # Open the file
        for line in file:  # Iterate over each line
            verb = line.strip().lower()  # Process the line to get the verb
            verbs.append(verb)  # Append the verb to the list
    return verbs  # Return the list of verbs


"""
I did already read the files and copy pasted the lists into the variables most_common_nouns and most_common_verbs below
"""
# https://speakspeak.com/resources/general-english-vocabulary/100-essential-business-english-verbs + 150 most common english verbs from another website
# new_common_verbs = read_verbs_from_file("C:/Users/Kaan Apaydin/Downloads/verbs.txt")
# print(new_common_verbs)
# https://speakspeak.com/resources/general-english-vocabulary/100-essential-business-english-nouns + 150 most common nouns from another website
# new_common_nouns = read_verbs_from_file("C:/Users/Kaan Apaydin/Downloads/nouns.txt")
# print(new_common_nouns)

most_common_nouns = ['advantage', 'agenda', 'bill', 'change', 'competition', 'costs', 'deadline', 'decision',
                     'delivery', 'difference', 'employee', 'environment', 'experience', 'factory', 'goal', 'guarantee',
                     'industry', 'inventory', 'limit', 'market', 'objective', 'option', 'payment', 'possibility',
                     'product', 'promotion', 'refund', 'report', 'retailer', 'salary', 'share', 'success', 'support',
                     'turnover', 'advertise', 'apology', 'brand', 'commission', 'competitor', 'creditor', 'debt',
                     'decrease', 'department', 'disadvantage', 'employer', 'equipment', 'explanation', 'fall', 'goods',
                     'improvement', 'instructions', 'invoice', 'loss', 'message', 'offer', 'order', 'penalty',
                     'preparation', 'production', 'purchase', 'reminder', 'responsibility', 'rise', 'sales',
                     'signature', 'suggestion', 'target', 'estimate', 'facilities', 'feedback', 'growth', 'increase',
                     'interest', 'knowledge', 'margin', 'mistake', 'opinion', 'output', 'permission', 'price', 'profit',
                     'reduction', 'repairs', 'result', 'risk', 'schedule', 'stock', 'supply', 'transport', 'people',
                     'history', 'way', 'art', 'world', 'information', 'map', 'two', 'family', 'government', 'health',
                     'system', 'computer', 'meat', 'year', 'thanks', 'music', 'person', 'reading', 'method', 'data',
                     'food', 'understanding', 'theory', 'law', 'bird', 'literature', 'problem', 'software', 'control',
                     'knowledge', 'power', 'ability', 'economics', 'love', 'internet', 'television', 'science',
                     'library', 'nature', 'fact', 'product', 'idea', 'temperature', 'investment', 'area', 'society',
                     'activity', 'story', 'industry', 'media', 'thing', 'oven', 'community', 'definition', 'safety',
                     'quality', 'development', 'language', 'management', 'player', 'variety', 'video', 'week',
                     'security', 'country', 'exam', 'movie', 'organization', 'equipment', 'physics', 'analysis',
                     'policy', 'series', 'thought', 'basis', 'boyfriend', 'direction', 'strategy', 'technology', 'army',
                     'camera', 'freedom', 'paper', 'environment', 'child', 'instance', 'month', 'truth', 'marketing',
                     'university', 'writing', 'article', 'department', 'difference', 'goal', 'news', 'audience',
                     'fishing', 'growth', 'income', 'marriage', 'user', 'combination', 'failure', 'meaning', 'medicine',
                     'philosophy', 'teacher', 'communication', 'night', 'chemistry', 'disease', 'disk', 'energy',
                     'nation', 'road', 'role', 'soup', 'advertising', 'location', 'success', 'addition', 'apartment',
                     'education', 'math', 'moment', 'painting', 'politics', 'attention', 'decision', 'event',
                     'property', 'shopping', 'student', 'wood', 'competition', 'distribution', 'entertainment',
                     'office', 'population', 'president', 'unit', 'category', 'cigarette', 'context', 'introduction',
                     'opportunity', 'performance', 'driver', 'flight', 'length', 'magazine', 'newspaper',
                     'relationship']

most_common_verbs = ['accept', 'achieve', 'admit', 'affect', 'afford', 'agree', 'allow', 'answer', 'apply', 'argue',
                     'arrange', 'arrive', 'ask', 'avoid', 'become', 'begin', 'believe', 'build', 'buy', 'call', 'could',
                     'create', 'cross', 'cut', 'damage', 'deal', 'deliver', 'deny', 'depend', 'describe', 'destroy',
                     'develop', 'disappear', 'discover', 'do', 'dress', 'drink', 'drive', 'eat', 'encourage', 'happen',
                     'have', 'hear', 'help', 'hide', 'hold', 'hope', 'identity', 'imagine', 'improve', 'increase',
                     'influence', 'inform', 'invite', 'involve', 'join', 'keep', 'know', 'last', 'laugh', 'open',
                     'order', 'own', 'pay', 'perform', 'play', 'point', 'prefer', 'prepare', 'press', 'prevent',
                     'produce', 'protect', 'provide', 'push', 'reach', 'read', 'receive', 'record', 'reduce', 'share',
                     'shoot', 'show', 'sing', 'sit', 'sleep', 'smile', 'sound', 'speak', 'stand', 'start', 'state',
                     'study', 'succeed', 'suggest', 'supply', 'suppose', 'survive', 'take', 'talk', 'care', 'carry',
                     'catch', 'cause', 'change', 'check', 'choose', 'clear', 'clean', 'collect', 'come', 'complain',
                     'complete', 'consist', 'contain', 'continue', 'contribute', 'control', 'correct', 'cost', 'enjoy',
                     'exist', 'expect', 'experience', 'explain', 'express', 'face', 'fall', 'feel', 'find', 'finish',
                     'fly', 'follow', 'forget', 'forgive', 'form', 'get', 'give', 'go', 'grow', 'learn', 'leave',
                     'lend', 'like', 'limit', 'listen', 'live', 'look', 'love', 'make', 'matter', 'mean', 'measure',
                     'meet', 'mention', 'mind', 'move', 'must', 'need', 'offer', 'regard', 'relate', 'release',
                     'remember', 'remove', 'repeat', 'replace', 'reply', 'report', 'result', 'return', 'reveal',
                     'rise', 'run', 'save', 'say', 'see', 'sell', 'send', 'set', 'tell', 'tend', 'think', 'throw',
                     'touch', 'train', 'travel', 'treat', 'try', 'turn', 'understand', 'use', 'visit', 'wait', 'want',
                     'walk', 'watch', 'win', 'wonder', 'write', 'accept', 'advertise', 'approve', 'borrow', 'buy',
                     'cancel', 'check', 'complete', 'convince', 'decrease', 'dismiss', 'divide', 'encourage',
                     'exchange', 'fix', 'improve', 'install', 'join', 'lower', 'measure', 'order', 'own', 'pay',
                     'prevent', 'promise', 'purchase', 'receive', 'refuse', 'remove', 'respond', 'sell', 'shorten',
                     'succeed', 'add', 'advise', 'authorize', 'break', 'calculate', 'change', 'choose', 'confirm',
                     'count', 'deliver', 'dispatch', 'drop', 'establish', 'extend', 'fund', 'increase', 'invest',
                     'lend', 'maintain', 'mention', 'organise', 'pack', 'plan', 'process', 'promote', 'raise',
                     'recruit', 'reject', 'reply', 'return', 'send', 'split', 'suggest', 'admit', 'afford', 'avoid',
                     'build', 'call', 'charge for', 'complain', 'consider', 'decide', 'develop', 'distribute', 'employ',
                     'estimate', 'fall', 'get worse', 'inform', 'invoice', 'lengthen', 'manage', 'obtain', 'owe',
                     'participate', 'present', 'produce', 'provide', 'reach', 'reduce', 'remind', 'resign', 'rise',
                     'separate', 'structure', 'write', '']


def generate_random_activities(number_of_activities):
    """
    :param number_of_activities: how many activity pairs do you need?
    :return: list of activies in the form ["random_verb1 random_noun1", "random_verb2 random_noun2", ...]
    """
    activities = []
    for i in range(number_of_activities):
        random_verb = random.choice(list(most_common_verbs))
        random_noun = random.choice(list(most_common_nouns))
        activities.append(f"{random_verb} {random_noun}")
    return activities


executor = ThreadPoolExecutor(max_workers=1)


async def async_llm_picks_best_starting_activity(operator):
    operator_translation = ""
    match operator:
        case "->":
            operator_translation = "sequence"
        case "+":
            operator_translation = "parallel"
        case "X":
            operator_translation = "xor"
        case "O":
            operator_translation = "or"
        case "*":
            operator_translation = "loop"

    candidate_activities = generate_random_activities(number_of_activities=10)
    loop = asyncio.get_running_loop()

    response = await loop.run_in_executor(
        executor,
        ollama.chat,
        'llama3',
        [
            {
                'role': 'user',
                'content': f'You are an expert in process modeling using process trees.'
                           f'Help to build an illustrative and realistic example for a process tree that begins with a {operator} {operator_translation} operator. '
                           f'by picking one of the verb noun combinations from the following list that is going to be the start activity of the process: {candidate_activities}'
                           f'Your answer will be used as the starting activity name, so only exactly answer with the activity and the noun you have picked. Nothing else.',
            },
        ]
    )
    # Assuming the response structure you need to adjust to your actual response format
    starting_activity = response['message']['content']
    print(starting_activity)
    return starting_activity


async def replace_activity_names(process_tree):
    loop = asyncio.get_running_loop()
    response = await loop.run_in_executor(
        executor,
        ollama.chat,
        'llama3',
        [
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
                'role': 'user',
                'content': f"You are an expert in process trees. I will present you a structure of a process tree "
                           f"where the activities are abstracted by letters. Make an illustrative and realistic "
                           f"example based on the following process tree structure be suggesting how each letter "
                           f"should be replaced by one verb followed by one noun to represent a real activity: " +
                           f"{process_tree}" +
                           "Describe the process in detail after replacing the letters with activities.  Finally "
                           "complete this dictionary that represents the mapping of the letters with your activities: "
                           "illustrative_and_realistic_activities = {" +
                           "'a'=''," +
                           "'b'=''," +
                           "'c'=''," +
                           "'d'=''," +
                           "'e'=''," +
                           "'f'=''," +
                           "'g'=''," +
                           "'h'=''," +
                           "'i'=''," +
                           "'j'=''," +
                           # "'k'=''," +
                           # "'l'=''," +
                           # "'m'=''," +
                           # "'n'=''," +
                           # "'o'=''," +
                           # "'p'=''," +
                           # "'q'=''," +
                           # "'r'=''," +
                           # "'s'=''," +
                           # "'t'=''," +
                           # "'u'=''," +
                           # "'v'=''," +
                           "}"
                ,
            },
        ]


    )
    # Assuming the response structure you need to adjust to your actual response format
    answer_with_mappings = response['message']['content']
    print(answer_with_mappings)
    illustrative_and_realistic_activity_mappings = extract_dict_from_string(answer_with_mappings)

    replace_activity_labels_in_process_tree(process_tree, illustrative_and_realistic_activity_mappings)

    """
    loop2 = asyncio.get_running_loop()
    response2 = await loop2.run_in_executor(
        executor,
        ollama.chat,
        'llama3',
        [
            {
                'role': 'user',
                'content': f"Extract the python dictionary and only answer with the python dictionary {answer_with_mappings}"
            },
        ]
    )
    # Assuming the response structure you need to adjust to your actual response format
    mappings_only = response2['message']['content']

    # mappings_only: dict = {}
    # mappings_only = json.JSONDecoder(mappings_only)

    print(mappings_only)
    print(extract_dict_from_string(mappings_only))
    """

    return process_tree


def extract_dict_from_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        extract_dict_from_string(content)


def extract_dict_from_string(content):
    start = content.find('{')
    end = content.rfind('}') + 1

    if start == -1 or end == -1:
        raise ValueError("Dictionary not found in the file")

    # Extract the dictionary part
    dict_str = content[start:end]

    # Convert string to dictionary
    mappings_dict = eval(dict_str)

    return mappings_dict


def replace_activity_labels_in_process_tree(root_node: ProcessTree, activity_mappings: dict):
    for child in root_node.children:
        if not child.children:
            try:
                if activity_mappings[child.label] != '':
                    child.label = activity_mappings[child.label]
            except:
                "activity couldn't be replaced, continue.."
        elif child.children:
            replace_activity_labels_in_process_tree(child, activity_mappings)


import re
from FileHandling import retrieve_file_path
import pm4py
import shutil
import os

number_of_generated_examples = 100


def load_and_update_all_process_trees_activity_labels_again():
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        # store visualization of the process graph
        update_activity_labels_in_process_tree_to_adhere_to_the_verb_noun_standard(process_tree)

        pm4py.write_ptml(process_tree, f"../updated_process_trees/{process_id}_process_tree.ptml")


def load_and_update_all_process_trees_activity_labels():
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        # store visualization of the process graph
        update_activity_labels_in_process_tree_to_adhere_to_the_verb_noun_standard(process_tree)

        process_tree_image_file_path = f"../process_models_and_descriptions/{process_id}_process_tree.png"
        pm4py.vis.save_vis_process_tree(process_tree, process_tree_image_file_path)
        print(process_tree)

        # convert process tree to a BPMN graph and store the visualization
        bpmn_graph = pm4py.convert_to_bpmn(process_tree)
        bpmn_image_file_path = f"../process_models_and_descriptions/{process_id}_bpmn.png"
        pm4py.vis.save_vis_bpmn(bpmn_graph, bpmn_image_file_path)

        # convert process tree to a petri net and store the visualization
        net, im, fm = pm4py.convert_to_petri_net(process_tree)
        petri_net_image_file_path = f"../process_models_and_descriptions/{process_id}_petri_net.png"
        pm4py.vis.save_vis_petri_net(net, im, fm, petri_net_image_file_path)

        # Copy the description.txt file to the new destination folder
        source_description_file = retrieve_file_path("process_tree_description", process_id)
        destination_folder = f"../process_models_and_descriptions"
        shutil.copy(source_description_file, destination_folder)

        # Copy the .ptml file
        source_description_file = retrieve_file_path("ptml", process_id)
        shutil.copy(source_description_file, destination_folder)


def update_activity_labels_in_process_tree_to_adhere_to_the_verb_noun_standard(root_node: ProcessTree):
    for child in root_node.children:
        if not child.children:
            try:
                child.label = update_activity_label_to_adhere_to_the_verb_noun_standard(child.label)
            except:
                "activity couldn't be replaced, continue.."
        elif child.children:
            update_activity_labels_in_process_tree_to_adhere_to_the_verb_noun_standard(child)


def update_activity_label_to_adhere_to_the_verb_noun_standard(activity_label):
    if is_camel_case(activity_label) or is_pascal_case(activity_label):
        # Convert camelCase or PascalCase to snake_case
        activity_label = re.sub(r'(?<!^)(?=[A-Z])', '_', activity_label).lower()

    # Split the snake_case string into words
    activity_label = activity_label.replace('_', ' ')

    activity_label = capitalize_words_custom(activity_label)

    return activity_label


def is_camel_case(s):
    # Regular expression to match camelCase
    camel_case_pattern = re.compile(r'^[a-z]+[a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*$')
    return bool(camel_case_pattern.match(s))


def is_pascal_case(s):
    # Regular expression to match PascalCase
    pascal_case_pattern = re.compile(r'^[A-Z][a-zA-Z0-9]*$')
    return bool(pascal_case_pattern.match(s))


def is_snake_case(s):
    # Regular expression to match snake_case
    snake_case_pattern = re.compile(r'^[a-z]+(_[a-z0-9]+)*$')
    return bool(snake_case_pattern.match(s))


def capitalize_words_custom(s):
    words = s.split()  # Split the string into words
    capitalized_words = [word.capitalize() for word in words]  # Capitalize each word
    return ' '.join(capitalized_words)  # Join the words back with spaces

#load_and_update_all_process_trees_activity_labels_again()
#load_and_update_all_process_trees_activity_labels()
"""
# Example usage:
input_string_1 = "runFast"
input_string_2 = "Run_fast"
input_string_3 = "jumpHigh"
input_string_4 = "jump High"
input_string_5 = "Jump high"
input_string_6 = "jump"
input_string_7 = "Jump a_meter"
input_string_8 = "JumpReallyHigh"

print(f"{input_string_1}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_1}"))
print(f"{input_string_2}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_2}"))
print(f"{input_string_3}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_3}"))
print(f"{input_string_4}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_4}"))
print(f"{input_string_5}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_5}"))
print(f"{input_string_6}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_6}"))
print(f"{input_string_7}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_7}"))
print(f"{input_string_8}: " + update_activity_labels_to_adhere_to_the_verb_noun_standard(f"{input_string_8}"))
"""

"""
I have tried using word libraries and installed their word databases but it contains too many words that we wouldn't use
and do not make any sense in combination
"""
"""
import nltk
from nltk.corpus import wordnet as wn
nltk.corpus import wordnet2022 as wn2
nltk.download()

# Function to get a random noun
nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
verbs = {x.name().split('.', 1)[0] for x in wn.all_synsets('v')}

def get_random_noun():
    return random.choice(list(nouns))


# Function to get a random verb
def get_random_verb():
    return random.choice(list(verbs))

# Example usage
random_verb = get_random_verb()
random_noun = get_random_noun()
print(f"Random Verb: {random_verb}")
print(f"Random Noun: {random_noun}")


def generate_really_random_activities(number_of_activities):
    activities = []
    for i in range(number_of_activities):
        random_verb = get_random_verb()
        random_noun = get_random_noun()
        activities.append(f"{random_verb} {random_noun}")
    return activities

"""
