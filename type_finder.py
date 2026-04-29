# Load environment variables from .env file
# Define a Pydantic model for structured output, expecting a list of strings
# Initialize a Pydantic output parser for the defined model
# Method 1: Parser-driven structured output
# Create a prompt template that includes instructions for the output format
# Initialize a Google Generative AI chat model
# Create a chain for Method 1: prompt -> model -> parser
# Method 2: Model-driven structured output
# Create a simple prompt template
# Create a structured version of the model that automatically handles parsing and formatting
# Create a chain for Method 2: prompt -> structured_model
# Alternative Groq model (commented out)
# Explanation of the two methods
# Get user input for the item to find subtypes for
# Get user choice between Method 1 and Method 2
# Execute the chosen method and get the result
# Print the result
# Print the type of the result

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