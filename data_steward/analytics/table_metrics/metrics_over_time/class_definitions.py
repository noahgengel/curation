"""
File is intended to establish a 'HPO class' that can be used
to store data quality metrics for each HPO in an easy and
identifiable fashion.
Class was used as a means for storing information as the ability
to add functions could prove useful in future iterations of the
script.
"""

from dictionaries_lists_and_prompts import thresholds
import datetime
import sys


class DataQualityMetric:
    """
    Class is used to store data quality metrics.
    """

    def __init__(
        self, hpo='', table='', metric_type='', value=0,
            data_quality_dimension='', date=datetime.today()
    ):

        """
        Used to establish the attributes of the DataQualityMetric
        object being instantiated.
        Parameters
        ----------
        hpo (string): name of the HPO being associated with the
            data quality metric in question (e.g. nyc_cu)

        table (string): name of the table whose data quality metric
            is being determined (e.g. Measurement)

        metric_type (string): name of the metric that is being
            determined (e.g. duplicates)

        value (float): value that represents the quantitative value
            of the data quality metric being investigated

        data_quality_dimension (string): represents whether the
            metric_type being investigated is related to the
            conformance, completeness, or plausibility of data
            quality with respect to the Kahn framework

        date (datetime): 'date' that the DQM represents (in
            other words, the corresponding analytics
            report from which it hails)
        """

        self.hpo = hpo
        self.table = table
        self.metric_type = metric_type
        self.value = value
        self.data_quality_dimension = data_quality_dimension
        self.date=date

    def print_dqd_attributes(self):
        """
        Function is used to print out some of the attributes
        of a DataQualityMetric object in a manner that enables
        all of the information to be displayed in a
        human-readable format.
        """
        print(
            "HPO: {hpo}\n"
            "Table: {table}\n"
            "Metric Type: {metric_type}\n"
            "Value: {value}\n"
            "Data Quality Dimension: {dqd}\n"
            "Date: {date}\n\n".format(
                hpo=self.hpo, table=self.table,
                metric_type=self.metric_type,
                value=self.value, dqd=self.data_quality_dimension,
                date=self.date))

    def get_list_of_attribute_names(self):
        """
        Function is used to get a list of the attributes that
        are associated with a DataQualityMetric object. This will
        ultimately be used to populate the columns of a
        pandas dataframe.
        Return
        ------
        attribute_names (list): list of the attribute names
            for a DataQualityMetric object
        """

        attribute_names = [
            "HPO", "Table", "Metric Type",
            "Value", "Data Quality Dimension", "Date"]

        return attribute_names

    def get_attributes_in_order(self):
        """
        Function is used to get the attributes of a particular
        DataQualityMetric object in an order that parallels
        the get_list_of_attribute_names function above. This
        will be used to populate the dataframe with data quality
        issues.
        Return
        ------
        attributes (list): list of the attributes (values, strings)
            for the object
        """

        attributes = [
            self.hpo, self.table, self.metric_type, self.value,
            self.data_quality_dimension, self.date]

        return attributes


class HPO:
    """
    Class is used to associated data quality issues with a particular
    HPO.
    """

    def __init__(
            self,

            # basic attributes
            name, full_name, date,

            # data quality metrics
            concept_success, duplicates,
            end_before_begin, data_after_death,
            route_success, unit_success, measurement_integration,
            ingredient_integration,

            # number of rows for the 6 canonical tables
            num_measurement_rows = 0,
            num_visit_rows = 0,
            num_procedure_rows = 0,
            num_condition_rows = 0,
            num_drug_rows = 0,
            num_observation_rows = 0):

        """
        Used to establish the attributes of the HPO object being instantiated.
        Parameters
        ----------
        self (HPO object): the object to be created
        name (str): name of the HPO ID to create (e.g. nyc_cu)

        full_name (str): full name of the HPO

        date (datetime): 'date' that the HPO represents (in
            other words, the corresponding analytics
            report from which it hails)

        concept_success (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to concept success rate. each index should also
            represent a different table.

        duplicates (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to the number of duplicates. each index should
            also represent a different table

        end_before_begin (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to the number of end dates preceding start dates.
            each index should also represent a different table

        data_after_death (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to the percentage of data points that follow a
            patient's death date. each index should also
            represent a different table

        route_success (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to the concept success rate for the route_concept_id
            field. should have a length of one (for the drug
            exposure table)

        unit_success (list): list of DataQuality metric objects
            that should all have the metric_type relating
            to the concept success rate for the route_concept_id
            field. should have a length of one (for the
            measurement table)

        measurement_integration (list): list of DataQuality metric
            objects that should all have the metric_type relating
            to the integration of certain measurement concepts.
            should have a length of one (for the measurement
            table).

        ingredient_integration (list): list of DataQuality metric
            objects that should all have the metric_type relating
            to the integration of certain drug ingredients.
            should have a length of one (for the drug exposure
            table).

        num_measurement_rows (float): number of rows in the
            measurement table

        num_visit_rows (float): number of rows in the
            visit_occurrence table

        num_procedure_rows (float): number of rows in the
            procedure_occurrence table

        num_condition_rows (float): number of rows in the
            condition_occurrence table

        num_drug_rows (float): number of rows in the drug
            exposure table

        number_observation_rows (float): number of rows
            in the observation table
        """
        # inherent attributes
        self.name = name
        self.full_name = full_name
        self.date = date

        # relates to multiple tables
        self.concept_success = concept_success
        self.duplicates = duplicates
        self.end_before_begin = end_before_begin
        self.data_after_death = data_after_death

        # only relates to one table
        self.route_success = route_success
        self.unit_success = unit_success
        self.measurement_integration = measurement_integration
        self.ingredient_integration = ingredient_integration

        # number of rows in each table
        self.num_measurement_rows = num_measurement_rows,
        self.num_visit_rows = num_visit_rows,
        self.num_procedure_rows = num_procedure_rows,
        self.num_condition_rows = num_condition_rows,
        self.num_drug_rows = num_drug_rows,
        self.num_observation_rows = num_observation_rows

    def add_attribute_with_string(self, metric, dq_object):
        """
        Function is designed to enable the script to add
        a DataQualityMetric object to the attributes that
        define an HPO object. This will allow us to easily
        associate an HPO object with its constituent data
        quality metrics

        Parameters
        ----------
        metric (string): the name of the sheet that contains the
            dimension of data quality to be investigated

        dq_object (DataQualityMetric): object that contains
            the information for a particular aspect of the
            site's data quality (NOTE: dq_object.hpo should
            equal self.name whenever this is used)
        """

        if metric == 'Concept ID Success Rate':
            self.concept_success.append(dq_object)

        elif metric == 'Duplicate Records':
            self.duplicates.append(dq_object)

        elif metric == 'End Dates Preceding Start Dates':
            self.end_before_begin.append(dq_object)

        elif metric == 'Data After Death':
            self.data_after_death.append(dq_object)

        elif metric == 'Measurement Integration':
            self.measurement_integration.append(dq_object)

        elif metric == 'Drug Ingredient Integration':
            self.ingredient_integration.append(dq_object)

        elif metric == 'Route Concept ID Success Rate':
            self.route_success.append(dq_object)

        elif metric == 'Unit Concept ID Success Rate':
            self.unit_success.append(dq_object)

        else:
            print("Unrecognized metric input: {metric} for {hpo}".format(
                metric=metric, hpo=self.name))
            sys.exit(0)

    def use_table_name_to_find_rows(self, table, metric):
        """
        Function is intended to use the table name to find
        the 'total number of rows' associated with said
        table and the 'success rate' for said table.
        Both should which should be stored in the HPO object.

        Parameters
        ----------
        table (string): table whose data quality metrics are
            to be determined

        metric (string): the metric (e.g. the concept
            success rate) that is being investigated

        Returns
        -------
        succ_rate (float): success rate for the particular table

        total_rows (float): the total number of rows for the
            table being queried
        """

        if metric == 'Concept ID Success Rate':
            for object in self.concept_success:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Duplicate Records':
           for object in self.duplicates:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'End Dates Preceding Start Dates':
            for object in self.end_before_begin:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Data After Death':
            for object in self.data_after_death:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Measurement Integration':
            for object in self.measurement_integration:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Drug Ingredient Integration':
            for object in self.measurement_integration:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Route Concept ID Success Rate':
            for object in self.measurement_integration:
                if object.table == table:
                    succ_rate = object.value

        elif metric == 'Unit Concept ID Success Rate':
            for object in self.measurement_integration:
                if object.table == table:
                    succ_rate = object.value

        else:
            raise Exception(
                "Unexpected metric type:"
                "{metric} found for table {table}".format(
                    metric=metric, table=table
                ))

        if table == "Measurement":
            total_rows = self.num_measurement_rows
        elif table == "Visit":
            total_rows = self.num_visit_rows
        elif table == "Procedure":
            total_rows = self.num_procedure_rows
        elif table == "Condition":
            total_rows = self.num_condition_rows
        elif table == "Drug":
            total_rows = self.num_drug_rows
        elif table == "Observation":
            total_rows = self.num_observation_rows
        else:
            raise Exception(
                "Unexpected table type:"
                "{table} found for metric {metric}".format(
                    table=table, metric=metric
                ))

        return succ_rate, total_rows

    def return_metric_row_count(self, metric, table):
        """
        Function is used to return the 'row
        count' for a particular metric. This will be
        useful for determine 'aggregate metrics' which
        are contingent upon 'aggregate' successes over
        totals. This 'row count' could either refer to
        the number of 'successful' rows or the number
        of 'failed' rows depending on the nature of the
        metric that is being investigated.

        Parameters
        ----------
        metric (string): the metric (e.g. the concept
            success rate) that is being investigated

        table (string): table whose data quality metrics are
            to be determined

        Returns
        -------
        row_count (float): total number of rows - merely
            a multiplier of the two aforementioned
            number converted from percent to rows
        """

        if metric == 'Concept ID Success Rate':
            relevant_objects = self.concept_success

            for dqm in relevant_objects:
                dqm_table = dqm.table

                if dqm_table == dqm_table:  # discovered
                    succ_rate, total_rows = \
                        use_table_name_to_find_rows(
                            self, table,
                            metric)
                    succ_rows = total_rows * succ_rate / 100  # convert from percent

        # elif metric == 'Duplicate Records':
        #     self.duplicates.append(dq_object)
        #
        # elif metric == 'End Dates Preceding Start Dates':
        #     self.end_before_begin.append(dq_object)
        #
        # elif metric == 'Data After Death':
        #     self.data_after_death.append(dq_object)
        #
        # elif metric == 'Measurement Integration':
        #     self.measurement_integration.append(dq_object)
        #
        # elif metric == 'Drug Ingredient Integration':
        #     self.ingredient_integration.append(dq_object)
        #
        # elif metric == 'Route Concept ID Success Rate':
        #     self.route_success.append(dq_object)
        #
        # elif metric == 'Unit Concept ID Success Rate':
        #     self.unit_success.append(dq_object)

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

        Returns
        -------
        failing_metrics (list): has a list of the data quality metrics
            for the HPO that have 'failed' based on the thresholds
            provided

        NOTES
        -----
        1. if no data quality problems are found, however, the
        function will return 'None' to signify that no issues arose

        2. this funciton is not currently implemented in our current
        iteration of metrics_over_time. this function, however, holds
        potential to be useful in future iterations.
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

        for route_obj in self.route_success:
            if route_obj.value < thresholds['route_success_min']:
                failing_metrics.append(route_obj)

        for unit_obj in self.unit_success:
            if unit_obj.value < thresholds['unit_success_min']:
                failing_metrics.append(unit_obj)

        for measurement_integration_obj in self.measurement_integration:
            if measurement_integration_obj.value < \
                    thresholds['measurement_integration_min']:
                failing_metrics.append(measurement_integration_obj)

        for ingredient_integration_obj in self.ingredient_integration:
            if ingredient_integration_obj.value < \
                    thresholds['route_success_min']:
                failing_metrics.append(ingredient_integration_obj)

        if not failing_metrics:  # no errors logged
            return None
        else:
            return failing_metrics
