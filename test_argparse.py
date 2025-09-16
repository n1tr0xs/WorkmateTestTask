import pytest

from main import create_parser

def test_parse_args():
    parser = create_parser()
    args = parser.parse_args(
        ["--files", "students1.csv", "students2.csv", "--report", "student-performance"]
    )
    assert args.files == ["students1.csv", "students2.csv"]
    assert args.report == "student-performance"

def test_missing_files():
    parser = create_parser()
    with pytest.raises(SystemExit):
        args = parser.parse_args(["--report", "student-performance"])

def test_missing_report():
    parser = create_parser()
    with pytest.raises(SystemExit):
        args = parser.parse_args(["--files", "students1.csv"])
