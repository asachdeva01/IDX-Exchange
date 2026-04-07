import pandas as pd


def missing_value_report(df: pd.DataFrame, dataset_name: str = "Dataset") -> pd.DataFrame:
    """Generate a missing value report showing count and percentage for columns with nulls.

    Returns a DataFrame sorted by missing percentage (descending), filtered to only
    columns that have at least one missing value.
    """
    missing_count = df.isnull().sum()
    missing_pct = (missing_count / len(df) * 100).round(2)

    report = pd.DataFrame({
        'Missing Count': missing_count,
        'Missing %': missing_pct
    }).query('`Missing Count` > 0').sort_values('Missing %', ascending=False)

    print(f"=== {dataset_name}: {len(report)} columns with missing values ===")
    print(report)
    return report
