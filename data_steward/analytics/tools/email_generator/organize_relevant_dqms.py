"""
This file contains functions that can be used to determine the
DataQualityMetric (and
"""

from contact_list import recipient_dict


def get_hpo_site():
    """
    Function is used to get the HPO ID of the site whose e-mail will
    be generated

    Returns
    -------
    hpo_id (str): string that represents the HPO ID whose email
        is to be generated
    """
    prompt = "Please input the site ID of the HPO site that " \
             "you would like to use for an auto-generated e-mail. " \
             "(e.g. nyc_hh)\n"

    hpo_id = input(prompt)
    hpo_id = hpo_id.lower()  # case sensitivity

    while hpo_id not in recipient_dict:
        print("HPO ID not found in the 'contact list' file.")
        hpo_id = input(prompt)

    return hpo_id


def organize_relevant_dqms(hpo_objects):
    """
    Function is used to organize the data quality
    metrics for the specified HPO ID

    Parameters
    ----------
    hpo_objects (list): contains all of the HPO objects. the
        DataQualityMetric objects will now be associated to
        the HPO objects appropriately.

    Returns
    -------
    unique_metrics (dict): has the following structure:
        keys: the 'metric type' (e.g. duplicates)
        values: the tables that were deemed to have 'failed'
    """
    hpo_id = get_hpo_site()
    failing_metrics, unique_metrics = [], {}

    for hpo in hpo_objects:
        if hpo.name == hpo_id:

            try:
                failing_metrics.extend(hpo.find_failing_metrics())
            except TypeError:
                pass  # nothing found

    # now we have all the failing metrics for the HPO

    for failing_metric in failing_metrics:

        if failing_metric.metric_type not in unique_metrics.keys():
            unique_metrics[failing_metric.metric_type] = \
                [failing_metric.table_or_class]

        else:
            unique_metrics[failing_metric.metric_type].append(
                failing_metric.table_or_class)

    return unique_metrics


def create_string_for_failing_metrics(hpo_objects):
    """
    Function is used to create a string for the failing
    metrics that can ultimately be inserted into the email output.


    Parameters
    ----------
    hpo_objects (list): contains all of the HPO objects. the
        DataQualityMetric objects will now be associated to
        the HPO objects appropriately.

    Returns
    -------
    """

    unique_metrics = organize_relevant_dqms(hpo_objects)

    issue_num = 1

    issue_report = ""

    for metric_type, tables_or_classes in unique_metrics.items():

        tables_affected = ', '.join(tables_or_classes)

        issue_report += f"{issue_num}. {metric_type} " \
              f"has failed in at least the following tables or classes: \n\t" \
              f"{tables_affected}\n\n"

        issue_num += 1

    return issue_report
