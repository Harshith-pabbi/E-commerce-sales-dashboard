import pytest
import pandas as pd
import numpy as np
from src.process_data import clean_data

@pytest.fixture
def mock_raw_data():
    data = {
        'transaction_id': ['TRX-1', 'TRX-2', 'TRX-3', 'TRX-4', np.nan],
        'date': ['2023-01-01', '2023-01-02', '2023-01-03', '2023-01-04', '2023-01-05'],
        'product_id': ['P1', 'P2', 'P3', 'P4', 'P5'],
        'category': ['C1', 'C2', 'C1', 'C3', 'C1'],
        'region': ['R1', 'R2', 'R1', 'R3', 'R2'],
        'quantity': [5, -2, 10, 0, 5],
        'unit_price': [10.0, 20.0, -5.0, 15.0, 10.0],
        'discount': [0.1, 0.0, 0.2, 1.5, 0.0], # 1.5 is > 1.0 (invalid)
        'revenue': [45.0, -40.0, -40.0, 0.0, 50.0],
        'profit': [15.0, -10.0, -10.0, 0.0, 15.0]
    }
    return pd.DataFrame(data)

def test_clean_data_drops_missing(mock_raw_data):
    cleaned = clean_data(mock_raw_data)
    # The last row has NaN in transaction_id, so it should be dropped
    assert 'TRX-5' not in cleaned['transaction_id'].values
    assert len(cleaned) < len(mock_raw_data)

def test_clean_data_handles_negative_values(mock_raw_data):
    cleaned = clean_data(mock_raw_data)
    # Row 2 has negative quantity, Row 3 has negative unit_price
    assert (cleaned['quantity'] > 0).all()
    assert (cleaned['unit_price'] > 0).all()

def test_clean_data_handles_invalid_discounts(mock_raw_data):
    cleaned = clean_data(mock_raw_data)
    # Row 4 has discount 1.5
    assert (cleaned['discount'] <= 1.0).all()

def test_clean_data_adds_features(mock_raw_data):
    cleaned = clean_data(mock_raw_data)
    expected_cols = ['year_month', 'month', 'day_of_week', 'is_weekend', 'calculated_revenue']
    for col in expected_cols:
        assert col in cleaned.columns

def test_clean_data_types(mock_raw_data):
    cleaned = clean_data(mock_raw_data)
    assert pd.api.types.is_datetime64_any_dtype(cleaned['date'])
