import pytest

from pre_commit_hooks.remove_tabs import main as remove_tabs


@pytest.mark.parametrize(
    ("input_s", "expected", "expected_retval"),
    (
        ("  foo", "  foo", 0),
        ("foo  ", "foo  ", 0),
        ("\tfoo", "    foo", 1),
        ("foo\t", "foo ", 1),
        ("foo \t", "foo     ", 1),
        ("foo \t  \t\t   bar", "foo                bar", 1),
        (
            "No leading\ttab\n\tleading\ttab\n \tSpace then\tTab\n",
            "No leading  tab\n    leading tab\n    Space then  Tab\n",
            1,
        ),
        (
            "Tabs\tbetween\tevery\tword\tin\tthe\tline.\n",
            "Tabs    between every   word    in  the line.\n",
            1,
        ),
        (
            "Space \tthen \ttab \tbetween \tevery \tword \tin \tthe \tline.",
            "Space   then    tab     between     every   word    in  the     line.",
            1,
        ),
        (
            "cat <<- EOF\n\tfoo\n\tbar\n\tEOF",
            "cat <<- EOF\n    foo\n    bar\n    EOF",
            1,
        ),
        (
            "cat <<- EOF\n\tfoo\n\tbar\tbaz\n\tEOF",
            "cat <<- EOF\n    foo\n    bar baz\n    EOF",
            1,
        ),
    ),
)
def test_remove_tabs(input_s, expected, expected_retval, tmpdir):
    path = tmpdir.join("file.txt")
    path.write(input_s)
    assert remove_tabs(("--whitespaces-count=4", path.strpath)) == expected_retval
    assert path.read() == expected


@pytest.mark.parametrize(
    ("input_s", "expected", "expected_retval"),
    (
        ("  foo", "  foo", 0),
        ("foo  ", "foo  ", 0),
        ("\tfoo", "    foo", 1),
        ("foo\t", "foo ", 1),
        (
            "cat <<- EOF\n\tfoo\n\tbar\n\tEOF",
            "cat <<- EOF\n\tfoo\n\tbar\n\tEOF",
            0,
        ),
        (
            "cat <<- EOF\n\tfoo\n\tbar\tbaz\n\tEOF",
            "cat <<- EOF\n\tfoo\n\tbar baz\n\tEOF",
            1,
        ),
    ),
)
def test_remove_tabs_allow_heredoc(input_s, expected, expected_retval, tmpdir):
    path = tmpdir.join("file.txt")
    path.write(input_s)
    assert (
        remove_tabs(("--whitespaces-count=4", "--allow-heredoc", path.strpath))
        == expected_retval
    )
    assert path.read() == expected


@pytest.mark.parametrize(("arg"), ("", "--", "a.b", "a/b"))
def test_badopt(arg):
    with pytest.raises(SystemExit) as excinfo:
        remove_tabs(["--whitespaces-count", arg])
    assert excinfo.value.code == 2


def test_nothing_to_fix():
    assert remove_tabs(["--whitespaces-count=4", __file__]) == 0
