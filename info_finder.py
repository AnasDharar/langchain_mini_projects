from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from pydantic import BaseModel, Field
from dotenv import load_dotenv

load_dotenv()
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

