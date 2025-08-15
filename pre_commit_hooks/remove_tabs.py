import argparse, re, sys


def removes_tabs_in_file(filename, whitespaces_count, allow_heredoc=False):
    with open(filename, mode="rb") as file_processed:
        lines = file_processed.readlines()

    file_was_altered = False
    heredoc_delim = None

    with open(filename, mode="wb") as file_processed:
        for line in lines:
            if not allow_heredoc:
                processed_line = line.expandtabs(whitespaces_count)
            elif heredoc_delim is None:
                processed_line = line.expandtabs(whitespaces_count)
                parts = processed_line.split(b"<<-", maxsplit=1)
                if len(parts) > 1:
                    heredoc_delim = parts[1].strip().lstrip(b"'").rstrip(b"'")
            else:
                tab_match = re.search(b"([\\t]*)((.|\\n|\\r)*)", line)
                processed_line = tab_match.group(1) + tab_match.group(2).expandtabs(
                    whitespaces_count
                )

                if tab_match.group(2) == heredoc_delim:
                    heredoc_delim = None

            file_was_altered = file_was_altered or processed_line != line
            file_processed.write(processed_line)

    return file_was_altered


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--whitespaces-count",
        type=int,
        required=True,
        help="number of whitespaces to substitute tabs with",
    )
    parser.add_argument("--allow-heredoc", action="store_true")
    parser.add_argument("filenames", nargs="*", help="filenames to check")
    args = parser.parse_args(argv)

    file_was_altered = False
    for file in args.filenames:
        if removes_tabs_in_file(
            file,
            whitespaces_count=args.whitespaces_count,
            allow_heredoc=args.allow_heredoc,
        ):
            print(
                f"Substituting tabs in: {file} by {args.whitespaces_count} whitespaces"
            )
            file_was_altered = True

    if file_was_altered:
        print("")
        print("Tabs have been successfully removed. Now aborting the commit.")
        print(
            'You can check the changes made. Then simply "git add --update ." and re-commit'
        )
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))  # pragma: no cover
