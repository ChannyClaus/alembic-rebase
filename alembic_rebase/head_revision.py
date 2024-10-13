import io
from alembic.config import Config
from alembic import command
import argparse


def head_revision(alembic_cfg_path):
    alembic_cfg = Config(alembic_cfg_path)

    # alembic doesn't currently support returning a structured
    # response from its API natively; we parse the raw output here and parse it instead.
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
            f"Found {len(head_revisions)} head revisions {', '.join(head_revisions)}, expected 1"
        )

    return head_revisions[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Print the head revision of the current branch."
    )
    parser.add_argument(
        "--alembic-cfg-path",
        help="path to the alembic configuration file",
        required=True,
    )
    args = parser.parse_args()

    print(head_revision(args.alembic_cfg_path))
