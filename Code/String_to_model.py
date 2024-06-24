import pm4py
import pm4py.utils as u
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer


def string_to_tree(process_string: str) -> pm4py.visualization.process_tree:
    # Transform a string into a process tree object
    tree = u.parse_process_tree(process_string)
    return tree


def llm_response_string_to_tree(llm_response_string_with_process_tree: str) -> pm4py.visualization.process_tree:
    # Transform a string into a process tree object
    process_string = None  # TODO cut llm_response_string_with_process_tree to only include process tree string
    tree = u.parse_process_tree(process_string)
    return tree


def view_tree_as_png(tree: pm4py.visualization.process_tree) -> None:
    # View tree as PNG graphic
    pm4py.view_process_tree(tree)


from FileHandling import retrieve_file_path


number_of_generated_examples = 100
def load_and_convert_all_process_trees_to_svg():
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        viz = pt_visualizer.apply(process_tree,
                                  parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
        process_tree_svg_file_path = f"../pm4py_generated_models_and_descriptions/{process_id}_process_tree.svg"
        pt_visualizer.save(viz, process_tree_svg_file_path)

def load_and_convert_all_process_trees_to_bpmn_and_then_to_svg():
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        bpmn_graph = pm4py.convert_to_bpmn(process_tree)
        viz_bpmn = bpmn_visualizer.apply(bpmn_graph, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
        bpmn_svg_file_path = f"../pm4py_generated_models_and_descriptions/{process_id}_bpmn.svg"
        pm4py.visualization.bpmn.visualizer.save(viz_bpmn, bpmn_svg_file_path)

def load_and_convert_all_process_trees_to_petri_nets_and_then_to_svg():
    for process_id in range(number_of_generated_examples):
        ptml_file_path = retrieve_file_path("ptml", process_id)
        process_tree = pm4py.read_ptml(ptml_file_path)
        net, initial_marking, final_marking = pm4py.convert_to_petri_net(process_tree)
        viz_petri_net = pm4py.visualization.petri_net.visualizer.apply(net, initial_marking, final_marking, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
        petri_net_svg_file_path = f"../pm4py_generated_models_and_descriptions/{process_id}_petri_net.svg"
        pm4py.visualization.petri_net.visualizer.save(viz_petri_net, petri_net_svg_file_path)

def view_tree_as_svg(tree: pm4py.visualization.process_tree) -> None:
    # View tree as SVG graphic
    viz = pt_visualizer.apply(tree, parameters={pt_visualizer.Variants.WO_DECORATION.value.Parameters.FORMAT: "svg"})
    pt_visualizer.view(viz)


def print_pn(tree: pm4py.visualization.process_tree) -> None:
    # Generate and print Petri Net model from a tree structure
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)
    print(net)


def tree_to_pn(tree: pm4py.visualization.process_tree) -> None:
    # Generate and view a Petri Net model from a tree structure
    net, initial_marking, final_marking = pm4py.convert_to_petri_net(tree)
    viz = pm4py.visualization.petri_net.variants.alignments.apply(net, initial_marking, final_marking)
    pm4py.visualization.dfg.visualizer.matplotlib_view(viz)


def tree_to_bpmn(tree: pm4py.visualization.process_tree) -> None:
    # Generate and view a BPMN model from a tree structure
    bpmn_graph = pm4py.convert_to_bpmn(tree)
    viz_bpmn = bpmn_visualizer.apply(bpmn_graph)
    bpmn_visualizer.view(viz_bpmn)


def string_to_bpmn(process_string: str) -> None:
    # Generate and view a BPMN model from a string
    tree = string_to_tree(process_string)
    tree_to_bpmn(tree)


def string_to_petri_net(process_string: str) -> None:
    # Generate and view a Petri Net model from a string
    tree = string_to_tree(process_string)
    view_tree_as_svg(tree)


# Tests
ps = "X( ->( 'Create Menu', +( 'Prepare Order', 'Pack Goods' ) ), X( 'Process Payment', +( 'Verify Card', 'Authorize Transaction' ) ) )"

# t1 = string_to_tree(ps)
# view_tree_as_png(t1)
# view_tree_as_svg(t1)
# tree_to_pn(t1)
# print_pn(t1)
# tree_to_bpmn(t1)
# string_to_petri_net(ps)
#string_to_bpmn(ps)
#load_and_convert_all_process_trees_to_svg()
#load_and_convert_all_process_trees_to_bpmn_and_then_to_svg()
#load_and_convert_all_process_trees_to_petri_nets_and_then_to_svg()