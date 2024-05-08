import pm4py
from ProcessTree import CustomRandomProcessTree
import ActivityNames
import ModelDescription


if __name__ == '__main__':
    activities = ActivityNames.generate_random_activities(6)

    randomProcessTree = CustomRandomProcessTree(activities)
    process_tree = randomProcessTree.return_process_tree()

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