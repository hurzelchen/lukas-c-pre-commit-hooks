import pytest

from pre_commit_hooks.forbid_tabs import main as forbid_tabs


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("foo", True),
        ("\tfoo", False),
        ("foo\t", False),
        ("cat <<- EOF\nfoo\nbar\nEOF", True),
        ("cat <<- 'EOF'\nfoo\nbar\nEOF", True),
        ("cat <<- EOF\n\tfoo\n\tbar\n\tEOF", False),
        ("cat <<- 'EOF'\n\tfoo\n\tbar\n\tEOF", False),
        ("cat <<- EOF\n\tfoo\n\tbar\tbaz\n\tEOF", False),
        ("cat <<- 'EOF'\n\tfoo\n\tbar\tbaz\n\tEOF", False),
    ),
)
def test_forbid_tabs(input_s, expected, tmpdir):
    path = tmpdir.join("file.txt")
    path.write(input_s)
    assert (forbid_tabs([path.strpath]) == 0) == expected


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("foo", True),
        ("\tfoo", False),
        ("foo\t", False),
        ("cat <<- EOF\nfoo\nbar\nEOF", True),
        ("cat <<- 'EOF'\nfoo\nbar\nEOF", True),
        ("cat <<- EOF\n\tfoo\n\tbar\n\tEOF", True),
        ("cat <<- 'EOF'\n\tfoo\n\tbar\n\tEOF", True),
        ("cat <<- EOF\n\tfoo\n\tbar\tbaz\n\tEOF", False),
        ("cat <<- 'EOF'\n\tfoo\n\tbar\tbaz\n\tEOF", False),
    ),
)
def test_forbid_tabs_allow_heredoc(input_s, expected, tmpdir):
    path = tmpdir.join("file.txt")
    path.write(input_s)
    assert (forbid_tabs(["--allow-heredoc", path.strpath]) == 0) == expected


def test_nothing_to_forbid():
    assert forbid_tabs([__file__]) == 0
