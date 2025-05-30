
import openai
import os

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def compare_campaigns_with_ai(current_summary, previous_summary, benchmark_summary):
    prompt = f"""
Compare the following marketing campaign performance summaries. Point out improvements, underperforming channels, and recommend changes.

Current Campaign:
{current_summary}

Previous Campaign:
{previous_summary}

Benchmark:
{benchmark_summary}

Give a concise analysis and improvement plan.
"""
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()
