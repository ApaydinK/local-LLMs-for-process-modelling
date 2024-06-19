import pm4py
import pm4py.utils as u
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer


def string_to_tree(process_string: str) -> pm4py.visualization.process_tree:
    # Transform a string into a process tree object
    tree = u.parse_process_tree(process_string)
    return tree


def view_tree_as_png(tree: pm4py.visualization.process_tree) -> None:
    # View tree as PNG graphic
    pm4py.view_process_tree(tree)


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
string_to_bpmn(ps)
