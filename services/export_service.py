import gspread
from gspread_formatting import *
from google.oauth2.service_account import Credentials
from gspread.exceptions import WorksheetNotFound

from utils import datetime_generator
from services import google_auth

class ExportService:
    """
    Exports the final results of jobs evaluated by LLM Evaluator, to a Google spreadsheet
    """

    def __init__(self, sheet_key, valid_jobs, mcr_jobs):
        self.gc = google_auth.get_gspread_client()
        self.job_sheet = self.gc.open_by_key(sheet_key)
        print(f"'{self.job_sheet}' has been loaded successfully!")
        self.valid_jobs = valid_jobs
        self.mcr_jobs = mcr_jobs


    def _generate_worksheet(self, job_type):
        """
        Generates a new worksheet unless the same name based on the datetime doesn't exist

        :arg job_type: whether it's a list of valid jobs or mcr(manual_check_required) jobs
        """

        sheet_title = f"{datetime_generator.generate_current_datetime()}_{job_type.upper()}"

        try:
            worksheet = self.job_sheet.worksheet(sheet_title)
            print(f"Worksheet({job_type}) for the given date already exists")
        except WorksheetNotFound:
            worksheet = self.job_sheet.add_worksheet(
                title=sheet_title,
                rows=500,
                cols=10
            )

        return worksheet

    def _format_sheet(self, worksheet, col_len):
        end_col = chr(64 + col_len)

        #### Header ####
        worksheet.format(
            ranges=f"A1:{end_col}",
            format={
                "backgroundColor": {
                    "red": 0.72,
                    "green": 0.84,
                    "blue": 0.96
                },
                "horizontalAlignment": "CENTER",
                "textFormat": {
                    "bold": True
                }
            }
        )

        #### Rows ####
        worksheet.format(
            ranges=f"A2:{end_col}",
            format={
                "backgroundColor": {
                    "red": 0.92,
                    "green": 0.96,
                    "blue": 1.0
                },
                "horizontalAlignment": "LEFT",
                "textFormat": {
                    "bold": False
                }
            }
        )

    def _set_column_widths(self, worksheet, widths):
        set_column_widths(worksheet, widths)


    def export_jobs(self):
        """
        Export job data to the spreadsheet
        """

        job_groups = {
            "valid": self.valid_jobs,
            "mcr": self.mcr_jobs
        }

        for job_type, jobs in job_groups.items():

            worksheet = self._generate_worksheet(job_type)

            if job_type == "valid":
                headers = ["Title", "Keep", "Score", "Reason", "URL", "Source"]

                rows = [
                    headers,
                    *[
                        [job.title, job.keep, job.score, job.reason, job.url, job.searched_via]
                        for job in jobs
                    ]
                ]

                #### Width ####
                width = [
                    ('A', 300), ('B', 50), ('C', 50), ('D', 300), ("E", 150), ("F", 50)
                ]

            else:
                headers = ["Title", "Keep", "Score", "Reason", "URL", "Source", "MCR"]

                rows = [
                    headers,
                    *[
                        [job.title, job.keep, job.score, job.reason, job.url, job.searched_via,
                         job.manual_check_required]
                        for job in jobs
                    ]
                ]

                #### Width ####
                width = [
                    ('A', 300), ('B', 50), ('C', 50), ('D', 300), ("E", 150), ("F", 50), ("G", 50)
                ]

            worksheet.update("A1", rows)

            self._format_sheet(worksheet, len(headers))
            self._set_column_widths(worksheet, width)
