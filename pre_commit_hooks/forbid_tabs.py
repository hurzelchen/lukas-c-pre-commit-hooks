import argparse, sys


def contains_tabs(filename, allow_heredoc=False):
    with open(filename, mode="rb") as file_checked:
        if not allow_heredoc:
            return b"\t" in file_checked.read()

        heredoc_delim = None

        for line in file_checked.readlines():
            # Check if we are inside a here-doc
            if heredoc_delim is None:
                # Return early if we find a tab outside of a here-doc
                if b"\t" in line:
                    return True

                parts = line.split(b"<<-", maxsplit=1)

                if len(parts) > 1:
                    heredoc_delim = parts[1].strip().lstrip(b"'").rstrip(b"'")
            else:
                line = line.lstrip(b"\t")

                if b"\t" in line:
                    return True

                if line == heredoc_delim:
                    heredoc_delim = None

        return False


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    parser.add_argument("--allow-heredoc", action="store_true")
    args = parser.parse_args(argv)
    files_with_tabs = [
        f for f in args.filenames if contains_tabs(f, allow_heredoc=args.allow_heredoc)
    ]
    return_code = 0
    for file_with_tabs in files_with_tabs:
        print(f"Tabs detected in file: {file_with_tabs}")
        return_code = 1
    return return_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
