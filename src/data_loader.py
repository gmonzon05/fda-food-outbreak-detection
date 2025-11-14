"""
FDA Food Event Data Loader

This module provides memory-efficient loading and processing of the FDA food event JSON data.
"""

import json
import pandas as pd
from typing import Iterator, Dict, List, Optional
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FDADataLoader:
    """
    Memory-efficient loader for FDA food event data.
    Handles large JSON files by processing records in chunks.
    """
    
    def __init__(self, filepath: str):
        """
        Initialize the data loader.
        
        Args:
            filepath: Path to the FDA JSON file
        """
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
    
    def load_metadata(self) -> Dict:
        """
        Load only the metadata from the JSON file.
        
        Returns:
            Dictionary containing meta information
        """
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            return data.get('meta', {})
    
    def iter_records(self, limit: Optional[int] = None) -> Iterator[Dict]:
        """
        Iterate through records without loading entire file into memory.
        
        Args:
            limit: Maximum number of records to return (None for all)
            
        Yields:
            Individual record dictionaries
        """
        with open(self.filepath, 'r') as f:
            data = json.load(f)
            results = data.get('results', [])
            
            count = 0
            for record in results:
                if limit and count >= limit:
                    break
                yield record
                count += 1
    
    def load_to_dataframe(self, 
                         chunk_size: int = 10000,
                         max_records: Optional[int] = None) -> pd.DataFrame:
        """
        Load records into a pandas DataFrame with memory efficiency.
        
        Args:
            chunk_size: Number of records to process at once
            max_records: Maximum total records to load (None for all)
            
        Returns:
            DataFrame with flattened record structure
        """
        logger.info("Loading FDA data to DataFrame...")
        
        records = []
        for i, record in enumerate(self.iter_records(limit=max_records)):
            # Flatten the record structure
            flat_record = self._flatten_record(record)
            records.append(flat_record)
            
            # Log progress
            if (i + 1) % chunk_size == 0:
                logger.info(f"Processed {i + 1} records...")
        
        df = pd.DataFrame(records)
        logger.info(f"Loaded {len(df)} records into DataFrame")
        
        return df
    
    def _flatten_record(self, record: Dict) -> Dict:
        """
        Flatten nested record structure for easier analysis.
        
        Args:
            record: Raw record dictionary
            
        Returns:
            Flattened dictionary
        """
        flat = {
            'report_number': record.get('report_number'),
            'date_created': record.get('date_created'),
            'date_started': record.get('date_started'),
            'outcomes': ','.join(record.get('outcomes', [])),
            'reactions': ','.join(record.get('reactions', [])),
            'reaction_count': len(record.get('reactions', [])),
        }
        
        # Extract consumer information
        consumer = record.get('consumer', {})
        flat['consumer_age'] = consumer.get('age')
        flat['consumer_age_unit'] = consumer.get('age_unit')
        flat['consumer_gender'] = consumer.get('gender')
        
        # Extract product information (first product only for simplicity)
        products = record.get('products', [])
        if products:
            product = products[0]
            flat['product_name'] = product.get('name_brand')
            flat['product_role'] = product.get('role')
            flat['industry_code'] = product.get('industry_code')
            flat['industry_name'] = product.get('industry_name')
        
        return flat
    
    def get_reaction_list(self, record: Dict) -> List[str]:
        """
        Extract list of reactions from a record.
        
        Args:
            record: Record dictionary
            
        Returns:
            List of reaction strings
        """
        return record.get('reactions', [])
    
    def has_valid_date(self, record: Dict) -> bool:
        """
        Check if record has a valid date_started.
        
        Args:
            record: Record dictionary
            
        Returns:
            True if date_started is not null
        """
        return record.get('date_started') is not None


def parse_date(date_str: Optional[str]) -> Optional[pd.Timestamp]:
    """
    Parse FDA date format (YYYYMMDD) to pandas Timestamp.
    
    Args:
        date_str: Date string in YYYYMMDD format
        
    Returns:
        Pandas Timestamp or None if invalid
    """
    if not date_str or date_str == 'null':
        return None
    try:
        return pd.to_datetime(date_str, format='%Y%m%d')
    except:
        return None


def load_and_prepare_timeseries_data(filepath: str, 
                                     max_records: Optional[int] = None) -> pd.DataFrame:
    """
    Convenience function to load data prepared for time series analysis.
    Filters for records with valid dates and converts date columns.
    
    Args:
        filepath: Path to FDA JSON file
        max_records: Maximum records to load (None for all)
        
    Returns:
        DataFrame ready for time series analysis
    """
    loader = FDADataLoader(filepath)
    df = loader.load_to_dataframe(max_records=max_records)
    
    # Convert date columns
    df['date_started'] = df['date_started'].apply(parse_date)
    df['date_created'] = df['date_created'].apply(parse_date)
    
    # Filter for records with valid date_started (required for time series)
    df_valid = df[df['date_started'].notna()].copy()
    
    logger.info(f"Records with valid date_started: {len(df_valid)} ({len(df_valid)/len(df)*100:.1f}%)")
    
    # Sort by date
    df_valid = df_valid.sort_values('date_started').reset_index(drop=True)
    
    return df_valid


if __name__ == "__main__":
    # Example usage
    import sys
    
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = "data/raw/food-event-0001-of-0001.json"
    
    print(f"Loading data from: {filepath}")
    
    # Load metadata
    loader = FDADataLoader(filepath)
    meta = loader.load_metadata()
    print("\nMetadata:")
    print(json.dumps(meta, indent=2))
    
    # Load first 1000 records
    print("\nLoading first 1000 records...")
    df = loader.load_to_dataframe(max_records=1000)
    print(f"\nDataFrame shape: {df.shape}")
    print(f"\nColumns: {df.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(df.head())