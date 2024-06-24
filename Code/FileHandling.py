import os
folder = "pm4py_generated_models_and_descriptions"
current_path = os.path.dirname(os.path.abspath(__file__))
folder_path = os.path.join(os.path.dirname(current_path), folder)


def retrieve_file_path(kind, process_id):
    match kind:
        case "process_tree":
            return f"{folder_path}/{process_id}_process_tree.png"
        case "process_tree.svg":
            return f"{folder_path}/{process_id}_process_tree.svg"
        case "bpmn":
            return f"{folder_path}/{process_id}_bpmn.png"
        case "bpmn.svg":
            return f"{folder_path}/{process_id}_bpmn.svg"
        case "petri_net":
            return f"{folder_path}/{process_id}_petri_net.png"
        case "petri_net.svg":
            return f"{folder_path}/{process_id}_petri_net.svg"
        case "process_tree_description":
            return f"{folder_path}/{process_id}_process_tree_description.txt"
        case "petri_net_description":
            return f"{folder_path}/{process_id}_petri_net_description.txt"
        case "ptml":
            return f"{folder_path}/{process_id}_process_tree.ptml"
        case "process_tree_description_based_on_few_shot_prompting":
            return f"{folder_path}/{process_id}_process_tree_description_based_on_few_shot_prompting.txt"
        case _:
            return "error"

def update_dotenv(key, new_value):

    with open('.env', 'r') as file:
        lines = [line.strip() for line in file]

    # Check if the key already exists in the file
    key_exists = False
    with open('.env', 'w') as file:
        for line in lines:
            if line.startswith(f"{key}="):
                file.write(f"{key}={new_value}\n")
                key_exists = True
            else:
                file.write(line + '\n')

        # If the key does not exist in the file, add it
        if not key_exists:
            file.write(f"{key}={new_value}\n")