import argparse, sys


def removes_crlf_in_file(filename):
    with open(filename, mode="rb") as file_processed:
        lines = file_processed.readlines()

    file_was_altered = False

    with open(filename, mode="wb") as file_processed:
        for line in lines:
            processed_line = line.replace(b"\r\n", b"\n")
            file_was_altered = file_was_altered or processed_line != line
            file_processed.write(processed_line)

    return file_was_altered


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)

    file_was_altered = False
    for file in args.filenames:
        if removes_crlf_in_file(file):
            print(f"Removing CRLF end-lines in: {file}")
            file_was_altered = True

    if file_was_altered:
        print("")
        print("CRLF end-lines have been successfully removed. Now aborting the commit.")
        print(
            'You can check the changes made. Then simply "git add --update ." and re-commit'
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
