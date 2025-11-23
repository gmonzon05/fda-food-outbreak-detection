"""
FDA Food Outbreak Detection System

A time series analysis and anomaly detection system for identifying 
potential foodborne illness outbreaks using FDA adverse event data.
"""

__version__ = "0.1.0"
__author__ = "Gregory Monzon"

from .data_loader import (
    FDADataLoader,
    parse_date,
    load_and_prepare_timeseries_data
)

__all__ = [
    'FDADataLoader',
    'parse_date',
    'load_and_prepare_timeseries_data'
]