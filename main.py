from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()
llm=ChatGoogleGenerativeAI(model="gemini-2.5-flash")

prompt=PromptTemplate(
    input_variables=["purpose","tone","whom","sender_email_id","reciver_email_id","sender_name","additional_details"],
    template="""Context
-------
You are an expert business communication assistant.
You write professional internal company emails.

Task
----
Write a complete email based on the provided information.

Input
-----
Purpose: {purpose}
Tone: {tone}
Recipient Name: {recipient_name}
Sender Name: {sender_name}
Sender Email: {sender_email}
Recipient Email: {recipient_email}
Additional Details: {additional_details}

Requirements
------------
- Use natural professional English.
- Keep the email concise.
- If additional details are provided, incorporate them naturally where relevant.
- Do not invent company names.
- Do not invent facts.
- Include an appropriate subject.
- Include greeting, body, closing, and signature.

Output
------
Return only the completed email.
Do not include explanations or Markdown.
"""

)

chain=prompt|llm
response = chain.invoke({
    "purpose": "Request a salary increase based on recent performance and additional responsibilities.",
    "tone": "Professional",
    "recipient_name": "John Doe",
    "sender_name": "Alice Smith",
    "sender_email": "alice.smith@example.com",
    "recipient_email": "john.doe@example.com",
     "additional_details": ""
})

print("--------")
print(response.content)
print("--------")
