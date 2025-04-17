from __future__ import annotations

from configparser import ConfigParser
import datetime
from importlib import metadata
from pathlib import Path
import random
import re
import sys

import click


try:
    __version__ = metadata.version("oblique")
except metadata.PackageNotFoundError:
    __version__ = "unknown"


CURRENT_DIR = Path(__file__).parent

DEFAULT_EDITION = "1,2,3,4"
DEFAULT_COUNT = 3
DEFAULT_EXTRA = False
DEFAULT_PYTHON = False
DEFAULT_FIVE_RINGS = False

EDITION_RE = re.compile(r"^Edition (?P<ed>\d+)$")


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
    "--five-rings",
    is_flag=True,
    default=DEFAULT_FIVE_RINGS,
    help="Include quotes from 'The Book of Five Rings'",
    show_default=True,
)
@click.option(
    "--count",
    default=DEFAULT_COUNT,
    type=int,
    help="How many koans to show",
    show_default=True,
)
@click.option(
    "--of-the-day",
    is_flag=True,
    show_default=True,
    default=False,
    help=(
        "Show one koan from the set chosen for today by a reproducible pseudo-random"
        " algorithm. If set, --count is ignored."
    ),
)
@click.option(
    "--attribution",
    is_flag=True,
    show_default=True,
    default=False,
    help=(
        "Append attribution to the printed out koan(s)."
    ),
)
def main_command(
    edition: str,
    count: int,
    extra: bool,
    python: bool,
    five_rings: bool,
    of_the_day: bool,
    attribution: bool,
) -> None:
    return main(edition, count, extra, python, five_rings, of_the_day, attribution)


def main(
    edition: str = DEFAULT_EDITION,
    count: int = DEFAULT_COUNT,
    extra: bool = DEFAULT_EXTRA,
    python: bool = DEFAULT_PYTHON,
    five_rings: bool = DEFAULT_FIVE_RINGS,
    of_the_day: bool = False,
    attribution: bool = False,
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

    strategies = get_strategies(
        include_editions,
        python=python,
        extra=extra,
        five_rings=five_rings,
        attribution=attribution,
    )

    if of_the_day:
        print(koan_of_the_day(strategies))
        return

    try:
        extra_nl = [""] * count
        if attribution:
            extra_nl = ["\n"] * (count - 1)
            extra_nl.append("")
        for koan, nl in zip(random.sample(list(strategies), count), extra_nl):
            print(koan)
            print(end=nl)
    except ValueError as ve:
        print(
            f"note: no koans to show ({len(strategies)} selected): {ve}",
            file=sys.stderr,
        )


def get_strategies(
    editions: set[int],
    *,
    extra: bool = False,
    python: bool = False,
    five_rings: bool = False,
    attribution: bool = False,
) -> set[str]:
    cfg = ConfigParser(
        delimiters=["="],
        comment_prefixes=["#"],
        interpolation=None,
        empty_lines_in_values=False,
    )
    cfg.optionxform = lambda option: option  # type: ignore[method-assign]
    cfg.read(CURRENT_DIR / "strategies.ini")
    sect = cfg["strategies"]

    if not extra:
        del sect["Extra"]

    if not five_rings:
        del sect["The Book of Five Rings"]

    if not python:
        keys_to_delete = [key for key in sect if key.startswith("Monty Python")]
        for key in keys_to_delete:
            del sect[key]

    allow_editions = set(f"Edition {i}" for i in editions)
    keys_to_delete = [
        key for key in sect if key.startswith("Edition ") and key not in allow_editions
    ]
    for key in keys_to_delete:
        del sect[key]

    strategies: set[str] = set()
    strategies_with_attribution: set[str] = set()
    for author, values in sect.items():
        lines = values.strip().splitlines()
        if not attribution:
            strategies.update(lines)
            continue

        for line in lines:
            if line not in strategies:
                strategies_with_attribution.add(f"{line}\n  -- {author}")
                strategies.add(line)

    return strategies_with_attribution or strategies


def koan_of_the_day(strategies: set[str], date: datetime.date | None = None) -> str:
    rand = random.Random()
    rand.seed(44)
    s = sorted(strategies)
    rand.shuffle(s)

    if date is None:
        date = datetime.date.today()
    days_since_birth = (date - datetime.date(1985, 3, 7)).days
    return s[days_since_birth % len(s)]
