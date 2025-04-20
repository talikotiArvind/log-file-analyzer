'''
This module provides a function to analyze log file.
'''

import concurrent.futures
from utilities import log_results_decorator, parse_log_line, read_log_file

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
            print("LOG File parse status successful :: Warning: Not all log lines were processed successfully.")
        else:
            print("LOG File parse status successful :: All log entries were processed successfully.")
        return results
