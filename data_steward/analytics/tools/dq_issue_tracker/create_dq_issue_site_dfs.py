"""
File is intended to create dataframes for each of the sites to better catalog
their respective data quality issues. The output of this file should
be useful for uploading to a project management tool that could then be
provisioned to the different sites.

This project management tool could then, in turn, enable sites to more easily
identify their data quality issues and allow the DRC to more easily track
HPO engagement.

For a full description of this issue, please see EDQ-427.

Start Date: 03/24/2020 (v1)
"""

from .relevant_links import relevant_links


concept_success_link = relevant_links['concept_success']
duplicates_link = relevant_links['duplicates']
end_before_start_link = relevant_links['end_before_start']
data_after_death_link = relevant_links['data_after_death']
unit_success_link = relevant_links['unit_success']
route_success_link = relevant_links['route_success']
measurement_integration_link = relevant_links['measurement_integration']
drug_integration_link = relevant_links['drug_integration']


