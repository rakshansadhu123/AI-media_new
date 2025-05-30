
import openai
import os

# You can replace this later with Azure, Ollama, or LangChain API setup
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def compare_campaigns_with_ai(current_data, previous_data, benchmark_data=None):
    """
    Accepts stringified summaries or structured JSON-like data of:
    - current_data: current campaign summary
    - previous_data: previous campaign summary
    - benchmark_data: optional benchmark metrics
    Returns an AI-generated comparison and recommendations.
    """

    prompt = f"""
    You are a media performance analyst. Below are two campaign summaries and optional benchmarks.

    Current Campaign:
    {current_data}

    Previous Campaign:
    {previous_data}

    Benchmark (if any):
    {benchmark_data if benchmark_data else 'N/A'}

    Tasks:
    1. Compare the performance (e.g., spend, ROAS, CPM) between current and previous campaigns.
    2. Highlight what improved or declined.
    3. Identify any media types or channels underperforming benchmarks.
    4. Suggest specific actions or optimizations for future campaigns.

    Provide your response as a structured summary with clear headings.
    """

    try:
        response = openai.ChatCompletion.create(
            model=OPENAI_MODEL,
            api_key=OPENAI_API_KEY,
            messages=[
                {"role": "system", "content": "You are a helpful data analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=800
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"⚠️ AI comparison failed: {e}"
