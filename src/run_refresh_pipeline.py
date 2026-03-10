import subprocess
import sys


def run_step(step_name: str, command: list[str]) -> None:
    print(f"\n--- Running: {step_name} ---")
    result = subprocess.run(command, capture_output=True, text=True)

    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        raise RuntimeError(f"{step_name} failed with exit code {result.returncode}")


def main():
    python_exec = sys.executable

    run_step("Fetch GDELT", [python_exec, "src/fetch_gdelt.py"])
    run_step("Clean GDELT", [python_exec, "src/clean_gdelt.py"])

    # Optional ACLED refresh
    # Keep this if your current ACLED historical pipeline is still useful
    # run_step("Fetch ACLED", [python_exec, "src/fetch_data.py"])
    # run_step("Clean ACLED", [python_exec, "src/clean_data.py"])

    print("\nRefresh pipeline completed successfully.")


if __name__ == "__main__":
    main()