import argparse


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


def main():
    parser = create_parser()
    args = parser.parse_args()


if __name__ == "__main__":
    main()
