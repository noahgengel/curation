"""
File is intended to store a number of functions that are
used to create the HPO objects throughtout the script.
"""

from dictionaries_and_lists import full_names
from hpo_class import HPO


def establish_hpo_objects(dqm_objects):
    """
    Function is used as a 'launch pad' for all of the other functions
    that create HPO objects based on the various DataQualityMetric
    objects

    Parameters
    ----------
    dqm_objects (list): list of DataQualityMetric objects.
        these will eventually be associated to their respective
        HPO objects.

    Return
    ------
    blank_hpo_objects (list): list of the blank HPO objects. there
        should be a unique (and mostly empty) object for each HPO
        and date (total length should be #HPOs times #dates)
    """
    names_to_establish = []
    dates_to_establish = []
    blank_hpo_objects = []

    for obj in dqm_objects:
        name = obj.name
        date = obj.date

        if name not in names_to_establish:
            names_to_establish.append(name)

        if date not in dates_to_establish:
            dates_to_establish.append(date)

    # create unique object for each HPO and date
    for hpo_name in names_to_establish:
        full_name = full_names[hpo_name]

        for date in dates_to_establish:

            hpo = HPO(
              name=hpo_name, full_name=full_name,
              date=date,

              # all of the metric objects to be left blank
              # for the time being

              concept_success=[], duplicates=[],
              end_before_begin=[], data_after_death=[],
              route_success=[], unit_success=[],
              measurement_integration=[], ingredient_integration=[]
              )

            blank_hpo_objects.append(hpo)

    return blank_hpo_objects
