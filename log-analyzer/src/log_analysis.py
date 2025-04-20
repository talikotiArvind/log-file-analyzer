
from pydantic import BaseModel
import json
from collections import Counter
import pandas as pd

class LogAnalysis(BaseModel):
    """
    LogAnalysis
    A model representing the analysis of log entries.
    """
    
    successful_entries: list = []
    failed_entries: list = []
    service_entries: dict = {}
    log_level_entries: dict = {}
    error_messages: list = []

    def analyze_entry(self, entry):
        """
        Analyze a log entry and categorize it into successful or failed.
        """
        if isinstance(entry, dict):
            self.add_successful_entry(entry)
        else:
            self.add_failed_entry(entry)
        self.add_service_entry(entry)
        self.add_log_level_entry(entry)

    def export_to_json(self, file_path):
        """
        Export the log analysis data to a JSON file.
        """

        data = self.get_stat_data()

        with open(file_path, "w") as json_file:
            json.dump(data, json_file, indent=4)

    def add_successful_entry(self, entry):
        """
        Add a successful log entry to the analysis.
        """
        self.successful_entries.append(entry)
    
    def add_failed_entry(self, entry):
        """
        Add a failed log entry to the analysis.
        """
        self.failed_entries.append(entry)

    def add_service_entry(self, entry):
        """
        Add a log entry to the service entries.
        Fetch the service name from the entry.
        """
        if isinstance(entry, dict):
            service_name = entry.get("service_name")
            if service_name not in self.service_entries:
                self.service_entries[service_name] = []
            self.service_entries[service_name].append(entry)

    def add_log_level_entry(self, entry):
        """
        Add a log entry to the log level entries.
        Fetch the log level from the entry.
        """
        if isinstance(entry, dict):
            log_level = entry.get("log_level")
            if log_level not in self.log_level_entries:
                self.log_level_entries[log_level] = []
            self.log_level_entries[log_level].append(entry)


    
    def get_stat_data(self):
        """
        Get the statistics data for the log analysis.
        """
        return {
            "successful_entries": len(self.successful_entries),
            "failed_entries": len(self.failed_entries),
            "service_entries": {k: len(v) for k, v in self.service_entries.items()},
            "log_level_entries": {k: len(v) for k, v in self.log_level_entries.items()},
            "most_common_error": self.get_most_commom_error_msg()
        }
    
    def get_most_commom_error_msg(self):
        """
        Get the most common error message from the failed entries.
        """
        self.get_error_messages()
        return Counter(self.error_messages)
    
    def get_error_messages(self):
        """
        Get all error messages from the successfull entries.
        """
        self.error_messages = [entry.get("message") for entry in self.log_level_entries['ERROR'] if isinstance(entry, dict)]

    def to_csv(self):
        """
            Convert the log analysis data into a single CSV file with multiple pages (sheets).
        """
        with pd.ExcelWriter("./output/log_analysis.xlsx", engine="xlsxwriter") as writer:
            # Write successful entries to a sheet
            pd.DataFrame(self.successful_entries).to_excel(writer, sheet_name="Successful Entries", index=False)

            # Write failed entries to a sheet
            pd.DataFrame(self.failed_entries).to_excel(writer, sheet_name="Failed Entries", index=False)

            # Write service entries to a sheet
            service_entries_df = pd.DataFrame([
            {"service_name": service, "count": len(entries), "entries": entries}
            for service, entries in self.service_entries.items()
            ])
            service_entries_df.to_excel(writer, sheet_name="Service Entries", index=False)

            # Write log level entries to a sheet
            log_level_entries_df = pd.DataFrame([
            {"log_level": log_level, "count": len(entries), "entries": entries}
            for log_level, entries in self.log_level_entries.items()
            ])
            log_level_entries_df.to_excel(writer, sheet_name="Log Level Entries", index=False)

            # Write most common error messages to a sheet
            most_common_error_df = pd.DataFrame(self.get_most_commom_error_msg().items(), columns=["Error Message", "Count"])
            most_common_error_df.to_excel(writer, sheet_name=" Error Messages count ", index=False)