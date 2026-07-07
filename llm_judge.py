import os
import pandas as pd

from dotenv import load_dotenv
from pydantic import BaseModel, Field

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

load_dotenv()

# ==========================================================
# Judge Model Configuration
# ==========================================================

JUDGE_MODEL = "deepseek/deepseek-chat-v3-0324"
JUDGE_TEMPERATURE = 0.0

judge_llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    model=JUDGE_MODEL,
    temperature=JUDGE_TEMPERATURE,
)

# ==========================================================
# Output Schema
# ==========================================================

class EmailEvaluation(BaseModel):

    instruction_following: int = Field(description="Score from 1 to 5")
    professional_tone: int = Field(description="Score from 1 to 5")
    grammar_fluency: int = Field(description="Score from 1 to 5")
    completeness: int = Field(description="Score from 1 to 5")
    conciseness: int = Field(description="Score from 1 to 5")
    naturalness: int = Field(description="Score from 1 to 5")
    hallucination: int = Field(description="Score from 1 to 5")
    overall_quality: int = Field(description="Score from 1 to 5")
    feedback: str = Field(description="Short explanation")


parser = JsonOutputParser(pydantic_object=EmailEvaluation)

# ==========================================================
# Prompt
# ==========================================================

judge_prompt = PromptTemplate(
    input_variables=[
        "purpose",
        "tone",
        "recipient_name",
        "additional_details",
        "generated_email"
    ],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
    template="""
You are an expert evaluator of professional internal business emails.

Your task is to evaluate the generated email according to the user's request.

==========================
User Request
==========================

Purpose:
{purpose}

Tone:
{tone}

Recipient:
{recipient_name}

Additional Details:
{additional_details}

==========================
Generated Email
==========================

{generated_email}

==========================
Evaluation Criteria
==========================

Score every criterion from 1 to 5.

1 = Very Poor
2 = Poor
3 = Acceptable
4 = Good
5 = Excellent

Evaluate:

1. Instruction Following
2. Professional Tone
3. Grammar & Fluency
4. Completeness
5. Conciseness
6. Naturalness
7. Hallucination
8. Overall Quality

Provide one short feedback sentence.

{format_instructions}
"""
)

judge_chain = judge_prompt | judge_llm | parser

# ==========================================================
# Evaluate One Email
# ==========================================================

def evaluate_email(
    purpose,
    tone,
    recipient_name,
    additional_details,
    generated_email,
):

    return judge_chain.invoke({
        "purpose": purpose,
        "tone": tone,
        "recipient_name": recipient_name,
        "additional_details": additional_details,
        "generated_email": generated_email
    })


# ==========================================================
# Run Evaluation
# ==========================================================

os.makedirs("reports", exist_ok=True)

df = pd.read_csv("outputs/generated_outputs.csv")

results = []

total = len(df)

print("=" * 60)
print("LLM Evaluation Started")
print("=" * 60)

for index, row in df.iterrows():

    print(f"[{index + 1}/{total}] Evaluating...", end=" ")

    try:

        score = evaluate_email(
            purpose=row["purpose"],
            tone=row["tone"],
            recipient_name=row["recipient_name"],
            additional_details=row["additional_details"],
            generated_email=row["generated_email"]
        )

        score["id"] = row["id"]
        score["category"] = row["category"]

        results.append(score)

        print("✓")

    except Exception as e:

        print("✗")
        print(e)

evaluation_df = pd.DataFrame(results)

evaluation_df.to_csv(
    "reports/llm_evaluation.csv",
    index=False
)

print("\n" + "=" * 60)
print("LLM Evaluation Completed")
print(f"Evaluated : {len(results)}/{total}")
print("Report    : reports/llm_evaluation.csv")
print("=" * 60)