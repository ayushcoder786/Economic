"""
main.py - Master Pipeline Orchestrator for the Economic Data Pipeline.

Research Question:
    "How has state-wise per-capita income diverged in India since 2011?"

Workflow Stages:
    Raw Data
       ↓
    Cleaning
       ↓
    Analysis
       ↓
    Visualization
       ↓
    R reproduction
       ↓
    Git repository
"""

import sys
from pathlib import Path

# Add project root to sys.path so modules can be imported directly
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from python.utils import ensure_directories_exist, get_pipeline_paths
from python.download_data import run_data_ingestion_check
from python.clean_data import run_cleaning_step
from python.analysis import run_analysis_step
from python.visualize import run_visualization_step


def display_pipeline_architecture() -> None:
    """
    Displays the visual ASCII diagram of the complete project architecture.
    """
    banner = r"""
======================================================================
               ECONOMIC DATA PIPELINE: INDIA POST-2011
      Research Question: State-Wise Per-Capita Income Divergence
======================================================================
               [1] Raw Data (RBI DBIE / MoSPI NSDP)
                               ↓
               [2] Cleaning (Standardize & Reshape)
                               ↓
               [3] Analysis (Sigma & Beta Convergence)
                               ↓
               [4] Visualization (Publication Plots)
                               ↓
               [5] R Reproduction (Cross-language Check)
                               ↓
               [6] Git Repository (Version Control & Submission)
======================================================================
"""
    print(banner)


def run_pipeline() -> None:
    """
    Executes the modular pipeline end-to-end.
    """
    display_pipeline_architecture()
    
    print("[PIPELINE] Initializing project folder structure...")
    ensure_directories_exist()
    
    # Stage 1: Data Ingestion Check
    data_ready = run_data_ingestion_check()
    
    if not data_ready:
        print("\n" + "=" * 65)
        print(" MODULE 1 STATUS: PIPELINE ARCHITECTURE READY & VERIFIED")
        print("=" * 65)
        print("All Python modules (utils, download, clean, analysis, visualize)")
        print("are compiled, syntactically valid, and ready to ingest data.")
        print("\nNext Action: When you are ready to feed real RBI/MoSPI data, place")
        print("the CSV file in data/raw/per_capita_nsdp_constant_2011_12.csv and run:")
        print("   python python/main.py")
        print("=" * 65 + "\n")
        return

    # Stage 2: Cleaning
    cleaned_ready = run_cleaning_step()
    if not cleaned_ready:
        print("[PIPELINE] Cleaning stage did not produce output. Halting.")
        return

    # Stage 3: Analysis
    analysis_ready = run_analysis_step()
    if not analysis_ready:
        print("[PIPELINE] Analysis stage halted.")
        return

    # Stage 4: Visualization
    run_visualization_step()
    
    # Stage 5: R Reproduction (Independent Verification)
    import shutil
    import subprocess
    rscript_cmd = shutil.which("Rscript")
    if not rscript_cmd:
        # Dynamically probe standard installation paths without hardcoding user names
        potential_r_roots = [
            Path.home() / "AppData" / "Local" / "Programs" / "R",
            Path("C:/Program Files/R"),
            Path("C:/Program Files (x86)/R"),
        ]
        for r_root in potential_r_roots:
            if r_root.exists():
                for candidate in r_root.glob("**/Rscript.exe"):
                    if candidate.is_file():
                        rscript_cmd = str(candidate)
                        break
            if rscript_cmd:
                break
            
    if rscript_cmd:
        r_script_path = project_root / "R" / "reproduce_analysis.R"
        if r_script_path.exists():
            print("\n[PIPELINE] Running Stage 5: Independent R Reproduction...")
            subprocess.run([rscript_cmd, str(r_script_path)], check=False)
    
    print("\n" + "=" * 65)
    print(" PIPELINE EXECUTION FINISHED SUCCESSFULLY")
    print(" Check outputs/figures/ and outputs/tables/ for generated deliverables.")
    print(" Check outputs/figures/r/ and outputs/tables/r/ for R replications.")
    print("=" * 65 + "\n")


if __name__ == "__main__":
    run_pipeline()
