"""
File is intended to establish a 'HPO class' that can be used
to store data quality metrics for each HPO in an easy and
identifiable fashion.

Class was used as a means for storing information as the ability
to add functions could prove useful in future iterations of the
script.
"""

from .relevant_dictionaries import thresholds


class HPO:
    """
    Class is used to store data quality metrics.
    """

    def __init__(
            self, name, full_name, concept_success=0, duplicates=0,
            end_before_begin=0, data_after_death=0,
            route_success=0, unit_success=0, measurement_integration=0,
            ingredient_integration=0):

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

        self.concept_success = concept_success
        self.duplicates = duplicates
        self.end_before_begin = end_before_begin
        self.data_after_death = data_after_death
        self.route_success = route_success
        self.unit_success = unit_success
        self.measurement_integration = measurement_integration
        self.ingredient_integration = ingredient_integration

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
        failing_metrics (dict): has the following structure
            keys: data quality metrics that have 'failed'
            values: the actual 'value' that was deemed to have failed

        NOTE:
        if no data quality problems are found, however, the function
        will return 'None' to signify that no issues arose
        """

        failing_metrics = {}

        if self.concept_success < thresholds['concept_success_min']:
            failing_metrics['concept_success'] = self.concept_success

        if self.duplicates > thresholds['duplicates_max']:
            failing_metrics['duplicates'] = self.duplicates

        if self.end_before_begin > thresholds['end_before_begin_max']:
            failing_metrics['end_before_begin'] = self.end_before_begin

        if self.data_after_death > thresholds['data_after_death_max']:
            failing_metrics['data_after_death'] = self.data_after_death

        if self.route_success < thresholds['route_success_min']:
            failing_metrics['route_success'] = self.route_success

        if self.unit_success < thresholds['unit_success_min']:
            failing_metrics['unit_success'] = self.unit_success

        if self.unit_success < thresholds['measurement_integration_min']:
            failing_metrics['measurement_integration'] = self.unit_success

        if self.route_success < thresholds['route_success_min']:
            failing_metrics['route_success'] = self.route_success

        if not failing_metrics:  # no errors logged
            return None
        else:
            return failing_metrics
