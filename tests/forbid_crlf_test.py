import pytest

from pre_commit_hooks.forbid_crlf import main as forbid_crlf


@pytest.mark.parametrize(
    ("input_s", "expected"),
    (
        ("foo\nbar", True),
        ("foo\rbar", True),
        ("foo\r\nbar", False),
    ),
)
def test_forbid_tabs(input_s, expected, tmpdir):
    path = tmpdir.join("file.txt")
    path.write(input_s)
    assert (forbid_crlf([path.strpath]) == 0) == expected


def test_nothing_to_forbid():
    assert forbid_crlf([__file__]) == 0
