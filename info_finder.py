# Loads environment variables from a .env file.
# Imports necessary libraries for interacting with Google Generative AI,
# creating prompts, parsing output, defining data models, and loading environment variables.

# Prints a placeholder message.

# Defines a Pydantic model for structured output, expecting a list of strings for subtypes.
# This model is intended for a scenario where only subtype names are needed.

# Defines another Pydantic model for structured output, expecting a dictionary
# to store subtypes as keys and their associated information as values.

# Creates a prompt template to request 5 subtypes of a given 'thing'.

# Initializes the Google Generative AI chat model, specifically using the "gemini-2.5-flash-lite" model.

# Configures the model to output structured data conforming to the OutputFormat Pydantic model.

# Configures the model to output structured data conforming to the OutputFormat2 Pydantic model.

# Creates a prompt template to generate a one-sentence description for a list of 'sub_types'.

# Initializes a string output parser.

# Chains together the prompt, structured model, second prompt, and second structured model
# to first get subtypes and then get information about them.

# Prompts the user to input the 'thing' for which they want subtypes.

# Invokes the defined chain with the user's input to get the structured result.

# Prints the final structured result obtained from the chain.
# Prints the type of the result, which is expected to be OutputFormat2.

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()

print("stuff")

# Here, parser is not used for json. we are using method 2. For more info, visit type_finder.py
class OutputFormat(BaseModel):
    sub_types: list[str] = Field(description="Write 5 top subtypes of the specific thing that the user wants")

class OutputFormat2(BaseModel):
    sub_types_with_info: dict[str,str] = Field(description="Enter the info about each subtypes in this dictionary as in key value pair")
prompt1 = PromptTemplate(
    template="""Tell me 5 subtypes of the following thing: {thing}""",
    input_variables=['thing'],
)
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash-lite"
)
structured_model = model.with_structured_output(OutputFormat)
structured_model2 = model.with_structured_output(OutputFormat2)
prompt2 = PromptTemplate(
    template="Generate 1 sentence info about all these types: {sub_types}",
    input_variables=['sub_types']
)
parser = StrOutputParser()
chain = prompt1 | structured_model | prompt2 | structured_model2

inp = input("What do you want subtypes for? : ")

result = chain.invoke({'thing':inp})

print(result)
print(type(result)) # <class '__main__.OutputFormat2'>