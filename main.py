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
import time
import os


def gen_mailto_links(df):
    for i, row in df.iterrows():
        row["Email address"] = "<a href='mailto:" + row["Email address"] + "'>" + row["Email address"] + "</a>"
    return df


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

def df_to_strings(df):
    strings = []
    for index, row in df.iterrows():
        strings.append(' '.join(row.tolist()).upper())
    return strings



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

def save_and_send(debug=False):
    dirname = str(int(time.time()))
    os.mkdir("email/" + dirname)
    for i, key in enumerate(pdra_projects.keys()):
        a_record = academic_df.iloc[key]
        # get map
        pdra_indices = pdra_projects[key]
        pdra_data = pdra_df.iloc[pdra_indices]

        email_gen.Gen_Email(a_record["Email Address"], 'R.Treharne@liverpool.ac.uk', dir=dirname, a_data = a_record, p_data = pdra_data.iloc[:, [1,2,4,5,7,8,9]])

if __name__ =="__main__":
    academic_df = get_google_sheet(ACADEMIC_SPREADSHEET_ID, RANGE)
    pdra_df = gen_mailto_links(get_google_sheet(PDRA_SPREADSHEET_ID, RANGE))
    academic_slim = academic_df[academic_df.columns[3:6]]
    pdra_slim = pdra_df[pdra_df.columns[6:7]]
    academic_strings = df_to_strings(academic_slim)
    pdra_strings = df_to_strings(pdra_slim)
    pdra_projects = projects_pdras(pdra_strings, academic_strings)
    save_and_send()