"""
download_data.py - Data Ingestion and Verification for Indian Economic Datasets.

Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

Official Data Sources:
    1. Reserve Bank of India (RBI) - Handbook of Statistics on Indian States
       Table: Per Capita Net State Domestic Product at Constant (2011-12) Prices
       Portal: https://dbie.rbi.org.in
    2. Ministry of Statistics and Programme Implementation (MoSPI)
       National Accounts Statistics - State Domestic Product series
       Portal: https://www.mospi.gov.in

Note on Academic Integrity:
    This project strictly avoids fabricating economic figures. Real datasets
    from official statistical agencies must be placed in `data/raw/`.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional

try:
    from python.utils import get_pipeline_paths, print_step_banner
except ImportError:
    from utils import get_pipeline_paths, print_step_banner

RAW_DATA_FILENAME = "per_capita_nsdp_constant_2011_12.csv"
METADATA_FILENAME = "dataset_provenance.json"


def get_official_sources_info() -> Dict[str, Any]:
    """
    Returns verified metadata and provenance information for the official
    datasets required to answer the research question.
    """
    return {
        "project_title": "An Economic Data Pipeline: Indian State-wise Per-Capita Income Divergence",
        "research_question": "How has state-wise per-capita income diverged in India since 2011?",
        "base_year": "2011-12",
        "metric": "Per Capita Net State Domestic Product (NSDP) at Constant (2011-12) Prices in Indian Rupees (INR)",
        "sources": [
            {
                "institution": "Reserve Bank of India (RBI)",
                "publication": "Handbook of Statistics on Indian States",
                "table_name": "Per Capita Net State Domestic Product - Constant Prices (Base 2011-12)",
                "url": "https://dbie.rbi.org.in",
                "notes": "Annual publication reporting state domestic product and per capita statistics."
            },
            {
                "institution": "Ministry of Statistics and Programme Implementation (MoSPI)",
                "division": "National Accounts Division (NAD)",
                "table_name": "State Domestic Product and Per Capita Income Series",
                "url": "https://www.mospi.gov.in",
                "notes": "Primary official statistical authority of the Government of India."
            }
        ],
        "expected_columns": [
            "State",
            "Financial_Year",
            "Per_Capita_NSDP_INR"
        ],
        "time_horizon": "2011-12 to present (or latest available fiscal year)"
    }


def save_metadata_manifest(manifest_path: Optional[Path] = None) -> Path:
    """
    Saves the data source provenance manifest to data/raw/ for reproducibility.
    
    Args:
        manifest_path (Optional[Path]): Destination path. If None, defaults to data/raw/dataset_provenance.json.
        
    Returns:
        Path: Path to the saved manifest file.
    """
    paths = get_pipeline_paths()
    target_path = manifest_path or (paths["data_raw"] / METADATA_FILENAME)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    info = get_official_sources_info()
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=4)
        
    print(f"[METADATA] Provenance manifest written to: {target_path.name}")
    return target_path


def check_raw_dataset_exists(filename: str = RAW_DATA_FILENAME) -> bool:
    """
    Checks if the raw dataset file exists in data/raw/.
    
    Args:
        filename (str): Name of the raw data file.
        
    Returns:
        bool: True if file exists and is not empty, False otherwise.
    """
    paths = get_pipeline_paths()
    raw_file = paths["data_raw"] / filename
    
    if not raw_file.exists():
        return False
    if raw_file.stat().st_size == 0:
        print(f"[WARNING] Raw data file found but it is empty (0 bytes): {raw_file.name}")
        return False
    return True


def display_download_instructions(filename: str = RAW_DATA_FILENAME) -> None:
    """
    Prints a clear, student-friendly step-by-step guide explaining how
    to obtain and place the real Indian economic dataset.
    """
    paths = get_pipeline_paths()
    raw_dir = paths["data_raw"]
    
    instructions = f"""
======================================================================
 DATA ACQUISITION GUIDE: State-wise Per-Capita Income (Post-2011)
======================================================================
To answer our research question on economic divergence, follow these steps
to obtain the official Government of India / RBI economic series:

Step 1: Visit the official RBI DBIE Portal:
        https://dbie.rbi.org.in
        Navigate to: 'Handbook of Statistics on Indian States'
        Select: 'Social and Demographic Indicators' -> 'Per Capita Net State Domestic Product - Constant Prices'

Step 2: Alternatively, visit MoSPI portal:
        https://www.mospi.gov.in (National Accounts Division)
        Download: NSDP Per Capita at Constant (2011-12) Prices.

Step 3: Save the downloaded file as a CSV or Excel file named:
        {filename}

Step 4: Place the file into your raw data directory:
        Folder: {raw_dir}

Step 5: Expected Data Structure:
        - Column 1: State / Union Territory name
        - Column 2: Financial Year (e.g., '2011-12', '2012-13', ..., '2022-23')
        - Column 3: Per Capita NSDP at 2011-12 prices (INR)

Once placed, re-run the pipeline to clean, analyze, and visualize divergence!
======================================================================
"""
    print(instructions)


def run_data_ingestion_check() -> bool:
    """
    Primary workflow function for Step 1 of the pipeline.
    Checks availability of raw data, logs provenance, and guides the student.
    
    Returns:
        bool: True if raw data is ready for processing, False if manual placement is awaited.
    """
    print_step_banner(
        step_number=1,
        step_name="Data Ingestion & Source Verification",
        description="Verify raw economic datasets and write provenance manifest."
    )
    
    # 1. Always record official provenance metadata
    save_metadata_manifest()
    
    # 2. Check if the actual dataset is present
    has_data = check_raw_dataset_exists(RAW_DATA_FILENAME)
    if has_data:
        paths = get_pipeline_paths()
        target = paths["data_raw"] / RAW_DATA_FILENAME
        size_kb = target.stat().st_size / 1024
        print(f"[SUCCESS] Raw dataset found: {RAW_DATA_FILENAME} ({size_kb:.2f} KB)")
        return True
    else:
        print(f"[INFO] Raw dataset '{RAW_DATA_FILENAME}' is not yet in data/raw/.")
        display_download_instructions(RAW_DATA_FILENAME)
        return False


if __name__ == "__main__":
    status = run_data_ingestion_check()
    print(f"\nData check status: {'Ready for cleaning' if status else 'Awaiting raw data file'}")
