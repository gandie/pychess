# pychess

Some chess experiments using the python chess library.

Written for absolutely no reason but boredom.

# Contents

- lbchess-pieces : Try to place N pieces of a given Symbol on the board which do not attack each other. Used to solve the eight queens problem using backtracking
- lbchess-randomgame : See two players playing a completely random game.

`lbchess.engine` is still in development and has no executable yet. Check tests for usage examples but do not expect it to be smart, fast or in any other way useful.

# Installation

```
python setup.py install
```

# Development

For development / testing install `dev_requirements.txt` using pip:

```
pip install -r dev_requirements.txt
```

Now you can call `tox` to run tests, check `tox.ini` for settings

# Links

- [python-chess](https://python-chess.readthedocs.io/en/latest/)
