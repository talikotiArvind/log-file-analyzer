'''
This module defines the data model for log entries using Pydantic.
'''

from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class LogEntry(BaseModel):
    """
    LogEntry
    A model representing a single log entry with details about the timestamp, service name, log level, and message.
    Attributes:
        date_time (datetime): Timestamp of the log in the format YYYY-MM-DD HH:MM:SS.
        service_name (str): Name of the service generating the log.
        log_level (Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]): 
            Log level indicating the severity of the log. Possible values are:
            - DEBUG
            - INFO
            - WARNING
            - ERROR
            - CRITICAL
        message (str): The actual log message content.
    """
    
    date_time: str = Field(..., description="Timestamp of the log in format YYYY-MM-DD HH:MM:SS")
    service_name: str = Field(..., description="Name of the service generating the log")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        ..., description="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    message: str = Field(..., description="The actual log message")
