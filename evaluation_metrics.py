import os
import re
import pandas as pd

# ----------------------------
# Create reports folder if it doesn't exist
# ----------------------------
os.makedirs("reports", exist_ok=True)

# ----------------------------
# Load generated outputs
# ----------------------------
df = pd.read_csv("outputs/generated_outputs.csv")

results = []

# Common email closings
CLOSINGS = [
    "Regards",
    "Best regards",
    "Kind regards",
    "Sincerely",
    "Thanks",
    "Thank you",
    "Warm regards",
    "Respectfully",
    "Best"
]

# ----------------------------
# Evaluate every email
# ----------------------------
for _, row in df.iterrows():

    email = str(row["generated_email"])

    # Subject
    subject_exists = bool(
        re.search(r"^Subject\s*:", email, re.IGNORECASE | re.MULTILINE)
    )

    # Greeting
    greeting_exists = bool(
        re.search(
            r"^(Dear|Hello|Hi)\b",
            email,
            re.IGNORECASE | re.MULTILINE
        )
    )

    # Closing
    closing_exists = any(
        closing.lower() in email.lower()
        for closing in CLOSINGS
    )

    # Signature
    lines = [
        line.strip()
        for line in email.splitlines()
        if line.strip()
    ]

    signature_exists = False

    if len(lines) >= 2:
        signature_exists = len(lines[-1].split()) <= 3

    # Word count
    word_count = len(email.split())

    # Character count
    character_count = len(email)

    # Empty response
    empty_response = len(email.strip()) == 0

    results.append({
        "id": row["id"],
        "category": row["category"],
        "subject_exists": subject_exists,
        "greeting_exists": greeting_exists,
        "closing_exists": closing_exists,
        "signature_exists": signature_exists,
        "word_count": word_count,
        "character_count": character_count,
        "empty_response": empty_response
    })

# ----------------------------
# Save evaluation
# ----------------------------
evaluation_df = pd.DataFrame(results)

evaluation_df.to_csv(
    "reports/rule_based_evaluation.csv",
    index=False
)

# ----------------------------
# Print summary
# ----------------------------
total = len(evaluation_df)

print("=" * 60)
print("Rule-Based Evaluation Summary")
print("=" * 60)

print(f"Total Emails           : {total}")
print(f"Subject Present        : {evaluation_df['subject_exists'].sum()}/{total}")
print(f"Greeting Present       : {evaluation_df['greeting_exists'].sum()}/{total}")
print(f"Closing Present        : {evaluation_df['closing_exists'].sum()}/{total}")
print(f"Signature Present      : {evaluation_df['signature_exists'].sum()}/{total}")
print(f"Empty Responses        : {evaluation_df['empty_response'].sum()}/{total}")
print(f"Average Word Count     : {evaluation_df['word_count'].mean():.1f}")
print(f"Average Character Count: {evaluation_df['character_count'].mean():.1f}")

print("\nDetailed report saved to:")
print("reports/rule_based_evaluation.csv")

