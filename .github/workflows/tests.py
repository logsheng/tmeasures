
name: tests

on:
  push:
    branches: [ master ]
  pull_request:
    branches: [ master ]

jobs:
  build:

    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        python-version: ['3.6', '3.7', '3.8']
        backend: [tensorflow, pytorch]
        os: [ubuntu-latest] #, macos-latest, windows-latest]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies, ${{ matrix.backend }}, and probflow
      run: |
        python -m pip install --upgrade pip
        python -m pip install -e .[dev,${{ matrix.backend }}]
    - name: Lint with flake8
      run: |
        flake8 src/probflow tests
    - name: Style checks with black
      run: |
        black --check src/probflow tests
    - name: Run tests
      run: |
        pytest tests/unit/${{ matrix.backend }} --cov=probflow --cov-report xml:coverage.xml
    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v1
      with:
        file: ./coverage.xml
    - name: Ensure the package builds
      run: |
        python setup.py sdist bdist_wheel
        twine check dist/*