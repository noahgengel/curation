"""
Goals
------
Program should generate a report (Excel file) that shows
how data quality metrics for each HPO site change over time.

Data quality metrics include:
   1. the number of duplicates per table
   2. number of 'start dates' that precede 'end dates'
   3. number of records that are >30 days after a patient's death date
   4. concept table success rates
   5. population of the 'unit' field in the measurement table
   6. population of the 'route' field in the drug exposure table
   7. proportion of expected ingredients observed
   8. proportion of expected measurements observed

Future data quality metrics should also be easily added to this
script.

ASSUMPTIONS
-----------
1. The user has all of the files s/he wants to analyze in the current
directory

2. The user will know to change the 'report' variables to match the
file names of the .xlsx files in the current working directory.

3. All sheets are saved as month_date_year.xlsx
   - month should be fully spelled (august rather than aug)
   - year should be four digits
   - this name is used to determine the date

5. Assumed certain naming conventions in the sheets
   a. consistency in the column names in the 'concept' tab
   b. total/valid rows are logged in the 'concept' tab as
      (first word of the table type)_total_row or
      (first word of the table type)_well_defined_row
      ex: drug_total_row
"""

from startup_functions import \
    get_user_analysis_choice, load_files, generate_hpo_id_col

from data_quality_metric_class import DataQualityMetric

from hpo_class import HPO


# UNIONED EHR COMPARISON
report1 = 'may_10_2019.xlsx'
report2 = 'july_15_2019.xlsx'
report3 = 'october_04_2019.xlsx'
report4 = 'march_19_2020.xlsx'


report_names = [report1, report2, report3, report4]


def startup():
    """
    Function is used to 'startup' the script. This should in essence
    get the user's choice, load the appropriate files, and allow us
    to determine which HPO objects we will instantiate.

    Returns
    -------
    metric_choice (string): represents the sheet from the analysis reports
        whose metrics will be compared over time

    metric_is_percent (bool): determines whether the data will be seen
        as 'percentage complete' or individual instances of a
        particular error

    ideal_low (bool): determines whether the number displayed should
        be considered a desirable or undesirable characteristic

    file_names (list): list of the user-specified Excel files that are
        in the current directory. Files are analytics reports to be
        scanned.

    hpo_id_col (list): list of the strings that should go
        into an HPO ID column. for use in generating HPO objects.
    """
    metric_choice, metric_is_percent, ideal_low = get_user_analysis_choice()
    data_frames = load_files(metric_choice, report_names)
    hpo_name_col = generate_hpo_id_col(report_names)

    return metric_choice, metric_is_percent, ideal_low, \
        data_frames, hpo_name_col


def main():
    """
    Function that executes the entirety of the program.
    """
    user_choice, percent_bool, target_low, dfs, hpo_names = \
        startup()


if __name__ == "__main__":
    main()
