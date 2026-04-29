# Imports necessary libraries for LLM interactions, prompt management, and data parsing.
# Loads environment variables, likely for API keys.

# Defines a Pydantic model to structure the expected output: a list of strings.
class OutputFormat(BaseModel):
    sub_types: list[str] = Field(description="Write 5 top subtypes of the specific thing that the user wants")

# Initializes a Pydantic output parser to handle structured output from the LLM based on the OutputFormat model.
parser = PydanticOutputParser(pydantic_object=OutputFormat)

# --- Method 1: Parser-Driven Structured Output ---
# Creates a prompt template that includes instructions for the LLM to provide subtypes and format them according to the parser's instructions.
prompt1 = PromptTemplate(
    template="""Tell me 5 subtypes of the following thing: {thing}
    
    {format_instructions}
    """,
    input_variables=['thing'],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
# Initializes a Google Generative AI chat model.
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)
# Creates a LangChain chain combining the modified prompt, the LLM, and the parser for structured output.
chain1 = prompt1 | model | parser

# --- Method 2: Model-Driven Structured Output ---
# Creates a simpler prompt template asking for subtypes without explicit formatting instructions.
prompt2 = PromptTemplate(
    template="""Tell me 5 subtypes of the following thing: {thing}""",
    input_variables=['thing'],
)
# Reconfigures the existing LLM to directly output structured data according to the OutputFormat model.
structured_model = model.with_structured_output(OutputFormat)

# Creates a LangChain chain combining the simple prompt and the model configured for structured output. The model itself handles parsing.
chain2 = prompt2 | structured_model

# Example of another LLM model that could be used (commented out).
# model2 = ChatGroq(
#     model="llama-3.1-8b-instant"
# )

# Explains that there are two primary methods demonstrated for achieving structured output: modifying the prompt or modifying the model.

# Prompts the user to input the subject for which they want subtypes.
inp = input("What do you want subtypes for? : ")
# Asks the user to choose between Method 1 (A) or Method 2 (B).
choice = input("Enter A for changed prompt with normal model, Enter B for normal prompt with changed model")
# Executes the chosen chain based on user input and stores the result.
if choice=="A":
    result = chain1.invoke({'thing':inp})
else:
    result = chain2.invoke({'thing':inp})
# Prints the structured output obtained from the LLM.
print(result)
# Prints the data type of the result.
print(type(result))

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

class OutputFormat(BaseModel):
    sub_types: list[str] = Field(description="Write 5 top subtypes of the specific thing that the user wants")

parser = PydanticOutputParser(pydantic_object=OutputFormat)

# Method 1 (PARSER DRIVEN STRUCTURED OUTPUT): Use modified prompt with normal model and parser
prompt1 = PromptTemplate(
    template="""Tell me 5 subtypes of the following thing: {thing}
    
    {format_instructions}
    """,
    input_variables=['thing'],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    }
)
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)
chain1 = prompt1 | model | parser

#Method 2 (MODEL DRIVEN STRUCTURED OUTPUT): Use a normal prompt with structured model
prompt2 = PromptTemplate(
    template="""Tell me 5 subtypes of the following thing: {thing}""",
    input_variables=['thing'],
)
# No need to instantiat the model again, directly making structured model
structured_model = model.with_structured_output(OutputFormat)

# No need of parser here. with_structured_output handles parsing and formatting on itself
chain2 = prompt2 | structured_model

#Another model that can be used
# model2 = ChatGroq(
#     model="llama-3.1-8b-instant"
# )

# The point is, there are two ways to do the same thing, modifying different things. Try whichever you feel good

inp = input("What do you want subtypes for? : ")
choice = input("Enter A for changed prompt with normal model, Enter B for normal prompt with changed model")
if choice=="A":
    result = chain1.invoke({'thing':inp})
else:
    result = chain2.invoke({'thing':inp})
print(result)
print(type(result))