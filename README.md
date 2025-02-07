# 471c

![coverage](https://gitlab.eecis.udel.edu/clause/471c/badges/main/coverage.svg?job=pytest)

![job status](https://gitlab.eecis.udel.edu/clause/471c/badges/main/pipeline.svg?ignore_skipped=true)



# Getting Started

## Prerequisites

1. Install `git`: https://git-scm.com/downloads

2. Install `uv`: https://docs.astral.sh/uv/getting-started/installation/

3. Install `python`: 

    ```console
    uv python install
    ```

## Installation

1. Clone the repository

2. Install pre-commit hooks
    ```console
    471c$ uv run pre-commit install
    ```

3. Install dependencies:
    ```console
    471c$ uv sync
    ```

# Usage

* Run tests

    ```console
    471c$ uv run pytest
    ```

    Test report is in `report.html`.
    Coverage report is in `htmlcov/index.html`.

