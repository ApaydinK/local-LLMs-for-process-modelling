from pm4py.objects.process_tree.obj import ProcessTree, Operator
import json
from ProcessTree import root_node
import pm4py

def serialize_process_tree(node):
    """ Serializes a process tree node to a JSON object. """
    node_data = {
        'type': 'leaf' if node.is_leaf() else 'operator',
        'label': node.label if node.is_leaf() else None,
        'operator': node.operator.name if not node.is_leaf() else None,
        'children': [serialize_process_tree(child) for child in node.children] if not node.is_leaf() else []
    }
    return node_data

# Assuming `root` is your root ProcessTreeOperator
#json_data = serialize_process_tree(root_node)
#json_string = json.dumps(json_data, indent=4)
#print(json_string)
#TODO
#pm4py.write_ptml(root_node, "running-example.ptml")
#tree = pm4py.read_ptml("running-example.ptml")


illustrative_and_realistic_activities = {
    'a': "Review Feedback",
    'b': "Draft Email",
    'c': "Open Ticket",
    'd': "Send Notification",
    'e': "Update Database",
    'f': "Check Inventory",
    'g': "Receive Call",
    'h': "Resolve Issue",
    'i': "Close Ticket",
    'j': "Write Summary",
    'k': "Approve Summary",
    'l': "Archive Document",
    'm': "Notify Customer",
    'n': "Consult Specialist",
    'o': "Collect Data",
    'p': "Assign Task",
    'q': "Schedule Follow-up",
    'r': "Analyze Data",
    's': "Send Confirmation",
    't': "Record Interaction",
    'u': "Update Records",
    'v': "Evaluate Solution"
}
#test
def replace_activity_labels_in_process_tree(root_node:ProcessTree, activity_mappings:dict):
    for child in root_node.children:
        if not child.children:
            child.label = activity_mappings[child.label]
        elif child.children:
            replace_activity_labels_in_process_tree(child, activity_mappings)
print(root_node)
replace_activity_labels_in_process_tree(root_node,illustrative_and_realistic_activities)
print(root_node)

"""
def deserialize_process_tree(json_data):
    # Deserializes JSON object back into a process tree node.
    if json_data['type'] == 'leaf':
        return ProcessTreeLeaf(label=json_data['label'])
    else:
        operator_map = {
            'SEQUENCE': Operator.SEQUENCE,
            'PARALLEL': Operator.PARALLEL,
            'XOR': Operator.XOR,
            'LOOP': Operator.LOOP
        }
        node = ProcessTreeOperator(operator=operator_map[json_data['operator']])
        node.children = [deserialize_process_tree(child) for child in json_data['children']]
        for child in node.children:
            child.parent = node
        return node

# Assuming `json_string` is your JSON string
loaded_json_data = json.loads(json_string)
reconstructed_tree = deserialize_process_tree(loaded_json_data)
"""
