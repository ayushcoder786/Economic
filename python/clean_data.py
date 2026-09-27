"""
clean_data.py - Data Cleaning and Harmonization Pipeline for Indian State Incomes.

This module processes raw economic data tables from RBI / MoSPI into a tidy,
analysis-ready dataset.

Key Cleaning Responsibilities:
1. Harmonize state/UT naming across historical variations (e.g. 'Orissa' -> 'Odisha').
2. Strip footnote annotations common in RBI/MoSPI data (e.g. '*', '(P)', '(Q)', '(RE)').
3. Reshape wide tables (states as rows, years as columns) into tidy long format.
4. Clean currency values, removing Indian comma formatting and non-numeric characters.
5. Standardize financial years (e.g. '2011-12' with base start year 2011).
6. Save processed dataset to `data/processed/`.
"""

import re
from pathlib import Path
from typing import Dict, List, Optional, Any
import pandas as pd

try:
    from python.utils import get_pipeline_paths, print_step_banner
except ImportError:
    from utils import get_pipeline_paths, print_step_banner

# Official standard names for Indian States & Major Union Territories
STATE_NAME_MAPPINGS: Dict[str, str] = {
    "orissa": "Odisha",
    "uttaranchal": "Uttarakhand",
    "pondicherry": "Puducherry",
    "jammu & kashmir": "Jammu and Kashmir",
    "andaman & nicobar islands": "Andaman and Nicobar Islands",
    "dadra & nagar haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "daman & diu": "Dadra and Nagar Haveli and Daman and Diu",
    "dadra and nagar haveli and daman and diu": "Dadra and Nagar Haveli and Daman and Diu",
    "delhi": "NCT of Delhi",
    "nct of delhi": "NCT of Delhi",
    "all-india": "All India",
    "all india": "All India",
}


def sanitize_text(text: str) -> str:
    """
    Strips whitespace and removes footnote markers common in Indian statistical tables.
    Example: 'Odisha*' -> 'Odisha', '2019-20 (P)' -> '2019-20'
    """
    if not isinstance(text, str):
        return text
    # Remove footnote markers: *, #, and parenthetical status codes like (P), (Q), (A), (RE)
    cleaned = re.sub(r"[\*#]+", "", text)
    cleaned = re.sub(r"\s*\((P|Q|A|RE|QE|PE)\)", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def standardize_state_name(raw_name: str) -> str:
    """
    Maps historical or non-standard state names to the official Survey of India standard.
    
    Args:
        raw_name (str): Original state name from raw table.
        
    Returns:
        str: Standardized state name.
    """
    cleaned = sanitize_text(str(raw_name))
    lookup_key = cleaned.lower()
    return STATE_NAME_MAPPINGS.get(lookup_key, cleaned)


def clean_currency_value(val: Any) -> Optional[float]:
    """
    Parses currency values, handling Indian comma separators (e.g., '1,25,000')
    and common statistical missing value indicators (e.g., '-', 'NA', '..').
    
    Args:
        val: Raw cell value.
        
    Returns:
        Optional[float]: Numeric float or None if missing.
    """
    if pd.isna(val):
        return None
    val_str = str(val).strip()
    if val_str in ["-", "--", "NA", "N.A.", "..", "", "null", "None"]:
        return None
    
    # Strip any footnote characters and commas
    val_clean = re.sub(r"[^\d\.]", "", val_str)
    try:
        return float(val_clean)
    except ValueError:
        return None


def reshape_wide_to_long(df: pd.DataFrame, id_col: str = "State") -> pd.DataFrame:
    """
    Converts wide-format state economic tables (where columns are years)
    into tidy long-format required for econometric panel analysis.
    
    Args:
        df (pd.DataFrame): Wide DataFrame.
        id_col (str): Column name identifying the state/region.
        
    Returns:
        pd.DataFrame: Reshaped DataFrame with columns [State, Financial_Year, Per_Capita_NSDP_INR].
    """
    # Identify year columns (e.g. matching '2011-12' or '2011')
    year_cols = [c for c in df.columns if c != id_col]
    
    melted = df.melt(
        id_vars=[id_col],
        value_vars=year_cols,
        var_name="Financial_Year",
        value_name="Per_Capita_NSDP_INR"
    )
    return melted


def parse_start_year_from_financial_year(fy_str: str) -> Optional[int]:
    """
    Extracts the base starting calendar year from an Indian financial year string.
    Example: '2011-12' -> 2011, '2018-19' -> 2018.
    """
    match = re.search(r"(\d{4})", str(fy_str))
    if match:
        return int(match.group(1))
    return None


def clean_nsdp_dataframe(raw_df: pd.DataFrame) -> pd.DataFrame:
    """
    Core data transformation pipeline applied to the loaded raw DataFrame.
    
    Validates structure, cleans labels, parses numeric per-capita incomes,
    and returns a standardized long-format DataFrame.
    """
    df = raw_df.copy()
    
    # Standardize column headers
    df.columns = [sanitize_text(str(c)) for c in df.columns]
    
    # Locate the state column (often named State, State/UT, Region, etc.)
    state_col_candidates = [c for c in df.columns if "state" in c.lower() or "u.t" in c.lower() or "region" in c.lower()]
    if state_col_candidates:
        primary_state_col = state_col_candidates[0]
        df = df.rename(columns={primary_state_col: "State"})
    elif "State" not in df.columns:
        # Default to first column if no explicit match
        df = df.rename(columns={df.columns[0]: "State"})
        
    # Check if wide format or long format
    is_already_long = ("Financial_Year" in df.columns or "Year" in df.columns) and len(df.columns) <= 4
    
    if not is_already_long:
        df = reshape_wide_to_long(df, id_col="State")
    else:
        # Rename year column if necessary
        for y_col in ["Year", "FY", "financial_year"]:
            if y_col in df.columns:
                df = df.rename(columns={y_col: "Financial_Year"})
        for v_col in ["NSDP", "Per_Capita_Income", "Income", "value"]:
            if v_col in df.columns:
                df = df.rename(columns={v_col: "Per_Capita_NSDP_INR"})

    # Standardize state names and clean financial years
    df["State"] = df["State"].apply(standardize_state_name)
    df["Financial_Year"] = df["Financial_Year"].apply(sanitize_text)
    df["Year_Start"] = df["Financial_Year"].apply(parse_start_year_from_financial_year)
    
    # Clean numeric values
    df["Per_Capita_NSDP_INR"] = df["Per_Capita_NSDP_INR"].apply(clean_currency_value)
    
    # Drop rows where state name is empty or a table footnote line
    df = df.dropna(subset=["State", "Financial_Year"])
    df = df[~df["State"].str.lower().str.contains("source|note|footnote|compounded|average", na=False)]
    
    # Sort for deterministic panel layout
    df = df.sort_values(by=["State", "Year_Start"]).reset_index(drop=True)
    
    return df


def process_raw_dataset(
    input_filename: str = "per_capita_nsdp_constant_2011_12.csv",
    output_filename: str = "per_capita_nsdp_cleaned.csv"
) -> Optional[Path]:
    """
    Loads raw dataset from data/raw/, applies the cleaning pipeline,
    and writes the tidy dataset to data/processed/.
    
    Returns:
        Optional[Path]: Path to saved cleaned file, or None if raw file was missing.
    """
    paths = get_pipeline_paths()
    input_path = paths["data_raw"] / input_filename
    output_path = paths["data_processed"] / output_filename
    
    if not input_path.exists():
        print(f"[SKIP] Raw file not found: {input_path}")
        print(f"       Place the raw data in data/raw/{input_filename} to run full cleaning.")
        return None
        
    print(f"[CLEAN] Reading raw data from: {input_path.name}")
    try:
        if input_path.suffix.lower() in [".xlsx", ".xls"]:
            raw_df = pd.read_excel(input_path)
        else:
            raw_df = pd.read_csv(input_path)
    except Exception as e:
        print(f"[ERROR] Failed to read raw data file: {e}")
        return None
        
    cleaned_df = clean_nsdp_dataframe(raw_df)
    
    # Ensure processed directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cleaned_df.to_csv(output_path, index=False, encoding="utf-8")
    
    print(f"[SUCCESS] Cleaned data saved: {output_path.name}")
    print(f"          Records: {len(cleaned_df)}, States/UTs: {cleaned_df['State'].nunique()}, Years: {cleaned_df['Financial_Year'].nunique()}")
    return output_path


def run_cleaning_step() -> bool:
    """
    Entry point for Step 2 of the pipeline.
    """
    print_step_banner(
        step_number=2,
        step_name="Data Cleaning & Harmonization",
        description="Transform raw RBI/MoSPI tables into tidy panel format with standardized state names."
    )
    result = process_raw_dataset()
    return result is not None


if __name__ == "__main__":
    run_cleaning_step()
