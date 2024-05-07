1. **Create a new module for utility functions**:
   - Create a new Python file, e.g., `utils.py` or `helpers.py`, in the appropriate directory (e.g., `src/utils.py`).
   - This module will contain all the utility functions that are not directly related to the main application logic.

2. **Move the `_load_profile` and `_load_role` functions to the new module**:
   - Copy the `_load_profile` and `_load_role` function definitions from `run_agent.py` and paste them into the new `utils.py` or `helpers.py` module.
   - Remove the leading underscore from the function names since they will no longer be considered "private" functions.
   - Adjust the import statements within these functions if necessary.

3. **Create a test file for the utility functions**:
   - Create a new test file, e.g., `test_utils.py` or `test_helpers.py`, in the appropriate test directory (e.g., `tests/test_utils.py`).
   - Import the necessary testing framework (e.g., `unittest` or `pytest`).
   - Import the utility functions from the `utils.py` or `helpers.py` module.

4. **Write test cases for the utility functions**:
   - In the `test_utils.py` or `test_helpers.py` file, create test cases for the `load_profile` and `load_role` functions.
   - Test various scenarios, such as:
     - Passing a valid profile/role UUID
     - Passing an invalid profile/role UUID
     - Testing file not found cases
     - Testing the correct loading and parsing of JSON data
   - Use test fixtures or mocking to isolate the functions from external dependencies (e.g., file system, environment variables).

5. **Update the imports in `run_agent.py`**:
   - In `run_agent.py`, replace the existing imports of `_load_profile` and `_load_role` functions with the new import statements from the `utils.py` or `helpers.py` module.
   - Update the function calls to use the new function names (without the leading underscore).

6. **Run the tests and ensure they pass**:
   - Execute the test suite (e.g., `python -m unittest discover tests` or `pytest tests/`) to verify that all tests for the utility functions pass.

7. **Refactor and repeat for other utility functions**:
   - Identify any other utility functions in `run_agent.py` that can be extracted and follow the same process to move them to the `utils.py` or `helpers.py` module and write corresponding tests.

By separating the utility functions into their own module and writing unit tests for them, you'll improve the code's modularity, testability, and maintainability. Additionally, having a dedicated test suite for the utility functions will ensure that any changes or refactoring in the future won't break their functionality.