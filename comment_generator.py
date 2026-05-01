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

Generate ONLY comments for the provided code explaining what it does.
DO NOT include any code, imports, or function definitions.
ONLY return Python comments starting with # or '''

Rules:
- ONLY return Python comments (lines starting with # or multi-line comments with ''')
- DO NOT return any Python code
- DO NOT return imports or function definitions
- DO NOT use markdown code blocks (no ```python or ```)
- Keep comments concise and to the point
- Prefer one short line per logical block (about 5-12 words)
- Avoid repetition and obvious statements

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
    
    # Remove any lines that contain code (imports, function definitions, etc)
    lines = result.split('\n')
    comment_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith("'''") or stripped.startswith('"""') or not stripped:
            comment_lines.append(line)
    
    result = '\n'.join(comment_lines).strip()
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
