import os
import json

current_path= os.path.dirname(os.path.abspath(__file__))
samples_path = os.path.join(os.path.dirname(current_path), 'Samples')

from dotenv import load_dotenv
load_dotenv()
from openai import OpenAI
client = OpenAI(api_key=os.getenv('openai_api_key'))

from pm4py.objects.process_tree.obj import ProcessTree, Operator
import json
import os
import random
from ActivityNames import generate_random_activities, most_common_nouns, most_common_verbs
from ProcessTree import root_node
from DecodeEncode import illustrative_and_realistic_activities #replace_activity_labels_in_process_tree, serialize_process_tree, 


def generate_activity_mappings(num_activities=10):
    prompt = (f"Generate a list of {num_activities} realistic business activities for a process tree",
              f"Please list activities in the form of verb-noun pairs, such as 'Review Order' or 'Send Email'. ")
    response = client.chat.completions.create(
            model='gpt-3.5-turbo-0125',
            messages=[
                {'role': 'system', 'content': 'You are an expert in business process and consultant.'},
                {'role': 'user', 'content': prompt},
            ],
            max_tokens=100,
            temperature=0.7,
            n = 1,
            stop=None
        )
    
    activities = response.choices[0].message.content.strip().split('\n')
    activities = [activity.strip() for activity in activities if activity.strip()]
    activities = [activity.replace('-', ' ').title() for activity in activities]

    activity_mappings = {chr(97 + i): activities[i] for i in range(min(len(activities), 26))}  # Map to a-z letters

    return activity_mappings


def generate_random_process_tree(activity_mappings, min_activities=4):
    """
    Arg:
    - activity mappings: map the list of all activities
    - min_activities: low boundary for amount of activities

    Return:
    - root: use as a base to check the nodes and its children

    Process:
    1. set a random number of activities
    2. Choose activities randomly based on the num_activities
    3. loop search to get all root children
    """
    activities = list(activity_mappings.keys())
    num_activities = random.randint(min_activities, len(activities))
    chosen_activities = random.sample(activities, num_activities)
    root = ProcessTree(operator=Operator.SEQUENCE)
    #root_node = ProcessTree(operator=Operator.SEQUENCE, children=[A, loop_node]) # from ProcessTree
    
    ## generate no operator, need to add more operator processes
    #for activity_label in chosen_activities:
    #    activity_node = ProcessTree(label=activity_label)
    #    root.children.append(activity_node)
    while chosen_activities:
        sub_tree_size = random.randint(1, len(chosen_activities))
        sub_activities = chosen_activities[:sub_tree_size]
        chosen_activities = chosen_activities[sub_tree_size:]
        
        if len(sub_activities) == 1:
            leaf_node = ProcessTree(label=sub_activities[0])
            root.children.append(leaf_node)
        else:
            sub_tree = generate_sub_tree(sub_activities)
            root.children.append(sub_tree)
    
    return root

# Logical operators
def generate_sub_tree(activities):
    operator = random.choice([Operator.SEQUENCE, Operator.PARALLEL, Operator.XOR, Operator.LOOP])
    sub_tree = ProcessTree(operator=operator)
    
    for activity in activities:
        leaf_node = ProcessTree(label=activity)
        sub_tree.children.append(leaf_node)
    
    return sub_tree

# Based on Kaan's work, change a bit the logic
# Replace activity labels in process tree with logic if not containing any children in root, from activity_mappings, get label. Otherwise performing replacement
def replace_activity_labels_in_process_tree_v2(root_node, activity_mappings):
    if not root_node.children:
        root_node.label = activity_mappings.get(root_node.label, root_node.label)
    else:
        for child in root_node.children:
            replace_activity_labels_in_process_tree_v2(child, activity_mappings)

# Serialize the process tree to JSON, use .children instead of is_leaf() 
def serialize_process_tree_v2(node):
    node_data = {
        'type': 'leaf' if not node.children else 'operator',
        'label': node.label if not node.children else None,
        'operator': node.operator.name if node.children else None,
        'children': [serialize_process_tree_v2(child) for child in node.children] if node.children else []
    }
    return node_data

# Describe the serialized process tree (json) with GPT-3.5
def generate_process_description_gpt(process_tree_json):
    prompt = "Provide a detailed description for the following business process tree {process_tree_json} in json format."
    response = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        response_format={ "type": "json_object" },
        messages=[
            {'role': 'system', 'content': f'You are an expert in process modeling, especially by using process trees and you can easily interpret process models.'},
            {'role': 'user', 'content': prompt},
        ],
        max_tokens=300,
        temperature=0.7,
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content.strip(), process_tree_json

# Full run of process
def generate_description_one_example(samples_path, activity_mappings, min_activities=4):
    response_path = os.path.join(samples_path, 'descriptions_samples.json')

    # Reasure that the new generated description do not overlap the current info in json file
    if os.path.exists(response_path):
        with open(response_path, 'r') as file:
            samples = json.load(file)
    else:
        samples = []

    # Generate a random process tree with generated activities
    process_tree = generate_random_process_tree(activity_mappings, min_activities)
    
    # Replace activity labels with realistic ones
    replace_activity_labels_in_process_tree_v2(process_tree, activity_mappings)
    
    # Serialize the process tree (flatten the process with JSON)
    serialized_tree = serialize_process_tree_v2(process_tree)
    
    # Based on serialized process tree, generate a description
    #process_description = generate_process_description_gpt(serialized_tree)
    
    # Storing process in Json format
    final_description = {
        "Note": f"Sample 1 with {min_activities} activities",
        "Realistic Process": illustrative_and_realistic_activities, #activity_mappings, # this is the illustration_and_realistic (sample)
        "Serialized Process Tree": serialized_tree,
        #"Description": process_description
    }
    samples.append(final_description)
    
    response_path = os.path.join(samples_path, 'descriptions_samples.json')
    with open(response_path, 'w') as f:
        json.dump(samples, f, indent=6) #[final_description]

    print(f"Process Tree: {json.dumps(serialized_tree, indent=6)}")
    #print(f"Process Description: {process_description}")

# Generate multiple sample descriptions
def generate_description_multi_examples(samples_path, activity_mappings, min_activities=4, num_samples=2):
    response_path = os.path.join(samples_path, 'descriptions_samples.json')

    # Reasure that the new generated description do not overlap the current info in json file
    if os.path.exists(response_path):
        with open(response_path, 'r') as file:
            samples = json.load(file)
    else:
        samples = []

    for i in range(num_samples):
        print(f"############ Sample {i} is processing...")
        process_tree = generate_random_process_tree(activity_mappings, min_activities)
        replace_activity_labels_in_process_tree_v2(process_tree, activity_mappings)
        serialized_tree = serialize_process_tree_v2(process_tree)
        process_description, process_tree_json = generate_process_description_gpt(serialized_tree)

        final_description = {
            "Note": f"Sample {i+1} with following activities",
            "Realistic Process": illustrative_and_realistic_activities, #activity_mappings, # this is the illustration_and_realistic (sample)
            "Serialized Process Tree": serialized_tree,
            "Process Tree": process_tree_json,
            "Description": process_description
        }
        samples.append(final_description)
        print(f"Process Tree: {json.dumps(serialized_tree, indent=6)}")
        #print(f"Process Description: {process_description}")
    
    with open(response_path, 'w') as f:
        json.dump(samples, f, indent=6)

    print("Process done!")
    

# Some results has hyphen in illustration_and_realistic_descriptions, remove the unnecessary punctuation
for key in illustrative_and_realistic_activities:
    illustrative_and_realistic_activities[key] = illustrative_and_realistic_activities[key].replace('-', ' ')

# Generate and describe one example process tree
#generate_description_one_example(samples_path, illustrative_and_realistic_activities, min_activities=4)

# Generate and save 9 other samples
generate_description_multi_examples(samples_path, illustrative_and_realistic_activities, min_activities=4, num_samples=2)
