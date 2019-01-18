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
import email_gen
import pandas as pd
from sheet_info import *

academic_df = get_google_sheet(ACADEMIC_SPREADSHEET_ID, RANGE)
pdra_df = get_google_sheet(PDRA_SPREADSHEET_ID, RANGE)

for i, row in pdra_df.iterrows():
    row["Email address"] = "<a href='mailto:" + row["Email address"] + "'>" + row["Email address"] + "</a>"

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

def transpose_dict(dict):
    trans_dict = {}
    for key in dict.keys():
        for item in dict[key]:
            try:
                if key not in trans_dict[item]:
                    trans_dict[item].append(key)
            except KeyError:
                trans_dict[item] = [key]
    return trans_dict

def projects_pdras(pdra_strings, academic_strings):
    pdra_projects = {}
    for i, pdra in enumerate(pdra_strings):
        project_list = []
        for item in pdra:
            temp_list = []
            for project in academic_strings:
                temp_list.append(similar(item, project))
            project_list.append(temp_list.index(max(temp_list)))
        pdra_projects[i] = project_list

    return transpose_dict(pdra_projects)

pdra_projects = projects_pdras(pdra_strings, academic_strings)

for i, key in enumerate(pdra_projects.keys()):
    a_record = academic_df.iloc[key]
    # get map
    pdra_indices = pdra_projects[key]
    pdra_data = pdra_df.iloc[pdra_indices]
    msg = email_gen.Gen_Email(a_record["Email Address"], 'R.Treharne@liverpool.ac.uk', filename=i, a_data = a_record, p_data = pdra_data.iloc[:, [1,2,3,4,5,7,8,9]])

