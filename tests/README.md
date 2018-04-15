# Notebook Tests

This directory contains a script for testing that the notebook scripts run without errors.

To run this script manually:
```
python test_analysis_notebooks.py
```

or

```
python -m unittest discover
```

The notebook requires the modules listed in the `requirements.txt` file, in the top level directory of the repository.

Tests are automatically run on every commit [here](https://circleci.com/gh/bjmorgan/garnet-lgmc-data).
