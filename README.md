# Researcher Connections

This repository contains a script, "main.py", that takes responses to the PDRA Researcher Connections form and emails
relevant academics to inform them of interest in their teaching opportunities.

The script uses two Google sheets generated by two corresponding Google Forms:
  + [Academic Form](https://goo.gl/forms/7xnqITJOMwNNZfQn2)
  + [PDRA Response Form](https://goo.gl/forms/7DvEpuini7QeOSh03)

## Instructions

1. Create a new Python environment and install requirements

```bash
$ pipenv install -r requirements.txt
```

2. Configure Google Sheets API. Go to [Python Quickstart](https://developers.google.com/sheets/api/quickstart/python),
click "ENABLE THE GOOGLE SHEETS API" button and create a new Google Sheets project. Download the client configuration
"credentials.json" and put in in the same directory as "main.py".
To run:

3. Update the spreadsheet ID variables in "sheet_info_dummy.py". To obtain the Google Sheet ID, when viewing a google sheet
click "SHARE" button, then click "Get shareable link". The sheet ID is within the shareable URL that is generated, e.g.
"https://docs.google.com/spreadsheets/d/<Spreadsheet_ID>/edit?usp=sharing". Then rename "sheet_info_dummy.py" to "sheet_info.py".

4. Run "main.py":

```bash
$ python main.py
```

This will generate a set of .eml files in the "email" folder. Each email will correspond to each teaching opportunity submitted
and will contain a list of PDRAs who have expressed interest in the opportunity.
