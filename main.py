from datetime import datetime
from fpdf import FPDF
import os
import sys


HEADER_HORIZONTAL_PADDING = 8


def extract_codes(filename: str) -> list[str]:
    with open(filename, 'r', encoding="utf-8-sig") as f:
        return [code.strip() for code in f.readlines()]
    

def make_header(filename: str) -> str:
    name = filename.split("/")[-1].strip(".txt") if "/" in filename else filename.split("\\")[-1].strip(".txt")
    dashes = "-" * (2 * HEADER_HORIZONTAL_PADDING + len(name))
    whitespace = " " * (HEADER_HORIZONTAL_PADDING - 1)
    return f"{dashes}\n|{whitespace}{name}{whitespace}|\n{dashes}"
    

def make_body(codes: list[str]) -> str:
    return "\n".join([f"[ ] {code}" for code in codes])


def make_footer() -> str:
    return f"Generated at {datetime.now()}"


def generate_backup_page_text(filename: str) -> str:
    codes = extract_codes(filename)
    header = make_header(filename)
    body = make_body(codes)
    footer = make_footer()
    return f"{header}\n\n{body}\n\n{footer}"


def doc_to_pdf(filepath: str, output_path: str) -> None:
    try:
        text = generate_backup_page_text(filepath if filepath.endswith(".txt") else filepath + ".txt")
    except FileNotFoundError:
        print(f"Ignoring {filepath} as it does not exist")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Courier", size=9)
    pdf.multi_cell(0, 4, text)
    pdf.output(output_path if output_path.endswith(".pdf") else f"{output_path}.pdf")


def docs_to_pdf(dir: str, output_path: str) -> None:
    try:
        filepaths = [os.path.join(dir, file) for file in os.listdir(dir) if file.endswith(".txt")]
    except FileNotFoundError:
        print(f"Ignoring {dir} as it does not exist")
        return

    pdf = FPDF()
    pdf.set_font("Courier", size=9)
    
    for file in filepaths:
        try:
            text = generate_backup_page_text(file)
        except FileNotFoundError:
            print(f"Ignoring {file} as it does not exist")
            continue

        pdf.add_page()
        pdf.multi_cell(0, 4, text)

    pdf.output(output_path if output_path.endswith(".pdf") else f"{output_path}.pdf")


def print_help() -> None:
    print("Welcome to PDF backupper!\n")
    print("This script takes a single backup file or a folder with with such files")
    print("and converts them into a single PDF ready for printing.\n")
    print("Backup files should be formatted like this:\n")
    print("filename=\"Service name.txt\"")
    print("code-1\ncode-2\ncode-3\n...\n")
    print("Every page of the output PDF will represent backups codes of a single service.")
    print("On the top there is a service name taken from the file being backed up.")
    print("Every code gets a place which you can mark off with a pen, like this:\n")
    print("[ ] code-1\n[ ] code-2\n[ ] code-3\n...\n")


def print_options() -> None:
    print("[1] back up a single file")
    print("[2] back up a folder")
    print("[q] quit")

def main() -> None:
    print_help()

    while True:
        print_options()
        choice = input("")

        if choice == "1":
            file_in = input("Enter the input filepath > ")
            file_out = input("Enter the output filepath > ")
            doc_to_pdf(file_in, file_out)
        elif choice == "2":
            dir_in = input("Enter the input directory path > ")
            file_out = input("Enter the output filepath > ")
            docs_to_pdf(dir_in, file_out)
        elif choice == "q":
            sys.exit(0)


if __name__ == "__main__":
    main()
