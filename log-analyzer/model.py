'''
This module defines the data model for log entries using Pydantic.
'''

from pydantic import BaseModel, Field
from typing import Literal

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
    
    date_time: str = Field(
        ..., 
        description="Timestamp of the log in format YYYY-MM-DD HH:MM:SS",
        pattern=r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$",
    )
    service_name: str = Field(
        ..., 
        pattern=r"^Service[A-Z]$", 
        description="Name of the service generating the log, must be in format ServiceA, ServiceB, ServiceC, etc."
    )
    log_level: Literal["INFO", "WARN", "ERROR", "DEBUG"] = Field(
        ..., description="Log level: DEBUG, INFO, WARNING, ERROR, CRITICAL"
    )
    message: str = Field(..., description="The actual log message")
