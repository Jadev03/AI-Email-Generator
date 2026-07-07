# AI Email Generator

AI Email Generator is a small Python project that uses an LLM to generate professional business emails from a structured set of inputs. It also includes simple rule-based and LLM-based evaluation scripts for comparing generated emails against a sample dataset.

## Features

- Interactive CLI for generating an email from user-entered details.
- `generate_email()` helper for programmatic use.
- Batch generation from a CSV dataset.
- Rule-based evaluation of generated emails.
- LLM-as-judge evaluation using OpenRouter.

## Project Structure

- `main.py` - email generation logic and interactive CLI entry point.
- `evaluate.py` - batch generation from `Datasets/email_evaluation_dataset.csv` into `outputs/generated_outputs.csv`.
- `evaluation_metrics.py` - rule-based checks that write `reports/rule_based_evaluation.csv`.
- `llm_judge.py` - LLM-based scoring that writes `reports/llm_evaluation.csv`.
- `Datasets/` - input dataset used for evaluation.
- `outputs/` - generated email output files.
- `reports/` - evaluation reports.

## Requirements

- Python 3.10 or later recommended.
- An API key for Groq to run the default generator in `main.py` and `evaluate.py`.
- An OpenRouter API key to run `llm_judge.py`.

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root and add the required keys:

```env
GROQ_API_KEY=your_groq_api_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

## Usage

### Generate one email interactively

Run:

```bash
python main.py
```

The script will prompt for:

- purpose
- tone
- recipient name
- sender name
- sender email
- recipient email
- additional details

### Generate emails for the dataset

Run:

```bash
python evaluate.py
```

This reads `Datasets/email_evaluation_dataset.csv` and writes generated emails to `outputs/generated_outputs.csv`.

### Run rule-based evaluation

Run:

```bash
python evaluation_metrics.py
```

This inspects the generated emails and writes the results to `reports/rule_based_evaluation.csv`.

### Run LLM-based evaluation

Run:

```bash
python llm_judge.py
```

This scores the generated emails with an LLM judge and writes the results to `reports/llm_evaluation.csv`.

## Output Files

- `outputs/generated_outputs.csv` - generated emails for each dataset row.
- `reports/rule_based_evaluation.csv` - rule-based evaluation results.
- `reports/llm_evaluation.csv` - LLM judge scores and feedback.

## Notes

- The default generator in `main.py` currently uses Groq with `llama-3.3-70b-versatile`.
- The prompt is designed for concise, professional internal business emails.
- If you change the provider or model in `main.py`, make sure the corresponding environment variables are set.