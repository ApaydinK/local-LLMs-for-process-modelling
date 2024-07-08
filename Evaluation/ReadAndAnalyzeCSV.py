import pandas as pd
from Levenshtein import distance
import matplotlib.pyplot as plt
import pm4py
import pm4py.utils as u
from pm4py.visualization.process_tree import visualizer as pt_visualizer
from pm4py.visualization.bpmn import visualizer as bpmn_visualizer
from Levenshtein import distance
# from Code import String_to_model as s
from pm4py.objects.process_tree.utils import generic as pt_utils
import pm4py
from typing import Set


def string_to_tree(process_string: str) -> pm4py.visualization.process_tree:
    # Transform a string into a process tree object
    tree = u.parse_process_tree(process_string)
    return tree


def extract_activities(tree: pm4py.visualization.process_tree) -> Set[str]:
    # Extract activities using the built-in function
    activities = pt_utils.get_leaves(tree)

    # Extract the labels from the leaves
    activity_labels = [activity.label for activity in activities if activity.label is not None]

    # Sort the list alphabetically and then turn the list into a set for set operations
    activity_labels.sort()
    activity_labels = set(activity_labels)
    return activity_labels


def jaccard_index(set1: Set[str], set2: Set[str]) -> float:
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union


# Reading file into a pandas dataframe
dataframe = pd.read_csv(f"../Evaluation/results.csv", delimiter=";")

# Original training, validation, and full set
dataframe_process_trees_original_structure_training_set = dataframe.iloc[:71, 1]
dataframe_process_trees_original_structure_validation_set = dataframe.iloc[71:, 1]
dataframe_process_trees_original_structure_entire_set = dataframe.iloc[:, 1]

# Predicted training, validation, and full set
dataframe_process_trees_after_fine_tuning_training_set = dataframe.iloc[:71, 4]
dataframe_process_trees_after_fine_tuning_validation_set = dataframe.iloc[71:, 4]
dataframe_process_trees_after_fine_tuning_entire_set = dataframe.iloc[:, 4]

# Converting pandas columns into strings
process_trees_original_structure_training_set = list(dataframe_process_trees_original_structure_training_set)
dataframe_process_trees_after_fine_tuning_training_set = list(dataframe_process_trees_after_fine_tuning_training_set)
dataframe_process_trees_original_structure_entire_set = list(dataframe_process_trees_original_structure_entire_set)
dataframe_process_trees_after_fine_tuning_entire_set = list(dataframe_process_trees_after_fine_tuning_entire_set)
process_trees_original_structure_validation_set = list(dataframe_process_trees_original_structure_validation_set)
dataframe_process_trees_after_fine_tuning_validation_set = list(dataframe_process_trees_after_fine_tuning_validation_set)


results = {}
for i in range(len(dataframe_process_trees_original_structure_entire_set)):
    # Levenshtein
    # results[i] = distance(dataframe_process_trees_original_structure_entire_set[i].replace(" ", ""), dataframe_process_trees_after_fine_tuning_entire_set[i].replace(" ", ""))

    # Jaccard
    t1 = string_to_tree(dataframe_process_trees_original_structure_entire_set[i])
    a1 = extract_activities(t1)
    t2 = string_to_tree(dataframe_process_trees_after_fine_tuning_entire_set[i])
    a2 = extract_activities(t2)
    results[i] = jaccard_index(a1, a2)

# Extracting keys and values from the dictionary
keys = list(results.keys())
values = list(results.values())

# Creating the line graph
# plt.plot(keys, values, marker='o')
plt.bar(keys, values)

# Adding titles and labels
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title('Jaccard-Index on Full Set')

# Display the plot
plt.show()
