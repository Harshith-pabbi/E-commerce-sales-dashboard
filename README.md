# E-Commerce Sales Analytics Dashboard

## Overview
This project processes and analyzes 50,000+ transactional records to identify monthly revenue trends, seasonal sales spikes, and key performance metrics including Top-10 product rankings and regional profit analysis. The final output is an interactive dashboard tracking vital KPIs.

## Project Structure
- `data/`: Contains raw and processed data.
- `notebooks/`: Jupyter Notebooks for data exploration and trend analysis.
- `src/`: Core Python modules for data processing, metrics calculation, and plotting.
- `dashboard/`: Application file for the interactive dashboard.
- `outputs/`: Generated figures and analytical reports.

## Setup Instructions
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place your raw data inside the `data/raw/` directory.
3. Run the data processing notebooks or scripts to generate the cleaned dataset in `data/processed/`.
4. Launch the dashboard (if using Streamlit):
   ```bash
   streamlit run dashboard/app.py
   ```
