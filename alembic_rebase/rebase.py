import argparse
import io

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory


def rebase(new_parent):
    alembic_cfg = Config("alembic.ini")

    script = ScriptDirectory.from_config(alembic_cfg)
    head_revisions = set(script.get_heads())

    if len(head_revisions) != 2:
        raise Exception(
            f"Found {len(head_revisions)} head revisions {', '.join(head_revisions)}, expected 2"
        )

    if new_parent not in head_revisions:
        raise Exception(
            f"provided new parent revision {new_parent} not found in head revisions {', '.join(head_revisions)}"
        )

    child = (head_revisions - set([new_parent])).pop()
    print(f"new head revision {child} to point to the new parent revision {new_parent}")

    # alembic doesn't support returning a structured
    # response from its API natively.
    # we parse the raw output here and parse it instead.
    stdout_buffer = io.StringIO()
    alembic_cfg.stdout = stdout_buffer
    command.show(alembic_cfg, child)
    stdout_buffer.seek(0)

    lines = [line for line in stdout_buffer.read().split("\n")]
    parent_to_replace = lines[1].replace("Parent: ", "")
    path = lines[2].replace("Path: ", "")

    print(f"replacing {parent_to_replace} with {new_parent} in {path}")

    new_revision_file_content = open(path).read().replace(parent_to_replace, new_parent)
    return {
        "path": path,
        "new_revision_file_content": new_revision_file_content,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebase the current branch to a new parent"
    )
    parser.add_argument(
        "--new-parent",
        help="the new parent revision for the revision added in the current branch.",
        required=True,
    )
    args = parser.parse_args()
    result = rebase(args.new_parent)
    with open(result["path"], "w") as f:
        f.write(result["new_revision_file_content"])
