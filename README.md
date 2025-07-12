# Gitdocify

Gitdocify is a comprehensive codebase analyzer and documentation generator. This codebase is designed to analyze your code, generate and maintain a well-structured and comprehensive documentation. 

## Key Features

- Automated documentation generation
- Support for Python, Text and Markdown language files
- Comprehensive codebase analysis
- Easy tracking and maintenance of your documentation

## Tech Stack

Gitdocify is built with the following technologies:

- Python
- OpenAI API
- Other Python libraries such as click, pathspec, tiktoken, filelock, fsspec, packaging, pyyaml, Pillow, torch, numpy, pandas, python-dateutil, and joblib.

## Quick Start Guide

1. Clone the repository
   ```
   git clone https://github.com/yourusername/gitdocify.git
   ```
2. Install the dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the main file
   ```
   python src/main.py
   ```
   
## Project Structure

The project has a total of 12 files with 973 lines of code spread across 3 languages (Python, Text, and Markdown). Here is a brief overview of the key directories and files:

- `.git/` : This directory is used by git to store metadata and object database for your project. This is where all commits, remote repository addresses, etc. are stored.

- `.gitignore` : This file tells git which files (or patterns) it should ignore.

- `gitdocify.egg-info/` : This directory contains metadata for the Python package.

- `LICENSE` : This file contains the license details for the project.

- `requirements.txt` : This file lists the Python dependencies required to run the project.

- `setup.py` : This is the build script for setuptools. It tells setuptools about your package (such as the name and version) as well as which code files to include.

- `src/` : This directory contains the source code for the project. It includes an analyzer, a generator, a main file, and a utility file.

- `test.md` : This is a markdown file used for testing purposes.

We hope you find Gitdocify useful for your documentation needs. If you have any issues or suggestions, please feel free to open an issue or submit a pull request.

Happy documenting!

# Architecture

## High-level Architecture Overview

This project is a Python codebase that consists of several key components each performing a specific function. At the highest level, the architecture is divided into modules for analyzing the codebase, generating documentation, and utility functions. The main entry point of the application is `main.py`.

## Main Components and Their Responsibilities

1. `analyzer.py`: This is the Codebase Analyzer module. It's responsible for analyzing the codebase and extracting vital information like functions, classes, and imports.

2. `generator.py`: This is the Documentation Generator module. It uses the analysis from the Codebase Analyzer module to generate technical documentation.

3. `utils.py`: This module contains utility functions that assist in tasks like setting up logging, validating OpenAI key, counting tokens, and truncating content.

4. `main.py`: This is the main entry point of the application. It orchestrates the flow of data across the application.

## Data Flow

The data flow in this application is primarily linear. Here's a simple text diagram representing the flow:

```
main.py 
  --> analyzer.py (analyze codebase)
  --> generator.py (generate documentation)
```

`main.py` first calls the Codebase Analyzer (`analyzer.py`), which analyzes the codebase and returns the analysis data. This data is then passed to the Documentation Generator (`generator.py`), which generates the technical documentation based on the analysis data.

## Design Patterns Used

The design pattern used in this project is the Module Pattern. Each file serves as a standalone module that performs a specific function. This pattern allows for high modularity and separation of concerns, making the codebase easy to maintain and extend.

## Module Relationships

The relationship between the modules is as follows:

- `main.py` is dependent on all other modules as it uses their functionalities.
- `analyzer.py` and `generator.py` are independent modules performing their specific tasks. They do not rely on each other but both are used by `main.py`.
- `utils.py` provides utility functions that can be used by any module, making it a helper module. In the current setup, it's mainly used by `main.py`.

Each module is designed to be independent and to communicate with each other through function calls and data transfer.

```markdown
## Installation & Setup

This guide provides detailed steps on how to install and setup the project. 

### Prerequisites

This project requires Python 3.6 or later. If you don't have Python installed, you can download it from [here](https://www.python.org/downloads/).

The project also has several Python package dependencies which are listed below:

- openai>=1.0.0
- python-dotenv>=1.0.0
- click>=8.0.0
- pathspec>=0.11.0
- tiktoken>=0.5.0
- filelock
- fsspec
- packaging
- pyyaml
- Pillow
- torch
- numpy
- pandas>=1.2
- python-dateutil>=2.7
- joblib>=1.2.0

### Installation Steps

1. Download or clone the project repository to your local machine.

2. Navigate to the project directory in your terminal.

3. Install the project dependencies using pip. Run the following command:

   ```bash
   pip install -r requirements.txt
   ```

### Environment Setup

1. Create a `.env` file in the root directory of the project. This will be used to store your environment variables.

    ```bash
    touch .env
    ```

2. Open the `.env` file and add your environment variables as key-value pairs. Use the `.env.example` file in the project directory as a reference.

### Configuration Requirements

The project uses two configuration files: `.env` and `.env.example`.

- `.env`: This file should contain your environment variables. It is not tracked by version control.

- `.env.example`: This is an example configuration file provided for reference. It does not contain any real data.

### Verification Steps

To verify if the installation and setup were successful:

1. Check if the Python dependencies were correctly installed by running:

   ```bash
   pip freeze
   ```

   This should list all the installed Python packages including the ones required for this project.

2. Ensure that the `.env` file is correctly setup by checking if the environment variables are correctly set.

3. Run the project. If everything is set up correctly, the project should run without any errors.
```


## Usage

The main file of this project is `main.py`, located in the `src` directory. The primary function of this file is `generate_docs`.

### 1. Basic Usage Examples

The `generate_docs` function can be used as follows:

```python
from src.main import generate_docs

# Use the function
generate_docs()
```

### 2. Common Use Cases

The `generate_docs` function is primarily used to generate documentation for a project. It is commonly used in software development and data analysis projects where documentation is necessary.

### 3. Code Examples

Below is an example of how you can use the `generate_docs` function:

```python
from src.main import generate_docs

# Define a project
project = {
  "name": "My Project",
  "files": ["file1.py", "file2.py"]
}

# Generate documentation
generate_docs(project)
```

### 4. Command-line Usage

If you prefer to use the command line, you can run the `main.py` file directly. For example:

```shell
python src/main.py
```

Note: Make sure you are in the correct directory before running the command.

### 5. Important Notes

- The `generate_docs` function currently only supports Python (.py) files.
- Make sure all the files in your project are in the same directory as `main.py`, or the function may not work as expected.
- The `generate_docs` function does not automatically save the generated documentation. You need to handle saving the output yourself.

```
## API Reference

This API reference documentation provides information on the main classes, public functions, return types, descriptions, usage examples, and error handling in the codebase.

### Classes

#### `CodebaseAnalyzer`

File: `src\\analyzer.py`

This class is responsible for analyzing the codebase. 

Methods:

(Currently, there are no public methods for this class.)

#### `DocumentationGenerator`

File: `src\\generator.py`

This class is responsible for generating the documentation.

Methods:

(Currently, there are no public methods for this class.)

### Functions

#### `generate_docs()`

File: `src\\main.py`

This function is responsible for generating the documentation.

Parameters:

(Currently, there are no parameters for this function.)

Return type:

(Currently, no specific return type is defined for this function.)

Usage example:

```python
generate_docs()
```

#### `setup_logging()`

File: `src\\utils.py`

This function is responsible for setting up logging.

Parameters:

(Currently, there are no parameters for this function.)

Return type:

(Currently, no specific return type is defined for this function.)

Usage example:

```python
setup_logging()
```

#### `validate_openai_key()`

File: `src\\utils.py`

This function is responsible for validating the OpenAI key.

Parameters:

(Currently, there are no parameters for this function.)

Return type:

(Currently, no specific return type is defined for this function.)

Usage example:

```python
validate_openai_key()
```

#### `count_tokens()`

File: `src\\utils.py`

This function is responsible for counting tokens.

Parameters:

(Currently, there are no parameters for this function.)

Return type:

(Currently, no specific return type is defined for this function.)

Usage example:

```python
count_tokens()
```

#### `truncate_content()`

File: `src\\utils.py`

This function is responsible for truncating content.

Parameters:

(Currently, there are no parameters for this function.)

Return type:

(Currently, no specific return type is defined for this function.)

Usage example:

```python
truncate_content()
```

### Error Handling

In case of any errors, the Python exceptions will be thrown. Make sure to handle these exceptions in your code.

```
Note: This markdown assumes there are no methods or parameters for the classes and functions, but this might not be the case. Please update the document accordingly if there are any methods or parameters.


## Configuration 

This section provides detailed information about the available configuration options, file formats, environment variables, default values, and examples.

### 1. Available Configuration Options

The configuration options are available in the following files:

- `.env`: This is the main configuration file for the project.
- `.env.example`: This is the example configuration file for the project. Its content is empty by default, it's intended to be filled with your own configurations.

### 2. Configuration File Formats

Both `.env` and `.env.example` files are in the [dotenv](https://github.com/motdotla/dotenv) format. The dotenv file format is simple, each line represents a key-value pair in the format `KEY=VALUE`.

### 3. Environment Variables

The following environment variables are used:   

- `OPENAI_API_KEY`: This is the key for the OpenAI API. It should be of the format `sk-proj-...`.
- `OPENAI_MODEL`: This is the model to be used for generating AI content. By default, it's set to `gpt-4`.
- `DEFAULT_OUTPUT_FILE`: This is the name of the output file for documentation. By default, it's set to `DOCUMENTATION.md`.

### 4. Default Values

Here are the default values for the environment variables:

- `OPENAI_API_KEY`: There is no default value, you should provide your own key.
- `OPENAI_MODEL`: The default value is `gpt-4`.
- `DEFAULT_OUTPUT_FILE`: The default value is `DOCUMENTATION.md`.

### 5. Configuration Examples

```




```markdown
## Development

### Development Setup

To set up the development environment, follow these steps:

1. Clone the repository: `git clone <repository-url>`.
2. Change to the project directory: `cd <project-folder>`.
3. Install dependencies using the requirements file: `pip install -r requirements.txt`.
4. Set up any environment variables in a `.env` file.

### Code Structure and Conventions

The project is structured as follows:

- **.git/**: Contains Git history and configuration.
- **.gitignore**: Lists files and directories that are ignored by Git.
- **gitdocify.egg-info/**: Contains metadata for the Python package.
- **LICENSE**: Contains the project's license.
- **requirements.txt**: Lists project dependencies.
- **setup.py**: Script for installing the project.
- **src/**: The main source code directory.
  - **analyzer.py**: Contains the analyzer module.
  - **generator.py**: Contains the generator module.
  - **main.py**: The main entry point of the project.
  - **utils.py**: Contains utility functions.
- **test.md**: A markdown file for testing.

For coding conventions, we use [PEP 8](https://www.python.org/dev/peps/pep-0008/) as a style guide for Python code.

### Testing Approach

We have 3 test files in this project. Always write test cases for new code, and ensure all tests pass before committing any changes. Use Python's built-in `unittest` library for writing the tests.

### Contributing Guidelines

1. Fork the repository and create your branch from `master`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Build and Deployment Process

The project's build script is `setup.py`. To build the project, run `python setup.py build`. For deployment, this will depend on the deployment platform, but typically involves pushing the build to a deployment branch or hosting service.
```
