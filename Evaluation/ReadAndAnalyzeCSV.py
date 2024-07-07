import pandas as pd

dataframe = pd.read_csv(f"../Evaluation/results.csv", delimiter=";")

dataframe_process_trees_original_structure_entire_set     = dataframe.iloc[:, 1]
dataframe_process_trees_after_fine_tuning_entire_set      = dataframe.iloc[:, 4]

dataframe_process_trees_original_structure_training_set   = dataframe.iloc[:71, 1]
dataframe_process_trees_after_fine_tuning_training_set    = dataframe.iloc[:71, 4]

dataframe_process_trees_original_structure_validation_set = dataframe.iloc[71:, 1]
dataframe_process_trees_after_fine_tuning_validation_set  = dataframe.iloc[71:, 4]

process_trees_original_structure_training_set             = list(dataframe_process_trees_original_structure_training_set)
dataframe_process_trees_after_fine_tuning_training_set    = list(dataframe_process_trees_after_fine_tuning_training_set)

dataframe_process_trees_original_structure_entire_set     = list(dataframe_process_trees_original_structure_entire_set)
dataframe_process_trees_after_fine_tuning_entire_set      = list(dataframe_process_trees_after_fine_tuning_entire_set)

process_trees_original_structure_validation_set           = list(dataframe_process_trees_original_structure_validation_set)
dataframe_process_trees_after_fine_tuning_validation_set  = list(dataframe_process_trees_after_fine_tuning_validation_set)
#for row1, row2 in column_b_column_e:
#    levensteihn(row, row2)
#
## Display the extracted column
#
#column = dataframe.columns[4]
#column
print("lets go")