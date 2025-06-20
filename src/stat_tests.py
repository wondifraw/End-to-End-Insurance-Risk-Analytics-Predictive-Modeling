import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, chi2_contingency

# --- Metrics ---
def claim_frequency(df, group_col=None):
    if group_col:
        return df.groupby(group_col).apply(lambda x: (x['TotalClaims'] > 0).mean())
    return (df['TotalClaims'] > 0).mean()

def claim_severity(df, group_col=None):
    if group_col:
        return df[df['TotalClaims'] > 0].groupby(group_col)['TotalClaims'].mean()
    return df[df['TotalClaims'] > 0]['TotalClaims'].mean()

def margin(df, group_col=None):
    if group_col:
        return df.groupby(group_col).apply(lambda x: (x['TotalPremium'] - x['TotalClaims']).mean())
    return (df['TotalPremium'] - df['TotalClaims']).mean()

# --- Segmentation ---
def ab_split(df, feature, group_a, group_b):
    return df[df[feature].isin([group_a, group_b])], group_a, group_b

# --- Statistical Tests ---
def t_test_metric(df, feature, group_a, group_b, metric_func):
    ab_df, a, b = ab_split(df, feature, group_a, group_b)
    group_a_vals = metric_func(ab_df[ab_df[feature] == a])
    group_b_vals = metric_func(ab_df[ab_df[feature] == b])
    stat, p = ttest_ind(group_a_vals, group_b_vals, equal_var=False, nan_policy='omit')
    return stat, p

def chi2_test(df, feature, target):
    contingency = pd.crosstab(df[feature], df[target])
    stat, p, _, _ = chi2_contingency(contingency)
    return stat, p

# --- Main Hypothesis Testing ---
def run_all_hypothesis_tests(df):
    results = {}
    # 1. Province risk difference (claim frequency)
    provinces = df['Province'].dropna().unique()
    if len(provinces) >= 2:
        stat, p = t_test_metric(df, 'Province', provinces[0], provinces[1], lambda d: (d['TotalClaims'] > 0).astype(int))
        results['province_risk'] = {'stat': stat, 'p': p, 'groups': (provinces[0], provinces[1])}
    # 2. Zip code risk difference (claim frequency)
    zips = df['PostalCode'].dropna().unique()
    if len(zips) >= 2:
        stat, p = t_test_metric(df, 'PostalCode', zips[0], zips[1], lambda d: (d['TotalClaims'] > 0).astype(int))
        results['zip_risk'] = {'stat': stat, 'p': p, 'groups': (zips[0], zips[1])}
    # 3. Zip code margin difference
    if len(zips) >= 2:
        stat, p = t_test_metric(df, 'PostalCode', zips[0], zips[1], lambda d: d['TotalPremium'] - d['TotalClaims'])
        results['zip_margin'] = {'stat': stat, 'p': p, 'groups': (zips[0], zips[1])}
    # 4. Gender risk difference (claim frequency)
    genders = df['Gender'].dropna().unique()
    if len(genders) >= 2:
        stat, p = t_test_metric(df, 'Gender', genders[0], genders[1], lambda d: (d['TotalClaims'] > 0).astype(int))
        results['gender_risk'] = {'stat': stat, 'p': p, 'groups': (genders[0], genders[1])}
    return results 