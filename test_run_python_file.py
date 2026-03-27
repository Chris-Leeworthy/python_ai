from functions.run_python_file import run_python_file


def print_result(label, result):
    print(label)
    if isinstance(result, str):
        # Print each line of the result indented
        for line in result.splitlines():
            print(f"  {line}")
    else:
        # Fallback if result is not a string
        print(f"  {result}")
    print()  # blank line between sections


if __name__ == "__main__":
    # 1) Should print calculator usage instructions
    result_usage = run_python_file("calculator", "main.py")
    print_result('run_python_file("calculator", "main.py"):', result_usage)
    # 2) Should run the calculator with an expression
    result_calc = run_python_file("calculator", "main.py", ["3 + 5"])
    print_result('run_python_file("calculator", "main.py", ["3 + 5"]):', result_calc)
    # 3) Should run calculator tests successfully
    result_tests = run_python_file("calculator", "tests.py")
    print_result('run_python_file("calculator", "tests.py"):', result_tests)
    # 4) Path outside working directory – should be an error
    result_parent = run_python_file("calculator", "../main.py")
    print_result('run_python_file("calculator", "../main.py"):', result_parent)
    # 5) Nonexistent file – should be an error
    result_missing = run_python_file("calculator", "nonexistent.py")
    print_result('run_python_file("calculator", "nonexistent.py"):', result_missing)
    # 6) Non-Python file – should be an error
    result_lorem = run_python_file("calculator", "lorem.txt")
    print_result('run_python_file("calculator", "lorem.txt"):', result_lorem)
