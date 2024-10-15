import pytest

from alembic_rebase.rebase import rebase


def test_single_revision_on_head(monkeypatch):
    monkeypatch.chdir("tests/single_revision_on_head")
    with pytest.raises(
        Exception, match="Found 1 head revisions 1f6d3d08a7d5, expected 2"
    ):
        rebase(
            new_parent="af622108a7d5",
        )


# `rebase` should fail when the provided parent revision is
# not one of the two head revisions.
def test_two_revisions_on_head_invalid_parent(monkeypatch):
    monkeypatch.chdir("tests/two_revisions_on_head")

    with pytest.raises(
        Exception,
        match="provided new parent revision non-head-revision not found in head revisions",
    ):
        rebase(
            new_parent="non-head-revision",
        )


# successful invocation of `rebase`, returning
# the editied revision file content as well as its path.
def test_two_revisions_on_head(monkeypatch):
    monkeypatch.chdir("tests/two_revisions_on_head")
    result = rebase(
        new_parent="038a80d518db",
    )

    assert result["path"].endswith(
        "tests/two_revisions_on_head/migrations/versions/011a80d518db_.py"
    )
    assert (
        result["new_revision_file_content"]
        == '"""empty message\n\nRevision ID: 011a80d518db\nRevises:\nCreate Date: 2024-10-13 14:26:33.609665\n\n"""\n\nfrom typing import Sequence, Union\n\nimport sqlalchemy as sa\nfrom alembic import op\n\n# revision identifiers, used by Alembic.\nrevision: str = "011a80d518db"\ndown_revision: Union[str, None] = None\nbranch_labels: Union[str, Sequence[str], None] = None\ndepends_on: Union[str, Sequence[str], None] = None\n\n\ndef upgrade() -> None:\n    pass\n\n\ndef downgrade() -> None:\n    pass\n'
    )


def test_more_than_two_revisions_on_head(monkeypatch):
    monkeypatch.chdir("tests/more_than_two_revisions_on_head")
    with pytest.raises(Exception, match="Found 3 head"):
        rebase(
            new_parent="af622108a7d5",
        )
