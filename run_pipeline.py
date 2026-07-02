import subprocess
import sys
from pathlib import Path
from datetime import datetime
import traceback

# Setup logging configuration
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)
LOG_FILE = LOG_DIR / "pipeline.log"

def log_message(message, level="INFO"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_msg = f"[{timestamp}] [{level}] {message}"
    # Print to standard output/error
    if level == "ERROR":
        sys.stderr.write(formatted_msg + "\n")
    else:
        sys.stdout.write(formatted_msg + "\n")
    # Write to the log file
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(formatted_msg + "\n")

def main():
    python_executable = sys.executable
    dbt_executable = Path(python_executable).parent / "dbt"
    if not dbt_executable.exists():
        dbt_executable = "dbt"  # Fallback to system PATH

    start_time = datetime.now()
    log_message("=" * 60, "INFO")
    log_message(f"ELT Pipeline started at {start_time.strftime('%Y-%m-%d %H:%M:%S')}", "INFO")
    log_message("=" * 60, "INFO")

    try:
        log_message("Step [1/6]: Extracting Products...", "INFO")
        subprocess.run([python_executable, "extract/extract_products.py"], check=True)

        log_message("Step [2/6]: Extracting Users...", "INFO")
        subprocess.run([python_executable, "extract/extract_users.py"], check=True)

        log_message("Step [3/6]: Extracting Carts...", "INFO")
        subprocess.run([python_executable, "extract/extract_carts.py"], check=True)

        log_message("Step [4/6]: Loading data into DuckDB...", "INFO")
        subprocess.run([python_executable, "load/load_duckdb.py"], check=True)

        log_message("Step [5/6]: Running dbt models...", "INFO")
        subprocess.run(
            [str(dbt_executable), "run"],
            cwd="ecommerce_dbt",
            check=True
        )

        log_message("Step [6/6]: Running dbt tests...", "INFO")
        subprocess.run(
            [str(dbt_executable), "test"],
            cwd="ecommerce_dbt",
            check=True
        )

        end_time = datetime.now()
        duration = end_time - start_time
        log_message("=" * 60, "INFO")
        log_message(f"ELT Pipeline completed successfully!", "INFO")
        log_message(f"End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')} | Duration: {duration}", "INFO")
        log_message("=" * 60, "INFO")
        sys.exit(0)

    except subprocess.CalledProcessError as e:
        end_time = datetime.now()
        error_msg = f"Pipeline step failed during execution: command {' '.join(e.cmd)} returned non-zero exit status {e.returncode}."
        log_message(error_msg, "ERROR")
        log_message(f"ELT Pipeline finished with status: FAILURE | End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}", "ERROR")
        sys.exit(e.returncode)
    except Exception as e:
        end_time = datetime.now()
        error_msg = f"Pipeline failed with unexpected error: {str(e)}\n{traceback.format_exc()}"
        log_message(error_msg, "ERROR")
        log_message(f"ELT Pipeline finished with status: FAILURE | End Time: {end_time.strftime('%Y-%m-%d %H:%M:%S')}", "ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()