# Oblique Strategies for Python

Shows koans from [Oblique Strategies](https://en.wikipedia.org/wiki/Oblique_Strategies).

You can get the official [physical card set](https://www.enoshop.co.uk/product/oblique-strategies) as well.

```
❯ pip install oblique
❯ python -m oblique --help
Usage: python -m oblique [OPTIONS]

Options:
  --edition TEXT   Which OS editions to include?  [default: 1,2,3,4]
  --extra          Include additional koans found online  [default: False]
  --python         Include Monty Python quotes  [default: False]
  --five-rings     Include quotes from 'The Book of Five Rings'  [default: False]
  --count INTEGER  How many koans to show  [default: 3]
  --of-the-day     Show one koan from the set chosen for today by a
                   reproducible pseudo-random algorithm. If set, --count is
                   ignored.  [default: False]
  --attribution    Append attribution to the printed out koan(s).
                   [default: False]
  --help           Show this message and exit.

❯ oblique
Faced with a choice, do both (from Dieter Rot)
Do something sudden, destructive and unpredictable
Move towards the unimportant
```

## Change Log

## 25.5.0
- Added quotes from "Monty Python's Life of Brian".
- Fixed running with `python -m oblique`, which previously ignored
  command-line arguments.

## 25.4.0
- Added quotes from "The Book of Five Rings".
- Introduced the `--attribution` parameter.

## 25.2.1
- No functional changes, build system replaced with Setuptools on uv.

### 25.2.0
- Introduced the `--of-the-day` parameter.
- Now requires Python 3.9+.

### 25.1.0
- Fixed Python 3.10+ incompatibility with `random.sample`. Patch by Hugo
  van Kemenade.

### 22.2.0
- Initial version.

## License

Code is BSD-3 licensed. Koans attributed to Brian Eno and Peter Schmidt. 