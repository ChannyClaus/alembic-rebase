import argparse

from alembic.config import Config
from alembic.script import ScriptDirectory


def head_revision():
    alembic_cfg = Config("alembic.ini")
    script = ScriptDirectory.from_config(alembic_cfg)
    head_revisions = script.get_heads()

    if len(head_revisions) != 1:
        raise Exception(
            f"Found {len(head_revisions)} head revisions {', '.join(head_revisions)}, expected 1"
        )
    return head_revisions[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print the head revision of the current branch."
    )
    args = parser.parse_args()
    print(head_revision())
