"""
These series of functions are used in the creation of
AggregateMetric objects. These are similar to the regular
DataQualityMetric objects except they contain additional
information to better convey the scale in terms of the
number of rows available across all of the different
sites.

Please see the AggregateMetric class documentation for
further information.
"""

from aggregate_metric_class import AggregateMetricAcrossHPOS, \
    AggregateMetricAcrossTables


def create_aggregate_dqms_for_metric(
        metric_dictionary, user_choice):
    """
    Function is intended to create 'aggregate' data quality
    metrics that can be applied to a specific data quality metric
    for a particular date (across all HPOs). This
    AggregateMetric object will contain information across
    all of the different sites.

    Parameters
    ----------
    metric_dictionary (dict): has the following structure
        keys: all of the different metric_types possible
        values: all of the HPO objects that
            have that associated metric_type

    user_choice (string): represents the sheet from the analysis reports
        whose metrics will be compared over time

    Returns
    -------
    aggregate_dqm (DataQualityMetric): DataQualityMetric object
        that is weighted across all of the provided HPO objects
        for that particular date
    """

    # first we shall find the applicable tables - each should
    # get a separate metric

    pass
