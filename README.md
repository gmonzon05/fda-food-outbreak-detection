# FDA Food Outbreak Detection System

A time series analysis and anomaly detection system for identifying potential foodborne illness outbreaks using FDA adverse event report data.

## 🎯 Project Goal

Identify unusual spikes in specific food-related adverse reactions over time to detect potential outbreaks before official recalls are issued, using statistical and machine learning techniques.

## 📊 Dataset

This project uses the FDA openFDA food adverse event reports dataset, which contains consumer-reported illnesses and injuries related to food products.

- **Source**: [FDA openFDA](https://open.fda.gov/)
- **File**: `food-event-0001-of-0001.json`
- **Size**: ~2.6M+ records
- **Fields**: Report number, reactions, outcomes, dates, consumer demographics, product information

### ⚠️ Data Disclaimer

This dataset contains consumer-submitted reports and has not been scientifically verified. Per FDA guidelines:
- Do not rely on this data for medical decisions
- Reports do not constitute proof that a product caused an event
- Cannot be used to estimate incidence rates or risk

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- pip or conda for package management

### Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/fda-food-outbreak-detection.git
cd fda-food-outbreak-detection
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download the FDA data:
   - Visit [FDA openFDA Downloads](https://open.fda.gov/apis/food/event/download/)
   - Place `food-event-0001-of-0001.json` in `data/raw/`

### Quick Start

1. **Explore the data**:
```bash
jupyter notebook notebooks/01_exploration.ipynb
```

2. **Run data loader**:
```python
from src.data_loader import FDADataLoader

loader = FDADataLoader('data/raw/food-event-0001-of-0001.json')
df = loader.load_to_dataframe(max_records=10000)
```

## 📁 Project Structure

```
fda-food-outbreak-detection/
├── data/
│   ├── raw/              # Original FDA JSON file (not tracked)
│   ├── processed/        # Cleaned/transformed data
│   └── README.md         # Data documentation
├── notebooks/
│   ├── 01_exploration.ipynb      # Data exploration
│   ├── 02_preprocessing.ipynb    # Data preparation
│   └── 03_modeling.ipynb         # Anomaly detection
├── src/
│   ├── __init__.py
│   ├── data_loader.py            # Efficient data loading utilities
│   ├── preprocessing.py          # Data cleaning and feature engineering
│   ├── time_series.py            # Time series processing
│   └── anomaly_detection.py      # Anomaly detection models
├── tests/                         # Unit tests
├── results/
│   ├── figures/                  # Generated plots
│   └── models/                   # Saved models
├── .gitignore
├── requirements.txt
├── README.md
└── LICENSE
```

## 🔬 Methodology

### 1. Time Series Analysis
- Aggregate adverse reaction counts by time period (daily/weekly)
- Identify temporal patterns and seasonality
- Focus on most common reactions (e.g., vomiting, diarrhea, nausea)

### 2. Anomaly Detection Techniques

**Statistical Methods**:
- Moving average with standard deviation thresholds
- Z-score based detection
- Seasonal decomposition (STL)

**Machine Learning**:
- Isolation Forest for multivariate anomaly detection
- ARIMA residual analysis
- Prophet for time series forecasting with anomaly detection

### 3. Validation
- Compare detected anomalies with known FDA recalls
- Temporal alignment of spikes with outbreak events
- False positive rate analysis

## 📈 Key Features

- **Memory-efficient data loading** for large JSON files
- **Flexible aggregation** by reaction type and time period
- **Multiple anomaly detection algorithms** for comparison
- **Visualization tools** for time series and anomaly presentation
- **Modular code structure** for easy extension

## 🎨 Sample Visualizations

The exploration notebook generates:
- Temporal distribution of adverse events
- Top reactions and their frequencies
- Outcome severity distributions
- Time series plots for individual reactions
- Consumer demographic analysis

## 🔜 Roadmap

- [ ] Complete data exploration (in progress)
- [ ] Build preprocessing pipeline
- [ ] Implement baseline statistical models
- [ ] Develop Isolation Forest anomaly detector
- [ ] Create ARIMA-based detection
- [ ] Build interactive dashboard
- [ ] Validate against historical recalls
- [ ] Deploy as web application

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- FDA openFDA initiative for providing open access to this data
- Anthropic's Claude for assistance with project development

## 📧 Contact

For questions or collaboration opportunities, please open an issue on GitHub.

---

**Note**: This is an educational/research project. Any findings should be verified with official sources before taking action.