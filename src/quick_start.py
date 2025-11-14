#!/usr/bin/env python3
"""
Quick Start Script for FDA Food Outbreak Detection

This script demonstrates basic usage of the data loader and performs
a quick sanity check on the data.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from data_loader import FDADataLoader, parse_date


def main():
    """Run quick start demo"""
    
    print("="*70)
    print("FDA FOOD OUTBREAK DETECTION - QUICK START")
    print("="*70)
    
    # Check if data file exists
    data_path = Path("data/raw/food-event-0001-of-0001.json")
    
    if not data_path.exists():
        print("\n❌ ERROR: Data file not found!")
        print(f"   Expected location: {data_path}")
        print("\n📥 Please download the data file from:")
        print("   https://open.fda.gov/apis/food/event/download/")
        print("\n   Place it in: data/raw/food-event-0001-of-0001.json")
        return
    
    print(f"\n✅ Data file found: {data_path}")
    print(f"   File size: {data_path.stat().st_size / (1024**2):.1f} MB")
    
    # Load metadata
    print("\n" + "-"*70)
    print("LOADING METADATA...")
    print("-"*70)
    
    loader = FDADataLoader(str(data_path))
    meta = loader.load_metadata()
    
    print(f"Last Updated: {meta.get('last_updated', 'N/A')}")
    print(f"Total Records: {meta.get('results', {}).get('total', 'N/A'):,}")
    
    # Load sample data
    print("\n" + "-"*70)
    print("LOADING SAMPLE DATA (1000 records)...")
    print("-"*70)
    
    df = loader.load_to_dataframe(max_records=1000)
    
    print(f"\n✅ Successfully loaded {len(df)} records")
    print(f"\nDataFrame shape: {df.shape}")
    print(f"Columns: {len(df.columns)}")
    
    # Basic statistics
    print("\n" + "-"*70)
    print("BASIC STATISTICS")
    print("-"*70)
    
    print(f"\nRecords with valid date_started: {df['date_started'].notna().sum()} "
          f"({df['date_started'].notna().sum()/len(df)*100:.1f}%)")
    
    print(f"Records with consumer age: {df['consumer_age'].notna().sum()} "
          f"({df['consumer_age'].notna().sum()/len(df)*100:.1f}%)")
    
    print(f"Records with consumer gender: {df['consumer_gender'].notna().sum()} "
          f"({df['consumer_gender'].notna().sum()/len(df)*100:.1f}%)")
    
    # Sample records
    print("\n" + "-"*70)
    print("SAMPLE RECORDS")
    print("-"*70)
    print("\nFirst 3 records:")
    print(df[['report_number', 'date_started', 'reactions', 'outcomes']].head(3).to_string())
    
    # Next steps
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("\n1. Open the exploration notebook:")
    print("   jupyter notebook notebooks/01_exploration.ipynb")
    print("\n2. Review the README.md for detailed documentation")
    print("\n3. Check requirements.txt for all dependencies")
    print("\n" + "="*70)
    print("Setup complete! 🎉")
    print("="*70 + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nPlease check that:")
        print("1. The data file is in the correct location")
        print("2. All dependencies are installed (pip install -r requirements.txt)")
        sys.exit(1)