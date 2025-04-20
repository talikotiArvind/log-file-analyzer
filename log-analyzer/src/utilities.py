'''
This module provides utility functions for log analysis.
'''

import os, json
from log_analysis import LogAnalysis
from model import LogEntry
    
def log_results_decorator(func):
    """
    Decorator to capture successful and failed entries into separate JSON files.
    """

    log_analysis = LogAnalysis()

    def wrapper(*args, **kwargs):
        entry_data = []
        
        for result in func(*args, **kwargs):
            entry_data.append(result)
            log_analysis.analyze_entry(result)
        
        # Dump the combined entries to a single JSON file
        dump_to_json(entry_data, "./output/analyzer_output.json")
        log_analysis.export_to_json("./output/log_analysis.json")
        log_analysis.to_csv()

        return entry_data  # Return only successful entries for further processing
    
    return wrapper

def dump_to_json(data, output_file):
    """
    Dump the processed log data into a JSON file.

    :param data: List of processed log entries
    :param output_file: Path to the output JSON file
    """
    try:
        if os.path.exists(output_file):
            open(output_file, 'w').close()
        with open(output_file, 'w') as file:
            json.dump(data, file, indent=4)
        # print(f"Data successfully written to {output_file}")
    except Exception as e:
        print(f"An error occurred while writing to JSON file: {e}")

def read_log_file(file_path):
    """
    Generator function to read a log file line by line.

    :param file_path: Path to the log file
    :yield: A line from the log file
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield line.strip()
    except FileNotFoundError:
        raise(f"Error: The file '{file_path}' was not found.")
    except Exception as e:
        return f"An error occurred: {e}"

def parse_log_line(line):
    """
    Parse a single log line and convert it into a LogEntry data model.

    :param line: A single line from the log file
    :return: A LogEntry object or None if the line cannot be parsed
    """
    try:
        # print(f"Parsing line: {line}")
        parts = line.split(" - ")
        if len(parts) == 4:
            parsed_entry = {
                "date_time": parts[0],
                "service_name": parts[1],
                "log_level": parts[2],
                "message": parts[3]
            }
            entry = LogEntry(**parsed_entry)
            output = dict(entry)
    except Exception as e:
        output = f"Failed to parse line: {line}. Error: {e}"
    finally:
        return output
