"""
File is intended to store some of the messages to be put into the program.
These messages can include:
    - Error messages
    - Text for the introduction/conclusion of the email
"""

introduction = """
Dear {EHR site},

My name is {name} and I am a Data Analyst at Columbia University Medical Center with the All of Us precision medicine initiative. CUMC has been reviewing your file submissions for the past few weeks and would like to share its findings with you.

In this e-mail, you will see if you have any errors with your most recent submission. We will also attach {num_metrics} images that display data quality metrics. These findings
are based on your latest submission as of {date}.
"""

fnf_error = \
    "{file} not found in the current directory: {cwd}. " \
    "Please ensure that the file names are " \
    "consistent between the Python script and the " \
    "file name in your current directory."

great_job = """
    All of the issues regarding the 11 monitored metrics have met or
    exceeded the DRC's expectations.
    """

sign_off = """
If have questions about our metrics, please consult the AoU EHR website at this link: {link} 
under the 'Data Quality Metrics' tab at the top of the page. This site contains descriptions, videos, and SQL queries that can help you troubleshoot your data quality."""
