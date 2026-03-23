from functions.get_files_info import get_files_info


def print_result(label, result):
    print(label)
    if result.startswith("Error:"):
        # Indent errors by 4 spaces
        print(f"    {result}")
    else:
        # Indent each directory entry by 2 spaces
        for line in result.splitlines():
            print(f"  {line}")
    print()  # blank line between sections


if __name__ == "__main__":
    # 1) current directory (calculator root)
    result_current = get_files_info("calculator", ".")
    print_result("Result for current directory:", result_current)
    # 2) 'pkg' directory under calculator
    result_pkg = get_files_info("calculator", "pkg")
    print_result("Result for 'pkg' directory:", result_pkg)
    # 3) absolute /bin (should be rejected)
    result_bin = get_files_info("calculator", "/bin")
    print_result("Result for '/bin' directory:", result_bin)
    # 4) parent directory (should be rejected)
    result_parent = get_files_info("calculator", "../")
    print_result("Result for '../' directory:", result_parent)
