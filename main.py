import datetime
import argparse
import csv


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


def main():
    parser = create_parser()
    args = parser.parse_args()


if __name__ == "__main__":
    main()
