import os
import argparse
from dotenv import load_dotenv
from rag_context_miner.core import mine_context

# Load environment variables from .env file
load_dotenv()

# Setup argparse to handle command-line arguments
parser = argparse.ArgumentParser(description='Extract code context for a specific target from a given repository.')
parser.add_argument('-t', '--target', help='Class or function to extract code for.')
parser.add_argument('-v', '--venv', help='Path to the virtual environment.')
parser.add_argument('-o', '--output', help='Output file to write the extracted code.')
parser.add_argument('-r', '--repo', help='Path to the repository.')

# Parse command-line arguments
args = parser.parse_args()

# Use values from the command line or fallback to .env file
TARGET = args.target if args.target else os.getenv('TARGET')
VENV_PATH = args.venv if args.venv else os.getenv('VENV_PATH')
OUTPUT_FILE = args.output if args.output else os.getenv('OUTPUT_FILE')
REPO_PATH = args.repo if args.repo else os.getenv('REPO_PATH')

if __name__ == "__main__":
    if not all([TARGET, VENV_PATH, OUTPUT_FILE, REPO_PATH]):
        print("All parameters are required. Provide them through command line or .env file.")
    else:
        mine_context(REPO_PATH, TARGET, OUTPUT_FILE, VENV_PATH)
