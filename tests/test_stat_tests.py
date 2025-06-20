import pandas as pd
from src.stat_tests import run_all_hypothesis_tests

def test_run_all_hypothesis_tests():
    data = {
        'Province': ['A', 'A', 'B', 'B'],
        'PostalCode': [1, 1, 2, 2],
        'Gender': ['M', 'F', 'M', 'F'],
        'TotalPremium': [100, 120, 110, 130],
        'TotalClaims': [0, 1, 0, 1]
    }
    df = pd.DataFrame(data)
    results = run_all_hypothesis_tests(df)
    assert isinstance(results, dict)
    assert 'province_risk' in results
    assert 'gender_risk' in results 