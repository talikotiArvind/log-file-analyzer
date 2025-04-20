# log-file-analyzer
Performs log analysis for a given file input

The project contains following set of souce codes

## log_analyzer.py

It defines a module for analyzing log files. It includes the process_logs function, which uses a thread pool to process log lines concurrently. The function reads log lines from a file, processes each line using the parse_log_line function, and checks if all lines were processed successfully. It uses a decorator log_results_decorator to log results.

## log_analysis.py

The file defines a LogAnalysis class that provides functionality to analyze log entries, categorize them, and generate statistics. Below is a breakdown of its key components:

**successful_entries**: A list to store successfully processed log entries.
**failed_entries**: A list to store failed log entries.
**service_entries**: A dictionary categorizing log entries by service name.
**log_level_entries**: A dictionary categorizing log entries by log level (e.g., ERROR, INFO).
**error_messages**: A list to store error messages extracted from log entries.

## model.py

This file defines a Pydantic data model for log entries.It represents a single log entry with details such as timestamp, service name, log level, and message.

It provides necessary constraints to the data entry if the format is missing (For eg, timestamp, log level entries etc.) to provide proper parsing of log entry.

## utilities.py

This module provides utility functions for log analysis, including reading, parsing, and exporting log data. Below is a breakdown of the key components:

**log_results_decorator** : A decorator to process log entries, analyze them, and export results to JSON and CSV files.

**dump_to_json(data, output_file)** : Writes a list of processed log entries to a JSON file.

**read_log_file** : Reads a log file line by line as a generator.

**parse_log_line** : Parses a single log line into a LogEntry object.

**main.py** : Execution trigger of analyzer.

## Workflow

We navigate to the src folder and add app.log file in same directory as main.py

execute the main.py path
NOTE:
As alternate , we can chage the path of app.log anywhere. We just have to update the global variable ```LOG_FILE_PATH``` accordingly

Once executed, we will get the status of log file parsing.
the outputs will be stored in the folder "output"

We get 3 types of output
1.  **analyzer_output.json** : This converts the entries in app.log into json objects after parsing it as data object. Failure of any improper entries gets if logged with error message

2. **log_analysis.json**: This is output of statistical data that provides categorical data with their statistics. This involves successful and failed parsed entries, service and log -level based entries and count of error mesages.

3. **log_analysis.xlsx**: This is the CSV file format of log_analysis.json. Each statistical data is defined as a separated sheet within excel.

### NOTE:

**Possible further updates that be done:**

1. Dockerize the application and use it as plugin service
2. Create it as python package 
