# alembic-rebase
Maintain a linear history of Alembic migrations without having to manually resolve merge conflict.

Organizations tend to maintain a completely linear history of database migrations for the sake of simplicity even when the tooling supports non-linear history. When they grow large enough, however, maintaining a linear history can be somewhat annoying and manual with the currently available tooling.

Let's say we have two feature branches:
```
main branch: (revision None->a) -> (revision a->b) -> (revision b->c)
feature branch 1: (revision c->d1)
feature branch 2: (revision c->d2)
```

When the feature branch 1 merges, the above becomes:
```
main branch: (revision None->a) -> (revision a->b) -> (revision b->c) -> (revision c->d1)
feature branch 2: (revision c->d2)
```

at which point the author of feature branch 2 would have to _manually_ edit their revision to be (d1 -> d2).

This action automates this by:
1. Ensure that there _exactly two_ revisions in `head` of the migration history.
2. Figure out the revision being added in the feature branch by excluding the revision head from the main branch.
3. Overwrite the parent of the new revision.

# Usage
```
name: CI

on:
  push:
    branches: ["main"]
  pull_request:
    branches: ["main"]

jobs:
  # run all Alembic migrations available in the current repository.
  # fails when there are multiple heads.
  upgrade:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres
        env:
          POSTGRES_HOST_AUTH_METHOD: trust
        ports:
          - 5432:5432
        # Set health checks to wait until postgres has started
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v3
      - run: uv run alembic upgrade head
        env:
          # done via adding
          # config.set_main_option("sqlalchemy.url", os.environ["DB_URL"]) in env.py
          DB_URL: postgresql://postgres@localhost:5432/postgres
        id: alembic_upgrade

  rebase:
    runs-on: ubuntu-latest
    permissions:
      # Give the default GITHUB_TOKEN write permission to commit and push the
      # added or changed files to the repository.
      contents: write

    # automatically rebases the migration with the new parent revision
    needs: upgrade
    if: ${{ always() && needs.upgrade.result == 'failure' }}
    steps:
      - uses: actions/checkout@v4
        # this token is used to create the rebasing commit.
        # this is necessary because the commits created by the defualt GitHub Action user
        # do _not_ trigger CI (see https://github.com/peter-evans/create-pull-request/issues/48).
        # make sure to include `repo` and `workflow` scopes.
        with:
          token: ${{ secrets.REPO_PAT }}
      - uses: ChannyClaus/alembic-rebase@v0.2
```
