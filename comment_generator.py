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