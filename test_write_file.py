from functions.write_file import write_file


def print_result(label, result):
    print(label)
    if isinstance(result, str) and result.startswith("Error:"):
        # Indent errors by 4 spaces
        print(f"    {result}")
    else:
        # For non-errors, treat result as the created file path
        print(f"    Success, file path: {result}")
    print()  # blank line between sections


if __name__ == "__main__":
    # 1) Overwrite existing lorem.txt in calculator
    result_lorem = write_file(
        "calculator",
        "lorem.txt",
        "wait, this isn't lorem ipsum",
    )
    print_result('write_file("calculator", "lorem.txt", ...):', result_lorem)
    # 2) Create nested path under calculator/pkg
    result_more_lorem = write_file(
        "calculator",
        "pkg/morelorem.txt",
        "lorem ipsum dolor sit amet",
    )
    print_result(
        'write_file("calculator", "pkg/morelorem.txt", ...):', result_more_lorem
    )
    # 3) Attempt to write outside working directory (should not be allowed)
    result_tmp = write_file(
        "calculator",
        "/tmp/temp.txt",
        "this should not be allowed",
    )
    print_result('write_file("calculator", "/tmp/temp.txt", ...):', result_tmp)
