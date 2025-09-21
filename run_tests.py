"""
Test runner script for the Daily Wellness Tracker.

Usage:
    python run_tests.py              # Run all tests
    python run_tests.py unit         # Run only unit tests
    python run_tests.py integration  # Run only integration tests
    python run_tests.py --coverage   # Run tests with coverage report
"""

import subprocess
import sys


def run_tests(test_type=None, coverage=False):
    """Run tests with optional filtering and coverage."""
    cmd = ["uv", "run", "python", "-m", "pytest"]

    if coverage:
        cmd.extend(["--cov=backend", "--cov-report=html", "--cov-report=term"])

    if test_type == "unit":
        cmd.extend(["-m", "unit"])
    elif test_type == "integration":
        cmd.extend(["-m", "integration"])

    cmd.append("tests/")

    print(f"Running: {' '.join(cmd)}")
    return subprocess.run(cmd)


if __name__ == "__main__":
    test_type = None
    coverage = False

    if len(sys.argv) > 1:
        if sys.argv[1] in ["unit", "integration"]:
            test_type = sys.argv[1]
        elif sys.argv[1] == "--coverage":
            coverage = True

    if "--coverage" in sys.argv:
        coverage = True

    result = run_tests(test_type, coverage)
    sys.exit(result.returncode)
