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
import numpy as np
from matplotlib import pyplot as plt

# +
from notebooks import parameters
DATASET = parameters.LATEST_DATASET
rounding_val = 2

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

# # Part II: Investigating the distribution of weights for the selected concept_ids

weight_concept_ids = weight_concept_usage['measurement_concept_id'].tolist()

weight_concept_ids = list(map(str, weight_concept_ids))

weight_concepts_as_str = ', '.join(weight_concept_ids)

weight_concepts_as_str

query_all_weights = f"""
SELECT
m.value_as_number
FROM
`{DATASET}.unioned_ehr_measurement` m
WHERE
m.measurement_concept_id IN ({weight_concepts_as_str})
AND
m.value_as_number IS NOT NULL
AND
m.value_as_number <> 9999999  -- issue with one site that heavily skews data
AND
m.value_as_number <> 0.0  -- not something we expect; appears for a site
ORDER BY value_as_number DESC
"""

weight_df = pd.io.gbq.read_gbq(query_all_weights, dialect='standard')

# ### Want to see what the unit distribution is for the measurements that we are looking at

see_weight_unit_distrib = f"""
SELECT
m.unit_as_concept_id, c.concept_name, COUNT(*) as num_measurements
FROM
`{DATASET}.unioned_ehr_measurement` m
JOIN
`{DATASET}.concept` c
ON
m.unit_concept_id = c.concept_id
WHERE
m.measurement_concept_id IN ({weight_concepts_as_str})
AND
m.value_as_number IS NOT NULL
AND
m.value_as_number <> 9999999  -- issue with one site that heavily skews data
AND
m.value_as_number <> 0.0  -- not something we expect; appears for a site
GROUP BY 1, 2
ORDER BY value_as_number DESC
"""

unit_df_for_weights = pd.io.gbq.read_gbq(see_weight_unit_distrib, dialect='standard')

unit_df_for_weights

# +
## 

# +
weights = weight_df['value_as_number'].tolist()

number_records = str(len(weights))
mean = str(round(np.mean(weights), rounding_val))

decile1 = str(round(np.percentile(weights, 10), rounding_val))

quartile1 = str(round(np.percentile(weights, 25), rounding_val))
median = str(round(np.percentile(weights, 50), rounding_val))
quartile3 = str(round(np.percentile(weights, 75), rounding_val))

decile9 = str(round(np.percentile(weights, 90), rounding_val))

stdev = str(round(np.std(np.asarray(weights)), rounding_val))

min_weight = min(weights)
max_weight = max(weights)

# -

general_weight_attributes = f"""
Number of weights: {number_records}

Minimum: {min_weight}
maximum: {max_weight}

Mean Weight: {mean}
Standard Devidation: {stdev}

10th Percentile: {decile1}
25th Percentile: {quartile1}
Median: {median}
75th Percentile: {quartile3}
90th Percentile: {decile9}
"""

print(general_weight_attributes)

# +

plt.xlim([min_weight - 5, 400])

plt.hist(weights, bins=50, alpha= 0.5)
plt.title('Weight Distribution Across All Sites')
plt.xlabel('Weight')
plt.ylabel('Count')

plt.show()
# -


