from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

load_dotenv()

def get_llm(provider="gemini"):
    if provider == "gemini":
        return ChatGoogleGenerativeAI(
            model="gemini-2.5-flash"
        )

    elif provider == "groq":
        return ChatGroq(
            model="llama-3.3-70b-versatile"
        )

    else:
        raise ValueError("Unknown provider")
prompt=PromptTemplate(
    input_variables=[
    "purpose",
    "tone",
    "recipient_name",
    "sender_name",
    "sender_email",
    "recipient_email",
    "additional_details"
                        ],
    validate_template=True,
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

llm = get_llm("groq")
chain = prompt | llm
# response = chain.invoke({
#     "purpose": "Request a salary increase based on recent performance and additional responsibilities.",
#     "tone": "Professional",
#     "recipient_name": "John Doe",
#     "sender_name": "Alice Smith",
#     "sender_email": "alice.smith@example.com",
#     "recipient_email": "john.doe@example.com",
#      "additional_details": ""
# })

# print("--------")
# print(response.content)
# print("--------")
def generate_email(
    purpose,
    tone,
    recipient_name,
    sender_name,
    sender_email,
    recipient_email,
    additional_details=""
):
    response = chain.invoke({
        "purpose": purpose,
        "tone": tone,
        "recipient_name": recipient_name,
        "sender_name": sender_name,
        "sender_email": sender_email,
        "recipient_email": recipient_email,
        "additional_details": additional_details
    })

    return response.content


def prompt_for_input(label, default=""):
    if default:
        value = input(f"{label} [{default}]: ").strip()
        return value or default

    return input(f"{label}: ").strip()


def collect_email_details():
    print("\nAI Email Generator")
    print("-------------------")
    print("Enter the details below. Press Enter to accept a suggested default where shown.\n")

    return {
        "purpose": prompt_for_input("Purpose of the email"),
        "tone": prompt_for_input("Tone", "Professional"),
        "recipient_name": prompt_for_input("Recipient name"),
        "sender_name": prompt_for_input("Sender name"),
        "sender_email": prompt_for_input("Sender email"),
        "recipient_email": prompt_for_input("Recipient email"),
        "additional_details": prompt_for_input("Additional details (optional)"),
    }


def main():
    details = collect_email_details()
    print("\nGenerating email...\n")
    email = generate_email(**details)
    print(email)


if __name__ == "__main__":
    main()
