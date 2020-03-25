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

from relevant_dictionaries import relevant_links, full_names, \
    desired_columns_dict, data_quality_dimension_dict, table_based_on_column_provided

from hpo_class_definition import HPO, DataQualityMetric

from functions_from_metrics_over_time import load_files, \
    generate_hpo_id_col, find_hpo_row, get_err_rate


file_name = 'march_19_2020.xlsx'

metric_names = [
    'measurement_units', 'drug_routes',

    # integration metrics
    'drug_success','sites_measurement',

    # ACHILLES errors
    'end_before_begin','data_after_death',

    # other metrics
    'concept', 'duplicates']

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
        hpo = HPO(
            name=hpo_id, full_name=full_names[hpo_id],
            concept_success=[], duplicates=[],
            end_before_begin=[], data_after_death=[],
            route_success=[], unit_success=[], measurement_integration=[],
            ingredient_integration=[])

        hpo_objects.append(hpo)

    # now we need to create the DataQualityMetric objects
    for metric in metric_names:
        sheet = load_files(
            sheet_name=metric, file_name=file_name)

        for hpo in hpo_objects:
            hpo_name = hpo.name
            row_num = find_hpo_row(sheet, hpo_name)

            desired_columns = desired_columns_dict[metric]

            all_dqds_for_hpo_for_metric = []  # list of objects - to be filled
            # FIXME: first_reported needs to exist

            for column_for_table in desired_columns:
                err_rate = get_err_rate(sheet, row_num, metric, hpo_name, column_for_table)

                data_quality_dimension = DataQualityMetric(
                    hpo=hpo_name, table=table_based_on_column_provided[column_for_table],
                    metric_type=metric, value=err_rate,
                    data_quality_dimension=data_quality_dimension_dict[metric])

                all_dqds_for_hpo_for_metric.append(data_quality_dimension)

            # now we have objects for all of the data quality metrics for
                # a. each site
                # b. each table
            # for a particular data quality metric - should now assign to HPO

            for metric_object in all_dqds_for_hpo_for_metric:

                hpo.set_attribute_with_string(
                    metric=metric_object.metric_type, dq_object=metric_object)


def main():
    create_hpo_objects()

if __name__ == "__main__":
    main()
