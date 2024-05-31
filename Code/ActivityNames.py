"""
author Kaan Apaydin
This file contains code for generating the activities that should be incorporated into the process models
It contains two lists with the most common verbs and nouns generally and also specifically in a business context
I've also tried using word databases but a random combination there didn't result in anything meaningful
TODO: My Professor had a great idea to prompt an LLM for a next logical activity. Something we should definitely implement
"""
import random
import ollama
import asyncio
from concurrent.futures import ThreadPoolExecutor

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
"""
def llm_picks_best_starting_activity(node):
    candidate_activities = generate_random_activities(number_of_activities=10)
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f'You are an expert in process modeling using process trees.'
                       f'Help to build an illustrative and realistic example for a process tree that begins with a {node}.'
                       f'by picking one of the verb noun combinations from the following list that is going to be the start activity of the process: {candidate_activities}'
                       f'Your answer will be used as the starting activity name, so only exactly answer with the activity and the noun you have picked. Nothing else.',
        },
    ])
    print(response['message']['content'])
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
