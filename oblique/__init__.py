from __future__ import annotations

__version__ = "22.2.1"

from configparser import ConfigParser
from pathlib import Path
import random
import sys

import click


CURRENT_DIR = Path(__file__).parent


@click.command()
@click.version_option(__version__)
@click.option(
    "--edition",
    default="1,2,3,4",
    help="Which OS editions to include?",
    show_default=True,
)
@click.option(
    "--extra",
    is_flag=True,
    default=False,
    help="Include additional koans found online",
    show_default=True,
)
@click.option(
    "--python",
    is_flag=True,
    default=False,
    help="Include Monty Python quotes",
    show_default=True,
)
@click.option(
    "--count",
    default=3,
    type=int,
    help="How many koans to show",
    show_default=True,
)
def main(edition: str, count: int, extra: bool, python: bool) -> None:
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
        for koan in random.sample(strategies, count):
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
