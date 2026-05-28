name: Build EXE

on:
  workflow_dispatch:

jobs:
  build:
    runs-on: windows-latest

    steps:
    - uses: actions/checkout@v4

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: pip install pyinstaller tkinterdnd2

    - name: Build EXE
      run: pyinstaller --onefile --noconsole pdf_tool_app.py

    - name: Upload EXE
      uses: actions/upload-artifact@v4
      with:
        name: pdf-tool
        path: dist/*
