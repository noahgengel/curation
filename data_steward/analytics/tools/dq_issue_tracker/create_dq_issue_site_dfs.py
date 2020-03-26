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

from dictionaries_and_lists import relevant_links, full_names, \
    desired_columns_dict, data_quality_dimension_dict, table_based_on_column_provided, \
    metric_names

from class_definitions import HPO, DataQualityMetric

from general_functions import load_files, \
    generate_hpo_id_col, find_hpo_row, get_err_rate


excel_file_name = 'march_19_2020.xlsx'

# these are the links we will ultimately use to populate the df
concept_success_link = relevant_links['concept_success']
duplicates_link = relevant_links['duplicates']
end_before_start_link = relevant_links['end_before_start']
data_after_death_link = relevant_links['data_after_death']
unit_success_link = relevant_links['unit_success']
route_success_link = relevant_links['route_success']
measurement_integration_link = relevant_links['measurement_integration']
drug_integration_link = relevant_links['drug_integration']

metric_names = list(metric_names.keys())  # sheets to be investigated


def create_hpo_objects(file_name):
    """
    Function is used to establish the HPO objects that will
    ultimately carry all of the data from the sheet.

    Parameters
    ----------
    file_name (str): the date of the file that is being used to generate
        the data quality issue frames

    Returns
    -------
    hpo_objects (lst): list of HPO objects (see class_definitions.py)
        that will be used and ultimately populated with the
        data quality metrics
    """
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

    return hpo_objects


def populate_hpo_objects_with_dq_metrics(
        hpo_objects, metrics, file_name):
    """
    Function is used to take the HPO objects created in a previous
    function (create_hpo_objects) and associate them with
    DataQualityMetric objects that contain the relevant pieces
    of information from the selected sheet.

    Parameters
    ----------
    hpo_objects (lst): list of HPO objects (see class_definitions.py)
        that will be used and ultimately populated with the
        data quality metrics

    metric_names (lst): list of the sheets that will be used to
        identify the data quality metrics for each of the HPO
        and DataQualityMetric objects

    file_name (str): the date of the file that is being used to generate
        the data quality issue frames

    Returns
    -------
    hpo_objects (lst): list of HPO objects (see class_definitions.py)
        that now have the appropriate DataQualityMetric objects
    """

    # start with analyzing each metric first - minimizes 'loads'
    for metric in metrics:
        sheet = load_files(sheet_name=metric, file_name=file_name)

        for hpo in hpo_objects:
            hpo_name = hpo.name
            row_num = find_hpo_row(sheet, hpo_name)

            # what we are looking for within each analytics sheet
            desired_columns = desired_columns_dict[metric]

            all_dqds_for_hpo_for_metric = []  # list of objects - to be filled

            for column_for_table in desired_columns:
                err_rate = get_err_rate(sheet, row_num, metric, hpo_name, column_for_table)

                data_quality_dimension = DataQualityMetric(
                    hpo=hpo_name, table=table_based_on_column_provided[column_for_table],
                    metric_type=metric, value=err_rate,
                    data_quality_dimension=data_quality_dimension_dict[metric])

                # adding to a list of the same metric type for the same site
                all_dqds_for_hpo_for_metric.append(data_quality_dimension)

            # now we have objects for all of the data quality metrics for
                # a. each site
                # b. each table
            # for a particular data quality metric - should now assign to HPO

            for metric_object in all_dqds_for_hpo_for_metric:
                hpo.add_attribute_with_string(
                    metric=metric_object.metric_type, dq_object=metric_object)

    return hpo_objects

# FIXME: first_reported needs to exist


def main():
    """
    Function that executes the entirety of the program. 
    """
    hpo_objects = create_hpo_objects(file_name=excel_file_name)

    hpo_objects = populate_hpo_objects_with_dq_metrics(
        hpo_objects=hpo_objects, metrics=metric_names,
        file_name=excel_file_name)

    for hpo in hpo_objects:
        if hpo.name == 'nyc_cu':
            failing_metrics = hpo.find_failing_metrics()

    print("There are {} issues with Columbia".format(len(failing_metrics)))

    for metric in failing_metrics:
        if isinstance(metric, DataQualityMetric):
            metric.print_dqd_attributes()
            print("\n\n")


if __name__ == "__main__":
    main()