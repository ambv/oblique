from oblique import get_strategies, koan_of_the_day, main


def test_all():
    s = get_strategies(editions={1, 2, 3, 4}, extra=True, python=True)
    assert len(s) > 200
    assert "Discard an axiom" in s
    assert "Just a flesh wound." in s
    assert "Turn it into a game." in s


def test_zero():
    s = get_strategies(editions=set(), extra=False, python=False)
    assert len(s) == 0


def test_main(capsys):
    main(edition="", count=3, extra=True, python=False)
    pos = get_strategies(editions=set(), extra=True, python=True)
    neg = get_strategies(editions={1, 2, 3, 4}, extra=False, python=False)
    captured = capsys.readouterr()
    for line in captured.out.splitlines():
        assert line in pos
        assert line not in neg


def test_koan_of_the_day():
    import datetime

    strategies = set(str(i) for i in range(666))
    actual = []
    expected_str = """
    155 18 46 145 181 268 8 406 234 146 540 637 495 496 269 261 62 628 136 374 214 467
    386 149 513 455 325 616 51 128 396 35 574 624 451 340 351 529 208 291 579 222 28 27
    577 123 216 478 207 63 641 509 446 192 277 489 457 418 135 420 283 233 464 361 360
    376 324 286 43 191 339 290 627 199 502 459 297 225 82 120 653 483 434 444 594 127
    """
    expected = expected_str.strip().split()
    date = datetime.date(1985, 3, 7)
    while len(actual) <= 85:
        actual.append(koan_of_the_day(strategies, date=date))
        date += datetime.timedelta(days=1)
    assert actual == expected, " ".join(actual)