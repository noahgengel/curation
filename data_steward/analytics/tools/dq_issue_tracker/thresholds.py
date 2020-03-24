"""
File is meant to contain the 'thresholds' that are going to be used to
determine whether or not a particular metric should be logged as a
'data quality issue' in the create_dq_issue_site_dfs script.

These thresholds are meant to be versatile and can be changed accordingly.
"""

concept_success_min = 90
duplicates_max = 5

end_before_begin_max = 0
data_after_death_max = 0

drug_ingredient_integration_min = 90
measurement_integration_min = 90

unit_success_min = 85
route_success_min = 85
