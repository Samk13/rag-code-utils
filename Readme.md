![License](https://img.shields.io/github/license/mashape/apistatus.svg)

# RAG Code Utils

## RAG Py Context Miner

This tool is designed to extract the inheritance tree of a specified class and save it in a file. It searches for the class or function within the specified path and the provided virtual environment, extracting the relevant code from the repository. This process enhances the efficiency of RAG applications by providing the essential code context.

The purpose of this tool is to furnish RAG with the minimal code context necessary to deliver accurate responses to queries about code snippets pertaining to the given class, without providing the entire codebase.

## Usage

provide the following variables to the function in `.env` file or as arguments to the script:

* Class or function to extract code for
`TARGET = 'your_target_class_or_function'`

* Path to the virtual environment to search for the target class or function
`VENV_PATH = 'path/to/venv'`

* Output file to write the extracted code
`OUTPUT_FILE = 'path/to/output/file'`

* Path to the repository to search for the target class or function
`REPO_PATH = 'path/to/repo'`

You either run the script with the following arguments:

```bash
python main.py -t TARGET -v VENV_PATH -o OUTPUT_FILE -r REPO_PATH
# the following arguments are required: -t/--target, -v/--venv, -o/--output, -r/--repo
```

You still can provide the `-t` argument to change your class target.
