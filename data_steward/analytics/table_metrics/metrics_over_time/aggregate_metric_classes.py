"""
This file is intended to establish the properties and
functions of the AggregateMetric classes. These classes should
be able to store information about

    a. a particular data quality metric on a particular date
       for a particular table (across all HPOs)

    b. a particular data quality metric on a particular date
       for a particular HPO (across all tables)
"""

from dictionaries_lists_and_prompts import full_names

class AggregateMetricAcrossHPOS:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

        a particular data quality metric on a particular date
        for a particular table
    """
    def __init__(self, date, table_name, metric_type,
        num_total_rows, num_pertinent_rows):
        """

        :param date:
        :param table_name:
        :param metric_type:
        :param num_total_rows:
        :param num_pertinent_rows:
        """
        pass


class AggregateMetricAcrossTables:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

       a particular data quality metric on a particular date
       for a particular HPO (across all tables)
    """
    def __init__(self, date, hpo_name, metric_type,
        num_total_rows, num_pertinent_rows):
        """

        :param date:
        :param hpo_name:
        :param metric_type:
        :param full_hpo_name:
        :param num_total_rows:
        :param num_pertinent_rows:
        """
        pass
        self.full_hpo_name = full_names[hpo_name]
