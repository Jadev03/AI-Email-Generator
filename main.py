from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt=PromptTemplate(
    input_variables=["purpose","tone"],
    template="Write an email for the following purpose: {purpose}. The tone of the email should be {tone}. keep it clear and concise as short as possible "
)

chain=prompt|llm
response=chain.invoke({"purpose":"requesting a meeting with a potential client","tone":"professional"})
print("--------")
print(response.content)
print("--------")
