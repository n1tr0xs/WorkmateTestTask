import datetime
import argparse
import csv
from tabulate import tabulate


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Workmate Test Task",
        description="Программа формирует отчет успеваемости студентов.",
    )

    parser.add_argument(
        "--files",
        required=True,
        nargs="+",
        help="Пути к файлам с данными",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=[
            "student-performance",
        ],
        help="Вид отчета",
    )

    return parser


def read_csv_file(filepath: str) -> list[dict]:
    """
    Читает CSV-файл и возвращает его содержимое в виде списка словарей.

    Каждый словарь содержит следующие ключи:
        - "student_name" (str): имя студента.
        - "subject" (str): название предмета.
        - "teacher_name" (str): имя преподавателя.
        - "date" (datetime.date): дата выставления оценки (формат 'YYYY-MM-DD').
        - "grade" (int): числовая оценка.
    """
    import csv
    import datetime

    try:
        with open(filepath, newline="", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            data = []
            for row in reader:
                try:
                    data.append(
                        {
                            "student_name": row["student_name"],
                            "subject": row["subject"],
                            "teacher_name": row["teacher_name"],
                            "date": datetime.datetime.strptime(
                                row["date"], "%Y-%m-%d"
                            ).date(),
                            "grade": int(row["grade"]),
                        }
                    )
                except (ValueError, KeyError) as e:
                    print(f"Ошибка в строке {row}: {e}")
            return data
    except FileNotFoundError:
        print(f"Файл не найден: {filepath}.")
        return []
    except Exception as e:
        print(f"Ошибка при чтении файла {filepath}: {e}")
        return []


def student_perfomance_report(data: list[dict]) -> dict[str, float]:
    """
    Формирует отчет об успеваемости студентов.

    Возвращает:
        dict[str, float]: Словарь вида {имя_студента: средний_балл}.
    """
    student_grades = {}
    for row in data:
        name = row["student_name"]
        grade = row["grade"]

        if name not in student_grades:
            student_grades[name] = [grade]
        else:
            student_grades[name].append(grade)
    return {name: sum(grades) / len(grades) for name, grades in student_grades.items()}


def print_student_perfomance_report(report: dict[str, float]) -> None:
    """
    Выводит отчет об успеваемости студентов.
    Сортирует студентов в порядке успеваемости, в случае одинаковой успеваемости - в алфавитном порядке.
    """
    if not report:
        print("Нет данных для отчета.")
        return

    table = sorted(report.items(), key=lambda item: (-item[1], item[0]))
    print(
        tabulate(
            table,
            headers=["student_name", "grade"],
            showindex=range(1, len(table) + 1),
            tablefmt="pretty",
            floatfmt=".1f",
        )
    )


def main():
    parser = create_parser()
    args = parser.parse_args()

    data = []
    for file in args.files:
        data.extend(read_csv_file(file))
        
    match args.report:
        case "student-performance":
            report = student_perfomance_report(data)
            print_student_perfomance_report(report)
        case _:
            print("Этот функционал пока не готов.")

if __name__ == "__main__":
    main()
