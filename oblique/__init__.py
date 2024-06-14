from __future__ import annotations

__version__ = "22.2.1"

from configparser import ConfigParser
from pathlib import Path
import random
import sys

import click


CURRENT_DIR = Path(__file__).parent


DEFAULT_EDITION = "1,2,3,4"
DEFAULT_COUNT = 3
DEFAULT_EXTRA = False
DEFAULT_PYTHON = False


@click.command()
@click.version_option(__version__)
@click.option(
    "--edition",
    default=DEFAULT_EDITION,
    help="Which OS editions to include?",
    show_default=True,
)
@click.option(
    "--extra",
    is_flag=True,
    default=DEFAULT_EXTRA,
    help="Include additional koans found online",
    show_default=True,
)
@click.option(
    "--python",
    is_flag=True,
    default=DEFAULT_PYTHON,
    help="Include Monty Python quotes",
    show_default=True,
)
@click.option(
    "--count",
    default=DEFAULT_COUNT,
    type=int,
    help="How many koans to show",
    show_default=True,
)
def main_command(edition: str, count: int, extra: bool, python: bool) -> None:
    return main(edition, count, extra, python)


def main(
    edition: str = DEFAULT_EDITION,
    count: int = DEFAULT_COUNT,
    extra: bool = DEFAULT_EXTRA,
    python: bool = DEFAULT_PYTHON,
) -> None:
    include_editions: set[int] = set()
    for value in edition.split(","):
        if not value:
            continue
        try:
            include_editions.add(int(value.strip()))
        except (ValueError, TypeError):
            print(f"warning: invalid edition {value}", file=sys.stderr)
            continue

    strategies = get_strategies(include_editions, python=python, extra=extra)

    try:
        for koan in random.sample(list(strategies), count):
            print(koan)
    except ValueError as ve:
        print(
            f"note: no koans to show ({len(strategies)} selected): {ve}",
            file=sys.stderr,
        )


def get_strategies(
    editions: set[int], *, extra: bool = False, python: bool = False
) -> set[str]:
    cfg = ConfigParser(interpolation=None, empty_lines_in_values=False)
    cfg.read(CURRENT_DIR / "strategies.ini")
    sect = cfg["strategies"]

    if not extra:
        del sect["extra"]

    if not python:
        keys_to_delete = [key for key in sect if key.startswith("monty python")]
        for key in keys_to_delete:
            del sect[key]

    allow_editions = set(f"edition {i}" for i in editions)
    keys_to_delete = [
        key for key in sect if key.startswith("edition ") and key not in allow_editions
    ]
    for key in keys_to_delete:
        del sect[key]

    strategies: set[str] = set()
    for _author, values in sect.items():
        lines = values.strip().splitlines()
        strategies.update(lines)

    return strategies
