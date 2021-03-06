"""
This file is intended to establish the properties and
functions of the AggregateMetric classes. These classes should
be able to store information about

    a. a particular data quality metric on a particular date
       for a particular table (across all HPOs)

    b. a particular data quality metric on a particular date
       for a particular HPO (across all tables)
"""

from dictionaries_and_lists import full_names

import constants


class AggregateMetricForTableOrClass:
    """
    Class is intended to store information regarding data quality
    across what would normally be triaged across many different
    DataQualityMetric objects. This class specifically contains
    information about:

        a particular data quality metric on a particular date
        for a particular table
    """
    def __init__(
            self, date, table_or_class_name, metric_type,
            num_total_rows, num_pertinent_rows):
        """
        Initializes the attributes of the class.

        Parameters
        ----------
        date (datetime): 'date' that the object represents (in
            other words, the corresponding analytics
            report from which it hails)

        table_or_class_name (string): name of the table
            or class whose data quality metric is
            being determined (e.g. Measurement,
            ACE Inhibitor)

        metric_type (string): name of the metric that is being
            determined (e.g. duplicates)

        num_total_rows (float): number of rows for the table
            across all of the HPOs for the particular date

        num_pertinent_rows (float): number of rows for the
            table that ultimately contribute to either the
            'success' or 'failure' rate for all of the HPOs
            for the particular date

        unweighted_metric (bool): indicates whether the metric
            relates to one that is weighted by the number
            of rows contributed by each HPO
        """
        self.date = date
        self.table_or_class_name = table_or_class_name
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows

        try:
            self.overall_rate = round(
                num_pertinent_rows/num_total_rows * 100,
                constants.rounding_val)
        except ZeroDivisionError:
            self.overall_rate = 0

        if num_pertinent_rows == 0 and \
           num_total_rows == 0:
            self.unweighted_metric = constants.true
        else:
            self.unweighted_metric = constants.false

    def print_attributes(self):
        """
        Function is used to print a string that can easily
        display the components of an AggregateMetricForTable
        object.
        """
        time = self.date.strftime(constants.date_format)

        attributes_str = f"""
        Table/Class Name: {self.table_or_class_name}
        Date: {time}
        Metric Type: {self.metric_type}
        Number of Total Rows: {self.num_total_rows}
        Number of Pertinent Rows: {self.num_pertinent_rows}
        Overall Rate: {self.overall_rate}
        Unweighted Metric?: {self.unweighted_metric}
        """

        print(attributes_str)

    def manually_set_overall_rate(self, rate):
        """
        Function is used to manually set the overall rate
        for the AggregateMetricforTable. This is a function
        that is useful when the pertinent rows and total
        rows are not informative to the 'overall' rate (namely
        in instances where the aggregate metric is weighted
        equally across all of the HPOs).

        Parameters
        ----------
        rate (float): the value to set as the overall rate
            for the AggregateMetricForTable object
        """
        # round by 2 to create metric consistency
        self.overall_rate = round(rate, constants.rounding_val)


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

        unweighted_metric (bool): indicates whether the metric
            relates to one that is weighted by the number
            of rows contributed by each table
        """
        self.date = date
        self.hpo_name = hpo_name
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows
        self.full_hpo_name = full_names[hpo_name]

        try:
            self.overall_rate = round(
                num_pertinent_rows/num_total_rows * 100,
                constants.rounding_val)
        except ZeroDivisionError:
            self.overall_rate = 0

        if num_pertinent_rows == 0 and \
           num_total_rows == 0:
            self.unweighted_metric = constants.true
        else:
            self.unweighted_metric = constants.false

    def print_attributes(self):
        """
        Function is used to print a string that can easily
        display the components of an AggregateMetricForHPO
        object.
        """
        time = self.date.strftime(constants.date_format)

        attributes_str = f"""
        Date: {time}
        HPO Name: {self.hpo_name}
        Metric Type: {self.metric_type}
        Number of Total Rows: {self.num_total_rows}
        Number of Pertinent Rows: {self.num_pertinent_rows}
        Overall Rate: {self.overall_rate}
        Unweighted Metric?: {self.unweighted_metric}
        """

        print(attributes_str)

    def manually_set_overall_rate(self, rate):
        """
        Function is used to manually set the overall rate
        for the AggregateMetricForHPO. This is a function
        that is useful when the pertinent rows and total
        rows are not informative to the 'overall' rate (namely
        in instances where the aggregate metric is weighted
        equally across all of the HPOs).

        Parameters
        ----------
        rate (float): the value to set as the overall rate
            for the AggregateMetricForTable object
        """
        # round by 2 to create metric consistency
        self.overall_rate = round(rate, constants.rounding_val)


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
            num_total_rows, num_pertinent_rows,
            table_or_class):
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

        table_or_class (string): the table or class that
            the object is referrring to (e.g. 'Measurement'
            or 'ACE Inhibitors')

        unweighted_metric (bool): indicates whether the metric
            relates to one that is weighted by the number
            of rows contributed by each table and/or HPO
        """
        self.date = date
        self.metric_type = metric_type
        self.num_total_rows = num_total_rows
        self.num_pertinent_rows = num_pertinent_rows
        self.table_or_class = table_or_class

        try:
            self.overall_rate = round(
                num_pertinent_rows/num_total_rows * 100,
                constants.rounding_val)
        except ZeroDivisionError:
            self.overall_rate = 0

        if num_pertinent_rows == 0 and \
           num_total_rows == 0:
            self.unweighted_metric = constants.true
        else:
            self.unweighted_metric = constants.false

    def print_attributes(self):
        """
        Function is used to print a string that can easily
        display the components of an AggregateMetricForDate
        object.

        Return
        ------
        attributes_str (string): displays all the components
            of the AggregateMetricForDate object in an easily-
            readable fashion.
        """
        time = self.date.strftime(constants.date_format)

        attributes_str = f"""
        Date: {time}
        Metric Type: {self.metric_type}
        Number of Total Rows: {self.num_total_rows}
        Number of Pertinent Rows: {self.num_pertinent_rows}
        Overall Rate: {self.overall_rate}
        Unweighted Metric?: {self.unweighted_metric}
        """

        print(attributes_str)

    def manually_set_overall_rate(self, rate):
        """
        Function is used to manually set the overall rate
        for the AggregateMetricForDate. This is a function
        that is useful when the pertinent rows and total
        rows are not informative to the 'overall' rate (namely
        in instances where the aggregate metric is weighted
        equally across all of the HPOs).

        Parameters
        ----------
        rate (float): the value to set as the overall rate
            for the AggregateMetricForTable object
        """
        # round by 2 to create metric consistency
        self.overall_rate = round(
            rate, constants.rounding_val)
