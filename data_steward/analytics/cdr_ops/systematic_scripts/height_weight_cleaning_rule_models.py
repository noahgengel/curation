# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.4.2
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# ## Function is used to create the models as designated by [EDQ-456](https://precisionmedicineinitiative.atlassian.net/browse/EDQ-456?focusedCommentId=61806&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-61806). 
#
# ### These models will include the following:
# - Leverage the concept_ancestor table in an attempt to get a larger ‘scope’ of potential concept_ids associated with height and weight
#
# - Create visualizations for the height, weight, and calculated BMI after excluding set amounts of data
#
# - 1 stdev, 2 stdev, 3 stdev, etc.
#
# - The calculated BMI would perhaps be useful to see if erroneous heights are almost always associated with erroneous weights
#
# - This could also be an interesting contrast to the BMI provided by its own concept_id.

from google.cloud import bigquery
# %reload_ext google.cloud.bigquery
client = bigquery.Client()
# %load_ext google.cloud.bigquery

# +
from notebooks import parameters
DATASET = parameters.LATEST_DATASET

print(f"Dataset to use: {DATASET}")

# +
import warnings

warnings.filterwarnings('ignore')
import pandas as pd
import matplotlib.pyplot as plt
import os

plt.style.use('ggplot')
pd.options.display.max_rows = 999
pd.options.display.max_columns = 999
pd.options.display.max_colwidth = 999


def cstr(s, color='black'):
    return "<text style=color:{}>{}</text>".format(color, s)


# -

cwd = os.getcwd()
cwd = str(cwd)
print("Current working directory is: {cwd}".format(cwd=cwd))

# # Part I: Investigating the concepts used in the measurement table

# #### The string below will be used to exclude certain concept_ids

# +
height_concepts = "1003912, 45876161, 1003116, 1003232, 40655804, 45876162"

weight_concepts = "1002670, 45876171, 1003383, 1004141, 40655805, 45876172, 3042378"
# -

caveat_string = """
  AND LOWER(c.domain_id) LIKE '%measurement%'
  AND LOWER(c.concept_name) NOT LIKE '%birth%' -- excluding as outliers
  AND LOWER(c.concept_name) NOT LIKE '%fetal%'
  AND LOWER(c.concept_name) NOT LIKE '%fetus%'
  AND LOWER(c.concept_name) NOT LIKE '%bmi%'
  AND LOWER(c.concept_name) NOT LIKE '%lower segment%'
  AND LOWER(c.concept_name) NOT LIKE '%upper segment%'
  AND LOWER(c.concept_name) NOT LIKE '%body fat%'
  AND LOWER(c.concept_name) NOT LIKE '%muscle mass%'
  AND LOWER(c.concept_name) NOT LIKE '%percentile%'
  AND LOWER(c.concept_name) NOT LIKE '%weight-for-length%'
  AND LOWER(c.concept_name) NOT LIKE '%difference%'
"""

# ### See the concept usage for weight

CONCEPT_ID_STRINGS = weight_concepts

get_all_descendant_concepts_as_table = f"""
WITH
height_and_weight_concepts AS
(SELECT
  DISTINCT ca.descendant_concept_id,
  c.concept_name AS descendant_name,
  c.domain_id AS domain
FROM
  `{DATASET}.concept_ancestor` ca
JOIN
  `{DATASET}.concept` c
ON
  ca.descendant_concept_id = c.concept_id
WHERE
  ca.ancestor_concept_id IN 
  ({CONCEPT_ID_STRINGS})
  {caveat_string})
"""

bulk_of_query = f"""
SELECT
DISTINCT
m.measurement_concept_id, c.concept_name, 
COUNT(DISTINCT mm.src_hpo_id) as num_sites,
COUNT(*) as num_rows

FROM
`{DATASET}.unioned_ehr_measurement` m
JOIN
`{DATASET}.concept` c
ON
m.measurement_concept_id = c.concept_id

JOIN
`{DATASET}._mapping_measurement` mm
ON
m.measurement_id = mm.measurement_id 

WHERE m.measurement_concept_id IN
  (SELECT DISTINCT
  h_w.descendant_concept_id
  FROM
  height_and_weight_concepts AS h_w)

GROUP BY 1, 2
ORDER BY num_rows DESC
"""

full_weight_query = get_all_descendant_concepts_as_table + bulk_of_query

weight_concept_usage = pd.io.gbq.read_gbq(full_weight_query, dialect='standard')

weight_concept_usage

# ### See the concept usage for height

CONCEPT_ID_STRINGS = height_concepts

get_all_descendant_concepts_as_table = f"""
WITH
height_and_weight_concepts AS
(SELECT
  DISTINCT ca.descendant_concept_id,
  c.concept_name AS descendant_name,
  c.domain_id AS domain
FROM
  `{DATASET}.concept_ancestor` ca
JOIN
  `{DATASET}.concept` c
ON
  ca.descendant_concept_id = c.concept_id
WHERE
  ca.ancestor_concept_id IN 
  ({CONCEPT_ID_STRINGS})
  {caveat_string})
"""

full_height_query = get_all_descendant_concepts_as_table + bulk_of_query

height_concept_usage = pd.io.gbq.read_gbq(full_weight_query, dialect='standard')

height_concept_usage
