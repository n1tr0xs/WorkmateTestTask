import pytest
import datetime
from tabulate import tabulate

from main import student_perfomance_report, print_student_perfomance_report


def test_student_perfomance_report_basic():
    data = [
        {
            "student_name": "Семенова Елена",
            "subject": "Английский язык",
            "teacher_name": "Ковалева Анна",
            "date": datetime.date(2023, 10, 10),
            "grade": 5,
        },
        {
            "student_name": "Семенова Елена",
            "subject": "География",
            "teacher_name": "Орлов Сергей",
            "date": datetime.date(2023, 10, 12),
            "grade": 4,
        },
        {
            "student_name": "Власова Алина",
            "subject": "Биология",
            "teacher_name": "Ткаченко Наталья",
            "date": datetime.date(2023, 10, 15),
            "grade": 5,
        },
        {
            "student_name": "Власова Алина",
            "subject": "Литература",
            "teacher_name": "Белова Светлана",
            "date": datetime.date(2023, 10, 18),
            "grade": 2,
        },
    ]

    result = student_perfomance_report(data)
    assert result["Семенова Елена"] == pytest.approx((5 + 4) / 2)
    assert result["Власова Алина"] == pytest.approx((5 + 2) / 2)


def test_student_perfomance_report_single_student():
    data = [
        {
            "student_name": "Семенова Елена",
            "subject": "Английский язык",
            "teacher_name": "Ковалева Анна",
            "date": datetime.date(2023, 10, 10),
            "grade": 5,
        },
        {
            "student_name": "Семенова Елена",
            "subject": "География",
            "teacher_name": "Орлов Сергей",
            "date": datetime.date(2023, 10, 12),
            "grade": 3,
        },
        {
            "student_name": "Семенова Елена",
            "subject": "Биология",
            "teacher_name": "Ткаченко Наталья",
            "date": datetime.date(2023, 10, 15),
            "grade": 1,
        },
        {
            "student_name": "Семенова Елена",
            "subject": "Литература",
            "teacher_name": "Белова Светлана",
            "date": datetime.date(2023, 10, 18),
            "grade": 2,
        },
    ]

    result = student_perfomance_report(data)
    assert result == {"Семенова Елена": pytest.approx((5 + 3 + 1 + 2) / 4)}


def test_student_perfomance_report_empty():
    data = []
    result = student_perfomance_report(data)
    assert result == {}


def test_student_perfomance_report_invalid_data_missing_name():
    invalid_data = [
        {
            "subject": "Литература",
            "teacher_name": "Белова Светлана",
            "date": datetime.date(2023, 10, 18),
            "grade": 2,
        },
    ]

    with pytest.raises(KeyError):
        student_perfomance_report(invalid_data)


def test_student_perfomance_report_invalid_data_missing_grade():
    invalid_data = [
        {
            "student_name": "Семенова Елена",
            "subject": "Английский язык",
            "teacher_name": "Ковалева Анна",
            "date": datetime.date(2023, 10, 10),
        },
    ]

    with pytest.raises(KeyError):
        student_perfomance_report(invalid_data)


def test_print_student_perfomance_report_normal(capsys):
    report = {
        "Семенова Елена": 4.8,
        "Власова Алина": 5,
        "Дорофеев Никита": 3.5
    }
    
    print_student_perfomance_report(report)
    captured = capsys.readouterr()
    
    expected_table = tabulate(
        sorted(report.items(), key=lambda item: (-item[1], item[0])),
        headers=["student_name", "grade"],
        showindex=range(1, len(report)+1),
        tablefmt="pretty",
        floatfmt=".1f"
    )
    
    assert captured.out.strip() == expected_table

def test_print_student_perfomance_report_empty(capsys):
    report = {}
    print_student_perfomance_report(report)
    captured = capsys.readouterr()
    
    assert captured.out.strip() == "Нет данных для отчета."