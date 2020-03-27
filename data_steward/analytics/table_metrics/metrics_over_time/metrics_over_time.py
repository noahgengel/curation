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
