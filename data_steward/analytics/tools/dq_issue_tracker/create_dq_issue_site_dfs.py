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

from relevant_dictionaries import relevant_links, full_names
from hpo_class_definition import HPO
from functions_from_metrics_over_time import load_files, \
    generate_hpo_id_col, find_hpo_row


file_name = 'march_19_2020.xlsx'

metric_names = [
    'measurement_units',
    'drug_routes',

    # integration metrics
    'drug_success',
    'sites_measurement',

    # ACHILLES errors
    'end_before_begin',
    'data_after_death',

    # other metrics
    'concept',
    'duplicates']

concept_success_link = relevant_links['concept_success']
duplicates_link = relevant_links['duplicates']
end_before_start_link = relevant_links['end_before_start']
data_after_death_link = relevant_links['data_after_death']
unit_success_link = relevant_links['unit_success']
route_success_link = relevant_links['route_success']
measurement_integration_link = relevant_links['measurement_integration']
drug_integration_link = relevant_links['drug_integration']


def create_hpo_objects():
    # creating the various HPO objects
    hpo_id_column = generate_hpo_id_col(file_name)
    hpo_objects = []

    for hpo_id in hpo_id_column:
        hpo = HPO(name=hpo_id, full_name=full_names[hpo_id])
        hpo_objects.append(hpo)

    for metric in metric_names:
        sheet = load_files(
            sheet_name=metric, file_name=file_name)

        for hpo in hpo_objects:
            hpo_row = find_hpo_row(sheet, hpo.name)


def main():
    create_hpo_objects()

if __name__ == "__main__":
    main()
