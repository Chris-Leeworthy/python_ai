from config import MAX_CHARS
from functions.get_file_content import get_file_content


def print_result(label, result):
    print(label)
    if result.startswith("Error:"):
        # Indent errors by 4 spaces
        print(f"    {result}")
    else:
        # For non-errors, just print the length and a short preview
        print(f"    Length: {len(result)}")
        preview = result[:2000].replace("\n", "\\n")
        print(f"    Preview: {preview}...")
    print()  # blank line between sections


if __name__ == "__main__":
    # 1) Large lorem.txt: ensure truncation
    lorem_result = get_file_content("calculator", "lorem.txt")
    print("Testing truncation for lorem.txt:")
    print(f"  Length: {len(lorem_result)}")
    expected_suffix = f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    print(f"  Ends with truncation message: {lorem_result.endswith(expected_suffix)}")
    print()

    # 2) Regular file in working directory: calculator/main.py
    result_main = get_file_content("calculator", "main.py")
    print_result('Result for file "main.py":', result_main)

    # 3) File in subdirectory: calculator/pkg/calculator.py
    result_pkg_calc = get_file_content("calculator", "pkg/calculator.py")
    print_result('Result for file "pkg/calculator.py":', result_pkg_calc)

    # 4) Absolute path outside working dir: "/bin/cat" (should be error)
    result_bin_cat = get_file_content("calculator", "/bin/cat")
    print_result('Result for "/bin/cat":', result_bin_cat)

    # 5) Non-existent file in subdirectory: pkg/does_not_exist.py (should be error)
    result_missing = get_file_content("calculator", "pkg/does_not_exist.py")
    print_result('Result for "pkg/does_not_exist.py":', result_missing)
