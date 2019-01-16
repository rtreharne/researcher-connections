"""
Script to manage emails to staff containing details of PDRAs interested in teaching opportunities

R. Treharne

16 Jan 2019
"""

from __future__ import print_function
from quickstart import get_google_sheet
import numpy as np

from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

ACADEMIC_SPREADSHEET_ID = '1LgSiaEj9oJUiqgtUEFnHVGtAlm5tffTjuvAcYoWJYjg'
PDRA_SPREADSHEET_ID = '1jp4zyL0l_CazqATbGQlMTh6ensKGQjZO5waw85uC-bQ'
RANGE = 'Form Responses 1'

academic_sheet = get_google_sheet(ACADEMIC_SPREADSHEET_ID, RANGE)
pdra_sheet = get_google_sheet(PDRA_SPREADSHEET_ID, RANGE)




