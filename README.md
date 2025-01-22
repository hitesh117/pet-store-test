# Pet Store API Test Project

## Overview
This project contains automated tests for the publicly available Pet Store API using pytest framework.
Test scenarios are covered in the scenarios.pdf file.

## Installation
1. Install all the packages listed in requirements.txt:
```bash
pip install -r requirements.txt
```
2. Run all tests 
```bash
pytest -v --html=report.html
```

---

### NOTE: Minimum requirement scenarios are covered in ./e2e

---
We can also run the tests using specific marker to save time.

Available modules/marks: `pet`, `store`, `user`, `performance`, `e2e`

Run the following command to execute specific modules: `pytest -v -m MODULE_NAME --html=report.html`

---

Most of the tests are parameterized and modularized. Easing the process of adding new cases and reusing the already existing capabilities.