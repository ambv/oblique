from oblique import get_strategies


def test_all():
    s = get_strategies(editions={1, 2, 3, 4}, extra=True, python=True)
    assert len(s) > 200
    assert "Discard an axiom" in s
    assert "Just a flesh wound." in s
    assert "Turn it into a game." in s


def test_zero():
    s = get_strategies(editions=set(), extra=False, python=False)
    assert len(s) == 0