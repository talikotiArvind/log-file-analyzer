'''
This module provides a function to analyze log file.
'''

from model import LogEntry
import os
import json
import concurrent.futures
from pydantic import BaseModel

class LogAnalysis(BaseModel):
    """
    LogAnalysis
    A model representing the analysis of log entries.
    """
    
    successful_entries: list = []
    failed_entries: list = []
    service_entries: dict = {}
    log_level_entries: dict = {} 

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
    
def log_results_decorator(func):
    """
    Decorator to capture successful and failed entries into separate JSON files.
    """
    def wrapper(*args, **kwargs):
        successful_entries = []
        failed_entries = []
        
        for result in func(*args, **kwargs):
            if isinstance(result, dict):
                successful_entries.append(result)
            else:
                failed_entries.append(result)
        
        # Combine successful and failed entries into a single dictionary
        combined_entries = {
            "successful_entries": successful_entries,
            "failed_entries": failed_entries
        }


        
        # Dump the combined entries to a single JSON file
        dump_to_json(combined_entries, "./output/combined_entries.json")
        
        return successful_entries  # Return only successful entries for further processing
    
    return wrapper

@log_results_decorator
def process_logs(log_file_path):
    """
    Process log lines and return the results.
    Validate if all processes were successful.
    """
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(parse_log_line, line): line for line in read_log_file(log_file_path)}
        results = [future.result() for future in futures]
        
        # Check if all processes were successful
        all_successful = all(isinstance(result, dict) for result in results)
        if not all_successful:
            print("Warning: Not all log lines were processed successfully.")
        print("Processing complete.")
        return results
