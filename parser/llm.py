import json
import os
from pathlib import Path

from groq import Groq
from dotenv import load_dotenv

# =====================================
# Config
# =====================================

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "qwen/qwen3-32b"

INPUT_FOLDER = "./"

client = Groq(api_key=API_KEY)


# =====================================
# Prompt Builder
# =====================================

def build_prompt(education, experience):
    return f"""
You are an expert resume parser.

You are given ONLY the Education and Experience sections of a resume.

The parser that generated these sections is imperfect.
Some resumes may have:
- Missing subsection boundaries (everything merged into one subsection)
- Too many subsection boundaries
- Incorrect subsection titles
- Broken subsection keys

Your task is to reconstruct the original Education and Experience entries.

IMPORTANT RULES

1. There may be ZERO, ONE, OR MANY education entries.
2. There may be ZERO, ONE, OR MANY experience entries.
3. Extract ALL entries. Never stop after the first one.
4. Never omit an entry.
5. Never merge two different jobs into one.
6. Never merge two different education records into one.

TEXT PRESERVATION

- Do NOT summarize.
- Do NOT rewrite.
- Do NOT paraphrase.
- Do NOT improve grammar.
- Preserve all information from the input.
- Every piece of information must appear exactly once in the output.
- If a value cannot be assigned to a structured field, include it in the description.

FIELD EXTRACTION

For Experience:

- company
- designation
- start_date
- end_date
- description

For Education:

- degree
- institution
- cgpa
- graduation_date

If a field cannot be confidently determined, leave it as an empty string.

The description field should contain ALL remaining text that does not belong to the structured fields.

OUTPUT FORMAT

Return ONLY valid JSON.

Always return BOTH keys.

{{
    "experience": [
        {{
            "company": "",
            "designation": "",
            "start_date": "",
            "end_date": "",
            "description": ""
        }}
    ],
    "education": [
        {{
            "degree": "",
            "institution": "",
            "cgpa": "",
            "graduation_date": ""
        }}
    ]
}}

Education input:

{json.dumps(education, indent=2)}

Experience input:

{json.dumps(experience, indent=2)}
"""


# =====================================
# Process One Resume
# =====================================

def process_resume(resume: dict) -> dict:
    education = resume.get("education", {})
    experience = resume.get("experience", {})

    prompt = build_prompt(education, experience)

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": "You are an expert CV parser."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    parsed = json.loads(response.choices[0].message.content)

    # Update only these sections
    resume["education"] = parsed.get("education", [])
    resume["experience"] = parsed.get("experience", [])

    return resume
# =====================================
# Process Entire Folder
# =====================================

# folder = Path(INPUT_FOLDER)

# json_files = sorted(folder.glob("*.json"))

# print(f"Found {len(json_files)} JSON files.\n")

# for json_file in json_files:
#     try:
#         process_resume(json_file)
#     except Exception as e:
#         print(f"✗ Failed on {json_file.name}: {e}")

# print("\nDone.")