import os

import pandas as pd

from main import generate_email

# Load dataset
dataset = pd.read_csv("Datasets/email_evaluation_dataset.csv")
os.makedirs("reports", exist_ok=True)

total_emails = len(dataset)
outputs = []

print("=" * 60)
print("Starting Email Evaluation")
print(f"Total Emails to Generate: {total_emails}")
print("=" * 60)

for index, row in dataset.iterrows():

    print(f"[{index + 1}/{total_emails}] Generating email...", end=" ")

    email = generate_email(
        purpose=row["purpose"],
        tone=row["tone"],
        recipient_name=row["recipient_name"],
        sender_name="Alice Smith",
        sender_email="alice@example.com",
        recipient_email="john@example.com",
        additional_details=row["additional_details"]
    )

    outputs.append({
    "id": row["id"],
    "category": row["category"],
    "purpose": row["purpose"],
    "tone": row["tone"],
    "recipient_name": row["recipient_name"],
    "additional_details": row["additional_details"],
    "generated_email": email
})

    print("✓")

# Save outputs
output_df = pd.DataFrame(outputs)

output_df.to_csv(
    "outputs/generated_outputs.csv",
    index=False
)

print("\n" + "=" * 60)
print("Evaluation Completed Successfully")
print(f"Generated Emails : {len(outputs)}/{total_emails}")
print("Output File      : outputs/generated_outputs.csv")
print("=" * 60)