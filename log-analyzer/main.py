from log_analyzer import process_logs

if __name__ == "__main__":
    # Apply the decorator and process logs
    LOG_FILE_PATH = "app.log"  # Path to the log file
    processed_logs = process_logs(LOG_FILE_PATH)