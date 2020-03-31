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


class AggregateMetricForTable:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

        a particular data quality metric on a particular date
        for a particular table
    """
    def __init__(
            self, date, table_name, metric_type,
            num_total_rows, num_pertinent_rows):
        """
        Initializes the attributes of the class.

        Parameters
        ----------
        date (datetime): 'date' that the object represents (in
            other words, the corresponding analytics
            report from which it hails)

        table_name (string): name of the table whose data quality
            metric is being determined (e.g. Measurement)

        metric_type (string): name of the metric that is being
            determined (e.g. duplicates)

        num_total_rows (float): number of rows for the table
            across all of the HPOs for the particular date

        num_pertinent_rows (float): number of rows for the
            table that ultimately contribute to either the
            'success' or 'failure' rate for all of the HPOs
            for the particular date
        """
        self.date = date
        self.table_name = table_name
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows
        self.overall_rate = round(
            num_pertinent_rows/num_total_rows * 100,
            2)


class AggregateMetricForHPO:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

       a particular data quality metric on a particular date
       for a particular HPO (across all tables)
    """
    def __init__(
            self, date, hpo_name, metric_type,
            num_total_rows, num_pertinent_rows):
        """
        Initializes the attributes of the class.

        Parameters
        ----------
        date (datetime): 'date' that the object represents (in
            other words, the corresponding analytics
            report from which it hails)

        hpo_name (string): name of the HPO whose data quality
            metric is being determined (e.g. nyc_cu)

        metric_type (string): name of the metric that is being
            determined (e.g. duplicates)

        num_total_rows (float): number of rows for the table
            across all of the HPOs for the particular date

        num_pertinent_rows (float): number of rows for the
            table that ultimately contribute to either the
            'success' or 'failure' rate for all of the HPOs
            for the particular date

        overall_rate (float): shows the overall 'success'
            or failure rate based on the aforementioned
            parameters

        full_hpo_name (string): full 'human readable' name of
            the HPO in question
        """
        self.date = date
        self.hpo_name = hpo_name
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows
        self.overall_rate = round(
            num_pertinent_rows/num_total_rows * 100,
            2)
        self.full_hpo_name = full_names[hpo_name]


class AggregateMetricForDate:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

       a particular data quality metric on a particular date
       (across all tables and all HPOs).

       example: number of duplicates for an entire date, across
       all tables
    """
    def __init__(
            self, date, metric_type,
            num_total_rows, num_pertinent_rows):
        """
        Initializes the attributes of the class.

        Parameters
        ----------
        date (datetime): 'date' that the object represents (in
            other words, the corresponding analytics
            report from which it hails)

        metric_type (string): name of the metric that is being
            determined (e.g. duplicates)

        num_total_rows (float): number of rows for the table
            across all of the HPOs for the particular date

        num_pertinent_rows (float): number of rows for the
            table that ultimately contribute to either the
            'success' or 'failure' rate for all of the HPOs
            for the particular date

        overall_rate (float): shows the overall 'success'
            or failure rate based on the aforementioned
            parameters
        """
        self.date = date
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows
        self.overall_rate = round(
            num_pertinent_rows/num_total_rows * 100,
            2)
