import csv
import pytest
import datetime

from main import read_csv_file


def test_read_csv_file(tmp_path):
    filepath = tmp_path / "test.csv"
    fieldnames = ["student_name", "subject", "teacher_name", "date", "grade"]
    rows = [
        ["Семенова Елена", "Английский язык", "Ковалева Анна", "2023-10-10", "5"],
        ["Титов Владислав", "География", "Орлов Сергей", "2023-10-12", "4"],
    ]
    data = [
        {
            "student_name": "Семенова Елена",
            "subject": "Английский язык",
            "teacher_name": "Ковалева Анна",
            "date": datetime.date(2023, 10, 10),
            "grade": 5,
        },
        {
            "student_name": "Титов Владислав",
            "subject": "География",
            "teacher_name": "Орлов Сергей",
            "date": datetime.date(2023, 10, 12),
            "grade": 4,
        },
    ]

    with open(filepath, "w", newline="", encoding="utf-8") as fout:
        writer = csv.writer(fout)
        writer.writerow(fieldnames)
        writer.writerows(rows)

    result = read_csv_file(filepath)
    assert result == data


def test_read_csv_file_not_found():
    result = read_csv_file("NON_EXISTENT_CSV_FILE.csv")
    assert result == []
