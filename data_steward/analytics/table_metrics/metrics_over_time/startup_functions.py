"""
Python file is intended to be used for the 'startup' of the
metrics_over_time script. This includes prompting the user
to specify his/her analysis target and loading applicable files.
"""

from dictionaries_lists_and_prompts import \
    analysis_type_prompt, choice_dict, percentage_dict, \
    target_low

def get_user_analysis_choice():
    """
    Function gets the user input to determine what kind of data
    quality metrics s/he wants to investigate.

    :return:
    analytics_type (str): the data quality metric the user wants to
        investigate

    percent_bool (bool): determines whether the data will be seen
        as 'percentage complete' or individual instances of a
        particular error

    target_low (bool): determines whether the number displayed should
        be considered a desirable or undesirable characteristic
    """

    user_command = input(analysis_type_prompt).lower()

    while user_command not in choice_dict.keys():
        print("\nInvalid choice. Please specify a letter that corresponds "
              "to an appropriate analysis report.\n")
        user_command = input(analysis_type_prompt).lower()

    analytics_type = choice_dict[user_command]
    percent_bool = percentage_dict[analytics_type]
    target_low = target_low[analytics_type]

    return analytics_type, percent_bool, target_low
