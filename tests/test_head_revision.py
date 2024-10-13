import pytest
from alembic_rebase.head_revision import head_revision


def test_head_revision_single_revision_on_head(monkeypatch):
    monkeypatch.chdir("tests/single_revision_on_head")
    assert "1f6d3d08a7d5" == head_revision(
        alembic_cfg_path="alembic.ini",
    )


def test_head_revision_two_revisions_on_head(monkeypatch):
    monkeypatch.chdir("tests/two_revisions_on_head")

    with pytest.raises(Exception, match="Found 2 head revisions"):
        head_revision(
            alembic_cfg_path="alembic.ini",
        )
