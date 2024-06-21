from Levenshtein import distance
from Code import String_to_model as s
from pm4py.objects.process_tree.utils import generic as pt_utils
import pm4py
from typing import Set


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
print("Levenshtein-distance: ", distance(s1, s2))  # string distance on both process tree strings
print("Jaccard-Set: ", jaccard_set(a1, a2))  # common elements in both sets
print("Jaccard-Index: ", jaccard_index(a1, a2))  # percentage of common elements on all elements
