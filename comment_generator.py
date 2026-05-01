# Imports necessary libraries for AI-powered comment generation, file operations, and system interactions.
# Loads environment variables from a .env file, likely for API keys.
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import subprocess
import sys
from dotenv import load_dotenv

# Defines a function to generate documentation comments for Python code using a language model.
# It initializes the AI model, sets up a prompt for comment generation, and uses a Langchain chain to process the code.
# The function returns the generated comments, cleaned of any markdown formatting.
def get_comment(code: str):
    load_dotenv()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )

    prompt = PromptTemplate(
        template="""
You are a Python documentation assistant.

Generate concise comments for the whole code explaining what it does.
NOT TO tell what is being imported, algorithm used, etc. stuff.
Explain what is the core functionality of the code.
DO NOT RETURN CODE, ONLY COMMENTS

Rules:
- Return ONLY valid Python comments
- DO NOT RETURN PYTHON CODE, ONLY SUMMARY OF CODE IN THE FORM OF VALID COMMENTS
- Keep comments concise

Code:
{code}
""",
        input_variables=["code"]
    )

    parser = StrOutputParser()
    chain = prompt | model | parser

    result = chain.invoke({"code": code})

    # Remove accidental markdown wrappers
    result = result.replace("", "").replace("", "").strip()
    
    return result

# Defines a function to clean Python code by removing existing comments and import statements.
# It identifies the first import statement and returns the code starting from that point, effectively stripping leading comments.
def remove_comments(code: str):
    lines = code.splitlines()

    first_import_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("import ") or stripped.startswith("from "):
            first_import_index = i
            break

    cleaned_code = "\n".join(lines[first_import_index:])
    return cleaned_code

# Retrieves the remote and local commit hashes from command-line arguments.
remote_commit = sys.argv[1]
local_latest = sys.argv[2]

# Determines the list of changed files using Git commands.
# If the remote commit is a placeholder (e.g., "000000"), it lists all files in the repository.
# Otherwise, it lists files changed between the specified remote and local commits.
if remote_commit.startswith("000000"):
    changed_files = subprocess.check_output(
        ["git", "ls-files"]
    ).decode().splitlines()
else:
    changed_files = subprocess.check_output(
        ["git", "diff", remote_commit, local_latest, "--name-only"]
    ).decode().splitlines()

# Filters the list of changed files to include only those with a .py extension.
python_files = [f for f in changed_files if f.endswith(".py")]

# Prints the list of Python files that will be processed for comment generation.
print("Python files to be commented:", python_files)

# Iterates through each identified Python file.
for file in python_files:
    # Checks if the file exists before proceeding.
    if os.path.exists(file):

        # Reads the content of the Python file.
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        # Removes any existing comments or leading code from the file content.
        code = remove_comments(code)

        # Generates new documentation comments for the cleaned code using the AI model.
        comment = get_comment(code)
        print("Comments generated for ", file, "editing it now")
        # Combines the generated comments with the original code content.
        new_data = comment + "\n\n" + code

        # Overwrites the original file with the new content, including the generated comments.
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_data)

        # Prints a confirmation message indicating that the file has been updated.
        print(f"Updated {file}")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import subprocess
import sys
from dotenv import load_dotenv

# Function to generate documentation comments for a given Python code string.
# Loads environment variables, initializes the Gemini AI model, defines a prompt template for comment generation,
# sets up an output parser, and creates a Langchain chain to invoke the model.
# It then invokes the chain with the provided code and cleans up the generated comments by removing markdown wrappers.
def get_comment(code: str):
    load_dotenv()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )

    prompt = PromptTemplate(
        template="""
You are a Python documentation assistant.

Generate concise comments for the whole code explaining what it does.
NOT TO tell what is being imported, algorithm used, etc. stuff.
Explain what is the core functionality of the code.
DO NOT RETURN CODE, ONLY COMMENTS

Rules:
- Return ONLY valid Python comments
- DO NOT RETURN PYTHON CODE, ONLY SUMMARY OF CODE IN THE FORM OF VALID COMMENTS
- Keep comments concise

Code:
{code}
""",
        input_variables=["code"]
    )

    parser = StrOutputParser()
    chain = prompt | model | parser

    result = chain.invoke({"code": code})

    # Remove accidental markdown wrappers
    result = result.replace("", "").replace("", "").strip()
    
    return result

# Function to remove existing comments and imports from Python code.
# It splits the code into lines, finds the index of the first import statement,
# and returns the code starting from that import statement, effectively removing leading comments and older imports.
def remove_comments(code: str):
    lines = code.splitlines()

    first_import_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("import ") or stripped.startswith("from "):
            first_import_index = i
            break

    cleaned_code = "\n".join(lines[first_import_index:])
    return cleaned_code

# Retrieves the remote commit hash and local latest commit hash from command-line arguments.
remote_commit = sys.argv[1]
local_latest = sys.argv[2]

# Determines the list of changed files based on the commit information.
# If the remote commit is a placeholder (starts with "000000"), it lists all files in the repository.
# Otherwise, it lists files changed between the remote commit and the local latest commit.
if remote_commit.startswith("000000"):
    changed_files = subprocess.check_output(
        ["git", "ls-files"]
    ).decode().splitlines()
else:
    changed_files = subprocess.check_output(
        ["git", "diff", remote_commit, local_latest, "--name-only"]
    ).decode().splitlines()

# Filters the list of changed files to include only Python files.
python_files = [f for f in changed_files if f.endswith(".py")]

# Prints the list of Python files that will be processed for comment generation.
print("Python files to be commented:", python_files)

# Iterates through each identified Python file.
for file in python_files:
    # Checks if the file exists before attempting to process it.
    if os.path.exists(file):

        # Reads the content of the Python file.
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        # Removes any previously generated comments or leading code from the file.
        code = remove_comments(code)

        # Generates new documentation comments for the cleaned code using the AI model.
        comment = get_comment(code)
        print("Comments generated for ", file, "editing it now")
        # Combines the generated comments with the original code.
        new_data = comment + "\n\n" + code

        # Overwrites the file with the new content including the generated comments.
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_data)

        # Prints a confirmation message indicating that the file has been updated.
        print(f"Updated {file}")

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
import subprocess
import sys
from dotenv import load_dotenv


def get_comment(code: str):
    load_dotenv()
    model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite"
    )

    prompt = PromptTemplate(
        template="""
You are a Python documentation assistant.

Generate concise comments for the whole code explaining what it does.

Rules:
- Return ONLY valid Python comments
- DO NOT RETURN PYTHON CODE, ONLY SUMMARY OF CODE IN THE FORM OF VALID COMMENTS
- Keep comments concise

Code:
{code}
""",
        input_variables=["code"]
    )

    parser = StrOutputParser()
    chain = prompt | model | parser

    result = chain.invoke({"code": code})

    # Remove accidental markdown wrappers
    result = result.replace("```python", "").replace("```", "").strip()
    
    return result


def remove_comments(code: str):
    lines = code.splitlines()

    first_import_index = 0

    for i, line in enumerate(lines):
        stripped = line.strip()

        if stripped.startswith("import ") or stripped.startswith("from "):
            first_import_index = i
            break

    cleaned_code = "\n".join(lines[first_import_index:])
    return cleaned_code


remote_commit = sys.argv[1]
local_latest = sys.argv[2]


if remote_commit.startswith("000000"):
    changed_files = subprocess.check_output(
        ["git", "ls-files"]
    ).decode().splitlines()
else:
    changed_files = subprocess.check_output(
        ["git", "diff", remote_commit, local_latest, "--name-only"]
    ).decode().splitlines()


python_files = [f for f in changed_files if f.endswith(".py")]

print("Python files to be commented:", python_files)


for file in python_files:
    if os.path.exists(file):

        # Read file
        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        # Remove previous generated comments
        code = remove_comments(code)

        # Generate new comments
        comment = get_comment(code)
        print("Comments generated for ", file, "editing it now")
        # Add fresh comments
        new_data = comment + "\n\n" + code

        # Overwrite file properly
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_data)

        print(f"Updated {file}")