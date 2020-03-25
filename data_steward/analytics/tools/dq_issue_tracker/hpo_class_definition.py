"""
File is intended to establish a 'HPO class' that can be used
to store data quality metrics for each HPO in an easy and
identifiable fashion.

Class was used as a means for storing information as the ability
to add functions could prove useful in future iterations of the
script.
"""

from relevant_dictionaries import thresholds
from datetime import date
import sys


class HPO:
    """
    Class is used to associated data quality issues with a particular
    HPO.
    """

    def __init__(
            self, name, full_name, concept_success, duplicates,
            end_before_begin, data_after_death,
            route_success, unit_success, measurement_integration,
            ingredient_integration):

        """
        Used to establish the attributes of the object being instantiated.

        Parameters
        ----------
        self (HPO object): the object to be created

        name (str): name of the HPO ID to create (e.g. nyc_cu)

        full_name (str): full name of the HPO

        all other optional parameters are intended to be float objects. they
        each represent a data quality metric that can be found on the AoU
        HPO site at the following link:
        https://sites.google.com/view/ehrupload

        they were all set to 0 because this would be the value all of the data
        quality metrics would receive if the site were to have no data
        """

        self.name = name
        self.full_name = full_name

        # relates to multiple tables - therefore should be list of objects
        self.concept_success = concept_success
        self.duplicates = duplicates
        self.end_before_begin = end_before_begin
        self.data_after_death = data_after_death

        # only relates to one table - therefore single float expected
        self.route_success = route_success
        self.unit_success = unit_success
        self.measurement_integration = measurement_integration
        self.ingredient_integration = ingredient_integration

    def set_attribute_with_string(self, metric, dq_object):
        """

        :param string:
        :param dq_object:
        :return:
        """

        if metric == 'concept':
            self.concept_success.append(dq_object)

        elif metric == 'duplicates':
            self.duplicates.append(dq_object)

        elif metric == 'end_before_begin':
            self.end_before_begin.append(dq_object)

        elif metric == 'data_after_death':
            self.data_after_death.append(dq_object)

        elif metric == 'sites_measurement':
            self.measurement_integration.append(dq_object)

        elif metric == 'drug_success':
            self.ingredient_integration.append(dq_object)

        elif metric == 'drug_routes':
            self.route_success.append(dq_object)

        elif metric == 'measurement_units':
            self.unit_success.append(dq_object)

        else:
            print("Unrecognized metric input: {metric} for {hpo}".format(
                metric=metric, hpo=self.name))
            sys.exit(0)

    def find_failing_metrics(self):
        """
        Function is used to create a catalogue of the 'failing' data
        quality metrics at defined by the thresholds established by
        the appropriate dictionary from relevant_dictionaries.

        Parameters
        ----------
        self (HPO object): the object whose 'failing metrics' are to
            be determined

        :return:
        failing_metrics (list): has a list of the data quality metrics
            for the HPO that have 'failed' based on the thresholds
            provided

        NOTE:
        if no data quality problems are found, however, the function
        will return 'None' to signify that no issues arose
        """

        failing_metrics = []

        # below we can find the data quality metrics for several tables -
        # need to iterate through a list to get the objects for each table
        for concept_success_obj in self.concept_success:
            if concept_success_obj.value < thresholds['concept_success_min']:
                failing_metrics.append(concept_success_obj)

        for duplicates_obj in self.duplicates:
            if duplicates_obj.value > thresholds['duplicates_max']:
                failing_metrics.append(duplicates_obj)

        for end_before_begin_obj in self.end_before_begin:
            if end_before_begin_obj.value > thresholds['end_before_begin_max']:
                failing_metrics.append(end_before_begin_obj)

        for data_after_death_obj in self.data_after_death:
            if data_after_death_obj.value > thresholds['data_after_death_max']:
                failing_metrics.append(data_after_death_obj)

        # the following attributes should only be one object - no need to
        # iterate through a list
        if self.route_success < thresholds['route_success_min']:
            failing_metrics.append(self.route_success)

        if self.unit_success < thresholds['unit_success_min']:
            failing_metrics.append(self.unit_success)

        if self.unit_success < thresholds['measurement_integration_min']:
            failing_metrics.append(self.unit_success)

        if self.route_success < thresholds['route_success_min']:
            failing_metrics.append(self.route_success)

        if not failing_metrics:  # no errors logged
            return None
        else:
            return failing_metrics


class DataQualityMetric:
    """
    Class is used to store data quality metrics.
    """

    def __init__(
        self, hpo='', table='', metric_type='', value=0,
            data_quality_dimension='', first_reported=date.today()):

        self.hpo = hpo
        self.table = table
        self.metric_type = metric_type
        self.value = value
        self.data_quality_dimension = data_quality_dimension
        self.first_reported = first_reported

    def print_dqd_attributes(self):
        print(
            "HPO: {hpo}\n"
            "Table: {table}\n"
            "Metric Type: {metric_type}\n"
            "Value: {value}\n"
            "Data Quality Dimension: {dqd}\n"
            "First Reported: {date}".format(
                hpo=self.hpo, table=self.table,
                metric_type=self.metric_type,
                value=self.value, dqd=self.data_quality_dimension,
                date=self.first_reported))
