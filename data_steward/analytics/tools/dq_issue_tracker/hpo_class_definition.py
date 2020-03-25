"""
File is intended to establish a 'HPO class' that can be used
to store data quality metrics for each HPO in an easy and
identifiable fashion.

Class was used as a means for storing information as the ability
to add functions could prove useful in future iterations of the
script.
"""

class HPO:
    """
    Class is used to store data quality metrics.
    """

    def __init__(
        self, name, full_name, concept_success = 0, duplicates = 0,
        end_before_begin = 0, data_after_death = 0,
        route_success = 0, unit_success, measurement_integration = 0,
        ingredient_integration = 0):

        """
        Used to establish the attributes of the object being instantiated.

        Parameters
        ----------
        name (str): name of the HPO ID to create (e.g. nyc_cu)

        full_name (str): full name of the HPO

        all other optional parameters are intended to be float objects. they
        each represent a data quality metric that can be found on the AoU
        HPO site at the following link:
        https://sites.google.com/view/ehrupload
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


