# Loads environment variables for API keys.
# Initializes a Google Generative AI chat model.
# Defines a prompt template for comment generation.
# Creates a chain to process code through the model.
# Invokes the chain to generate documentation comments.

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
You are a Python documentation comment assistant.

Task:
Generate comments that explain the core behavior of the given Python code.

Priority Rules (highest to lowest):
1. Output format: Return ONLY Python single-line comments that start with #.
2. No code: Do NOT output code, imports, function/class definitions, or markdown.
3. Length limit: Return at most 5 comment lines total.
4. Brevity: Keep each line concise and to the point (roughly 5-12 words).
5. Quality: Focus on core logic, avoid repetition, and skip obvious statements.
6. Clarity: Use plain, direct language.

Code:
{code}
""",
        input_variables=["code"]
    )

    parser = StrOutputParser()
    chain = prompt | model | parser

    result = chain.invoke({"code": code})

    result = result.replace("```python", "").replace("```", "").strip()
    
    lines = result.split('\n')
    comment_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('#') or stripped.startswith("'''") or stripped.startswith('"""') or not stripped:
            comment_lines.append(line)
    
    result = '\n'.join(comment_lines).strip()
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

        with open(file, "r", encoding="utf-8") as f:
            code = f.read()

        
        code = remove_comments(code)

        
        comment = get_comment(code)
        print("Comments generated for ", file, "editing it now")
        
        new_data = comment + "\n\n" + code

        
        with open(file, "w", encoding="utf-8") as f:
            f.write(new_data)

        
        print(f"Updated {file}")