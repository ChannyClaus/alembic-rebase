import argparse
import io
from alembic.config import Config
from alembic import command


def main():
    alembic_cfg = Config("alembic.ini")

    # alembic doesn't support returning a structured
    # response from its API natively.
    # we parse the raw output here and parse it instead.
    stdout_buffer = io.StringIO()
    alembic_cfg.stdout = stdout_buffer
    command.heads(alembic_cfg, "head")

    stdout_buffer.seek(0)
    head_revisions = [
        line.replace(" (head)", "").replace("Rev: ", "")
        for line in stdout_buffer.read().split("\n")
        if " (head)" in line
    ]

    if len(head_revisions) != 1:
        raise Exception(
            f"Found {len(head_revisions)} head revisions ({head_revisions}), expected 1"
        )

    print(head_revisions[0])


if __name__ == "__main__":
    main()
