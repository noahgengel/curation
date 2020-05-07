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

# ### Function is used to create the models as designated by [EDQ-456](https://precisionmedicineinitiative.atlassian.net/browse/EDQ-456?focusedCommentId=61806&page=com.atlassian.jira.plugin.system.issuetabpanels%3Acomment-tabpanel#comment-61806). 
#
# #### These models will include the following:
# Leverage the concept_ancestor table in an attempt to get a larger ‘scope’ of potential concept_ids associated with height and weight
#
# Create visualizations for the height, weight, and calculated BMI after excluding set amounts of data
#
# 1 stdev, 2 stdev, 3 stdev, etc.
#
# The calculated BMI would perhaps be useful to see if erroneous heights are almost always associated with erroneous weights
#
# This could also be an interesting contrast to the BMI provided by its own concept_id.
