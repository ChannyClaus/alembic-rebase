import argparse
import io
from alembic.config import Config
from alembic import command


def main(alembic_cfg_path, new_parent):
    alembic_cfg = Config(alembic_cfg_path)

    # alembic doesn't support returning a structured
    # response from its API natively.
    # we parse the raw output here and parse it instead.
    stdout_buffer = io.StringIO()
    alembic_cfg.stdout = stdout_buffer
    command.branches(alembic_cfg, "head")

    stdout_buffer.seek(0)
    head_revisions = set(
        [
            line.replace("             -> ", "")[:12]
            for line in stdout_buffer.read().split("\n")
            if "(head)" in line
        ]
    )

    if len(head_revisions) != 2:
        raise Exception(
            f"Found {len(head_revisions)} head revisions ({head_revisions}), expected 2"
        )

    if new_parent not in head_revisions:
        raise Exception(
            f"provided new parent revision {new_parent} not found in head revisions ({head_revisions})"
        )

    child = (head_revisions - set([new_parent])).pop()

    stdout_buffer.seek(0)
    command.show(alembic_cfg, child)
    stdout_buffer.seek(0)

    lines = [line for line in stdout_buffer.read().split("\n")]
    parent_to_replace = lines[1].replace("Parent: ", "")
    path = lines[2].replace("Path: ", "")

    new_file_content = open(path).read().replace(parent_to_replace, new_parent)

    with open(path, "w") as f:
        f.write(new_file_content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebase the current branch to a new parent"
    )
    parser.add_argument(
        "--new-parent",
        help="the new parent revision for the revision added in the current branch.",
        required=True,
    )
    parser.add_argument(
        "--alembic-cfg-path",
        help="path to the alembic configuration file",
        required=True,
    )
    args = parser.parse_args()
    main(args.alembic_cfg_path, args.new_parent)
