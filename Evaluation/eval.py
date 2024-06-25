from Levenshtein import distance
import matplotlib.pyplot as plt


original_trees = [
"*( ->( 'Extract Reports', +( 'Check Invoices', 'Process Payments' ) ), X( 'Analyze Financials', 'Generate Balance Sheets' ) )",
"X( X( ->( 'Approve Loan Application', 'Verify Credit History' ), X( 'Send Notification Email', 'Get Customer Information' ) ), 'Initiate Loan Application' )",
"*( *( 'Review Proposal', X( 'Evaluate Application', +( 'Shortlist Candidates', 'Conduct Interview' ) ) ), ->( *( 'Create Report', 'Offer Job' ), *( 'Conduct Interview Panel', 'Hire Employee' ) ) )",
"*( 'Package Materials', X( +( 'Process Order', X( 'Source Fresh Fruit', 'Pack Eggs' ) ), *( 'Extract Data', *( 'Verify Account', ->( 'Validate Health Records', 'Approve Grant Application' ) ) ) ) )"
]

predicted_trees = [
"*( ->( 'Extract Reports', +( 'Check Invoices', 'Process Payments' ) ), X( 'Analyze Financials', 'Generate Balance Sheets' ) )",
"X( X( ->( 'Approve Loan Application', 'Verify Credit History' ), X( 'Send Notification Email', 'Get Customer Information' ) ), 'Initiate Loan Application' )",
"*( *( 'Review Proposal', X( 'Evaluate Application', +( 'Shortlist Candidates', 'Conduct Interview' ) ) ), *( 'Create Report', *( 'Offer Job', 'Conduct Interview Panel' ) ) )",
"*( 'Package Materials', X( +( 'Process Order', X( 'Source Fresh Fruit', 'Pack Eggs' ) ), *( 'Extract Data', *( 'Verify Account', ->( 'Validate Health Records', 'Approve Grant Application' ) ) ) ) )"
]


original_trees_validation_set = [
"+( ->( 'Prepare Proposal', 'Hire Candidate' ), X( 'Conduct Interviews', *( 'Review Budget', X( 'Evaluate Options', +( 'Finalize Features', X( 'Develop Design', 'Generate Requirements' ) ) ) ) ) )",
"*( *( 'analyze_samples', *( 'extract_features', 'store_results' ) ), *( ->( 'prepare_data', 'run_analysis' ), *( 'interpret_results', 'present_findings' ) ) )",
"+( 'analyze', ->( +( 'thankYouNote', 'positiveFeedback' ), +( 'escalateToSupport', 'negativeFeedback' ) ) )",
"*( 'generate_code', ->( *( 'write_unit_test', +( 'integrate_module', X( 'add_features', 'test_case' ) ) ), ->( 'release_update', 'design_pattern' ) ) )",
"->( X( 'Receive_Order', +( 'Fill_Consolidation_Orders', 'Place_Order_for_Supply_Chains' ) ), ->( 'Confirm_Product_Return', 'Process_Returned_Items' ) )",
"->( X( *( 'Create', 'Test' ), +( 'Submit', 'Prepare' ) ), ->( 'Develop', ->( 'Conduct', 'Report' ) ) )",
"*( 'Review Meeting', X( +( ->( 'Prepare Presentation', 'Obtain Stakeholder Feedback' ), 'Write Report' ), +( 'Assign Task', *( 'Conduct Research Study', 'Analyze Data' ) ) ) )",
"*( 'Book Review', ->( *( 'Check Syntax', *( 'Design Pattern', 'Graph' ) ), ->( 'Analyze Code', ->( 'Test Functionality', 'Debug Issue' ) ) ) )",
"*( X( 'prepare order', 'order receipt' ), ->( 'processing start', ->( 'data collection', 'report generation' ) ) )",
"*( +( 'Create_Presentation', 'Prepare_Report_for_Client' ), X( ->( 'Provide_Feedback_to_Collaborator', 'Review_and_Approve_Document' ), ->( 'Send_Follow_Up_Email_to_Customer', X( 'Follow_up_on_Open_Tickets', 'Schedule_Meeting_with_Stakeholder' ) ) ) )",
"X( *( 'Gather Requirements', 'Approve Request' ), +( X( 'Create Document', X( 'Edit Report', 'Submit Proposal' ) ), X( 'Review Draft', X( 'Hire Consultant', X( 'Finalize Contract', 'Interview Candidate' ) ) ) ) )",
"+( 'publish', +( 'write book', X( +( 'edit chapter', 'design chapter' ), ->( 'publish book', *( 'design header', *( 'format headline', 'headline design' ) ) ) ) ) )",
"->( X( 'Computer', 'Order Parts' ), X( 'Design Product', +( ->( 'Assemble Final Product', 'Box' ), 'Test Prototype' ) ) )",
"*( 'Order Parts', +( *( 'Assemble Frame', 'Attach Handles' ), +( +( 'Connect Brackets', +( 'Pack Final Product', 'Install Wheels' ) ), 'Unpack Components' ) ) )",
"X( 'analyze data', *( X( 'develop algorithm', *( 'design model', *( 'generate report', 'execute script' ) ) ), X( 'test software', 'validate results' ) ) )",
"*( X( 'Create_Report', ->( 'Review_Document', ->( 'Prepare_Proposal', X( 'Analyze_Findings', 'Gather_Data' ) ) ) ), +( 'Schedule_Meeting', +( 'Hold_Video_Call', X( 'Brainstorm_Ideas', 'Invite_Collaborators' ) ) ) )",
"->( X( 'Order Product', ->( X( 'Review Invoice', 'Create Purchase Order' ), +( 'Make Payment Package', 'Authorize Transaction' ) ) ), ->( 'Process Claim', X( 'Verify Information', 'Ship Goods' ) ) )",
"*( +( ->( 'Order Pizza', +( 'Get Ingredients', 'Fetch Food' ) ), *( 'Prepare Hamburger', 'Cook Chicken' ) ), ->( 'Book Table', +( ->( 'Deliver Dinner', 'Gather Groceries' ), 'Eat Entree' ) ) )",
"*( +( +( 'Confirm with Customer', 'Inspect Order Details' ), 'Receive Order' ), +( X( 'Evaluate Order', 'Cancel' ), +( X( 'Archive Order', 'Notify Customer' ), ->( 'Send Confirmation Email', 'Update Database' ) ) ) )"
]


predicted_trees_validation_set = [
"+( *( 'Review Budget', ->( 'Prepare Proposal', 'Hire Candidate' ) ), ->( *( 'Conduct Interviews', 'Evaluate Options' ), +( 'Finalize Features', ->( 'Develop Design', 'Generate Requirements' ) ) ) )",
"+( *( 'Analyze', 'Extract' ), ->( 'Prepare', +( 'Run', 'Analyze' ) ) )",
"+( 'analyze', +( ->( 'give','send' ), X( 'negative', 'escalate' ) ) )",
"*( 'generate_code', +( 'design_pattern','release_update' ) ), ->( 'write_unit_test', *( 'add_feature', 'test_case' ), 'integrate_module' ) )",
"X( X( ->('receive order', +( 'place order for supply chains', 'fill consolidation order' ) ), ->( 'confirm product return', 'process returned items' ) ), ->( 'handle product return','verify product availability' ) )",
"X( +( 'Prepare', 'Submit' ), ->( 'Create', *( 'Test', 'Report' ) ) ), ->( 'Develop', 'Conduct' ) )",
"*( *( ->( 'Reviewing Meeting', *( 'Assign Task', *( 'Conduct Research Study', 'Analyze Data' ) ) ), X( 'Data is available', ->( 'Write Report for Boss', X( 'Prepare Presentation', 'Obtain Stakeholder Feedback' ) ) ) ), 'Follow Up with Team' )",
"*('review', ->( 'check', *( 'design','make' ) ) )",
"*( X( 'prepare an order', 'order a receipt' ), ->( 'process an order', ->( 'generate a report', 'output data' ) ) )",
"+( +( X( 'Create Presentation', 'Prepare Report for Client' ), X( +( 'Ask for Review', 'Approve Document' ), ->( 'Follow Up on Open Tickets', 'Schedule Meeting with Stakeholder' ) ) ), *( 'Handover Report to Boss', 'Handover Presentation to Boss' ) )",
"+( *( 'Gather Requirements', ->( 'Approve Requests', 'Review Draft' ) ), X( +( 'Create Document', X( 'Edit Report', 'Submit Proposal' ) ), X( 'Review Draft', X( 'Hire Consultant', X( 'Finalize Contract', 'Interview Candidate' ) ) ) ) )",
"+( 'Publish', +( +( 'Set Goal', 'End' ), X( +( 'Write Book', +( 'Design Chapter', 'Edit Chapter' ) ), *( 'Publish Book', *( 'Design Header', 'Format Headline' ) ) ) ) )",
"+( X( 'Order Parts', 'Use Computer' ), +( X( 'Design Product', +( 'Assemble Final Product', 'Test Prototype' ) ), 'Put in Box' ) )",
"*( ->( 'Order Parts', +( 'Unpack Components', +( *( 'Assemble Frame', 'Attach Handles' ), X( 'Connect Brackets', 'Install Wheels' ) ) ) ), ->( 'Pack Final Product', 'Install Wheels' ) )",
"X( 'Analyze Data', *( *( 'Design Model', 'Develop Algorithm' ), +( 'Generate Report', 'Execute Script' ) ) )",
"*( X( 'Create Report', ->( 'Review Document', *( 'Prepare Research Proposal', X( 'Finalize Proposal', *( 'Analyze Findings', 'Gather Data' ) ) ) ) ), +( 'Schedule Meeting with Professor', ->( 'Hold Video Call with Project Partner', X( 'Conduct Brainstorming Session', 'Invite More Collaborators with Expertise' ) ) ) )",
"X( X( 'order product', X('review invoice', 'create purchase order' ) ), ->( X( 'authorize transaction','make payment package' ), +( 'process claim', X('ship goods','verify all information is accurate and complete' ) ) ) )",
"+( *( 'Order Pizza', +( 'Get Ingredients', 'Fetch Food' ) ), X( +( 'Book Table', +( 'Eat Entree', *( 'Deliver Dinner', 'Gather Groceries' ) ) ), *( 'Prepare Hamburger', 'Cook Chicken' ) ) )",
"*( *( 'Receive Order', +( 'Confirm with Customer', 'Inspect Order Details' ) ), X( 'Cancel', 'Evaluate Order' ) ), ->( +( 'Notify Customer', 'Archive Order' ), ->( 'Send Confirmation Email', 'Update Database' ) ) )"
]

# levenshtein_results = {}
# for i in range(len(original_trees)):
#     # print(distance(original_trees[i].replace(" ", ""), predicted_trees[i].replace(" ", "")))
#     levenshtein_results[i] = distance(original_trees[i].replace(" ", ""), predicted_trees[i].replace(" ", ""))
# # print(levenshtein_results)


levenshtein_results = {}
for i in range(len(original_trees_validation_set)):
    levenshtein_results[i] = distance(original_trees_validation_set[i].replace(" ", ""), predicted_trees_validation_set[i].replace(" ", ""))


# Extracting keys and values from the dictionary
keys = list(levenshtein_results.keys())
values = list(levenshtein_results.values())

# Creating the line graph
# plt.plot(keys, values, marker='o')
plt.bar(keys, values)

# Adding titles and labels
plt.xlabel('Keys')
plt.ylabel('Values')
plt.title('Line Graph from Dictionary')

# Display the plot
plt.show()
