# alembic-rebase
Maintain a linear history of Alembic migrations without having to manually resolve merge conflict. 

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
        # this is necessayr because the commits created by the defualt GitHub Action user
        # do _not_ trigger CI (see https://github.com/peter-evans/create-pull-request/issues/48).
        # make sure to include `repo` and `workflow` scopes.
        with:
          token: ${{ secrets.REPO_PAT }}
      - uses: ChannyClaus/alembic-rebase@main
```
