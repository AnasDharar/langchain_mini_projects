from langchain_google_genai import ChatGoogleGenerativeAI
import os
import subprocess

changed_files = subprocess.check_output(
    ["git", "diff", "--cached", "--name-only"]
).decode().splitlines()

python_files = [f for f in changed_files if f.endswith(".py")]

print(python_files)