import json

import pm4py
from ProcessTree import CustomRandomProcessTree
import ActivityNames
import ModelDescription
import ProcessTree

def generate_and_view_one_example():
    activities = ActivityNames.generate_random_activities(6)

    random_process_tree = CustomRandomProcessTree(activities)
    process_tree = random_process_tree.return_process_tree()

    pm4py.view_process_tree(process_tree)
    print(process_tree)

    bpmn_graph = pm4py.convert_to_bpmn(process_tree)
    pm4py.view_bpmn(bpmn_graph)

    net, im, fm = pm4py.convert_to_petri_net(process_tree)
    pm4py.view_petri_net(net, im, fm)

    # image_file_path = f"render/{name}.png"
    # pm4py.vis.save_vis_petri_net(net, im, fm, image_file_path)

    abstraction = ModelDescription.pm4py_abstraction_of_petri_net(net, im, fm)
    print(abstraction)

    ModelDescription.description_with_local_llm(process_tree)


def generate_and_store_examples(number_of_examples):
    for i in range(number_of_examples):
        activities = ActivityNames.generate_random_activities(6)

        random_process_tree = CustomRandomProcessTree(activities)
        process_tree = random_process_tree.return_process_tree()

        # store visualization of the process graph
        process_tree_image_file_path = f"../generated_models_and_descriptions/{i}_process_tree.png"
        pm4py.vis.save_vis_process_tree(process_tree, process_tree_image_file_path)
        print(process_tree)

        # convert process tree to a BPMN graph and store the visualization
        bpmn_graph = pm4py.convert_to_bpmn(process_tree)
        bpmn_image_file_path = f"../generated_models_and_descriptions/{i}_bpmn.png"
        pm4py.vis.save_vis_bpmn(bpmn_graph, bpmn_image_file_path)

        # convert process tree to a petri net and store the visualization
        net, im, fm = pm4py.convert_to_petri_net(process_tree)
        petri_net_image_file_path = f"../generated_models_and_descriptions/{i}_petri_net.png"
        pm4py.vis.save_vis_petri_net(net, im, fm, petri_net_image_file_path)

        """
        abstraction = ModelDescription.pm4py_abstraction_of_petri_net(net, im, fm)
        description_of_petri_net_text_file = open(f"../generated_models_and_descriptions/{i}_petri_net_description.txt", "x")
        description_of_petri_net_text_file.write(abstraction)
        description_of_petri_net_text_file.close()
        """

        description_of_process_tree_path = f"../generated_models_and_descriptions/{i}_process_tree_description.txt"
        ModelDescription.describe_with_local_llm_and_store_description(process_tree, description_of_process_tree_path)

def generate_and_store_pm4py_process_trees(number_of_examples):
    for i in range(number_of_examples):
        process_tree = ProcessTree.pm4py_process_tree_generator()

        # store visualization of the process graph
        process_tree_image_file_path = f"../pm4py_generated_models_and_descriptions/{i}_process_tree.png"
        pm4py.vis.save_vis_process_tree(process_tree, process_tree_image_file_path)
        print(process_tree)

        # convert process tree to a BPMN graph and store the visualization
        bpmn_graph = pm4py.convert_to_bpmn(process_tree)
        bpmn_image_file_path = f"../pm4py_generated_models_and_descriptions/{i}_bpmn.png"
        pm4py.vis.save_vis_bpmn(bpmn_graph, bpmn_image_file_path)

        # convert process tree to a petri net and store the visualization
        net, im, fm = pm4py.convert_to_petri_net(process_tree)
        petri_net_image_file_path = f"../pm4py_generated_models_and_descriptions/{i}_petri_net.png"
        pm4py.vis.save_vis_petri_net(net, im, fm, petri_net_image_file_path)

        """
        abstraction = ModelDescription.pm4py_abstraction_of_petri_net(net, im, fm)
        description_of_petri_net_text_file = open(f"../pm4py_generated_models_and_descriptions/{i}_petri_net_description.txt", "x")
        description_of_petri_net_text_file.write(abstraction)
        description_of_petri_net_text_file.close()
        """

        description_of_process_tree_path = f"../pm4py_generated_models_and_descriptions/{i}_process_tree_description.txt"
        ModelDescription.describe_with_local_llm_and_store_description(process_tree, description_of_process_tree_path)



if __name__ == '__main__':
    #generate_and_view_one_example()
    #generate_and_store_examples(10)
    #generate_and_store_pm4py_process_trees(1)
    process_tree = pm4py.ProcessTree("->( 't', 's' )")
    pm4py.view_process_tree(process_tree)

    print(process_tree)
    with open("../pm4py_generated_models_and_descriptions/0_process_tree_revised_byChatGPT.txt", "r") as file:
        process_description = file.read()
    #pm4py.convert_to_process_tree(process_tree_string)
    #process_tree = pm4py.ProcessTree(
    #    "->( X( *( X( 'g', *( 'f', X( 'h', *( 't', 's' ) ) ) ), *( X( 'c', +( 'p', *( 'n', 'v' ) ) ), +( 'q', 'm' ) ) ), +( +( 'e', 'd' ), ->( ->( 'j', 'k' ), ->( 'b', 'l' ) ) ) ), *( tau, +( 'a', *( ->( 'o', 'r' ), X( 'u', 'i' ) ) ) ) )")
    #pm4py.view_process_tree(process_tree)
    print("test")

    json.JSONEncoder(process_tree)


