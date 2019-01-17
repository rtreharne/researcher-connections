"""
Script to manage emails to staff containing details of PDRAs interested in teaching opportunities

R. Treharne

16 Jan 2019
"""

from __future__ import print_function
from quickstart import get_google_sheet
import numpy as np
from difflib import SequenceMatcher
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import re

ACADEMIC_SPREADSHEET_ID = '1LgSiaEj9oJUiqgtUEFnHVGtAlm5tffTjuvAcYoWJYjg'
PDRA_SPREADSHEET_ID = '1jp4zyL0l_CazqATbGQlMTh6ensKGQjZO5waw85uC-bQ'
RANGE = 'Form Responses 1'

academic_df = get_google_sheet(ACADEMIC_SPREADSHEET_ID, RANGE)
pdra_df = get_google_sheet(PDRA_SPREADSHEET_ID, RANGE)

# TODO: convert rows in dataframes to strings

academic_slim = academic_df[academic_df.columns[3:6]]
pdra_slim = pdra_df[pdra_df.columns[6:7]]

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def df_to_strings(df):
    strings = []
    for index, row in df.iterrows():
        strings.append(' '.join(row.tolist()).upper())
    return strings

academic_strings = df_to_strings(academic_slim)
pdra_strings = [re.sub("\s\s+", " ", x).split(",") for x in df_to_strings(pdra_slim)]


def pdra_to_projects(pdra_strings, academic_strings):
    pdra_projects = {}
    for i, pdra in enumerate(pdra_strings):
        project_list = []
        for item in pdra:
            temp_list = []
            for project in academic_strings:
                temp_list.append(similar(item, project))
            project_list.append(temp_list.index(max(temp_list)))
        pdra_projects[i] = project_list

    return pdra_projects

pdra_projects = pdra_to_projects(pdra_strings, academic_strings)

print(pdra_projects)




# TODO: use sequence mathing to determine which project is wanted by each PDRA


