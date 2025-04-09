import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

# Load the API key from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please check your .env configuration.")

genai.configure(api_key=api_key)

def generate_quiz(topic):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use a stable model
    except Exception as e:
        print(f"Error initializing model: {e}")
        return None

    prompt = f"""
    Generate a quiz with exactly 8 questions on the topic '{topic}' with the following strict format for each question:
    - "Question": The question number as (1, 2, 3, 4, 5) followed by the question text.
    - "Question_id": the question id for each question from q1 to q5.
    - "Options": A list of 4 multiple-choice options formatted as:
      - A. "option answer 1"
      - B. "option answer 2"
      - C. "option answer 3"
      - D. "option answer 4"
    - "Answer": The index of the correct option (0 for A, 1 for B, 2 for C, 3 for D).

    Return ONLY a valid JSON object containing an array of 8 question objects. Do not include any additional text, explanations, or formatting outside the JSON structure.

    Example output:
    {{
        "questions": [
            {{
                "Question": "1. What is the capital of France?",
                "Question_id": q1,
                "Options": ["A. London", "B. Berlin", "C. Paris", "D. Madrid"],
                "Answer": 2
            }},
            // ... (7 more questions)
        ]
    }}
    """

    try:
        response = model.generate_content(prompt)
        raw_response = response.text if hasattr(response, 'text') else str(response)
        # print(f"Raw response: {raw_response}")  # Debug: Print raw response

        # Remove Markdown code block markers (```json) if present
        raw_response = re.sub(r'^```json\s*|\s*```$', '', raw_response, flags=re.MULTILINE).strip()
        if not raw_response or raw_response.isspace():
            print("Error: Empty or whitespace-only response from API.")
            return None

        quiz_data = json.loads(raw_response)

        # Validate structure
        if not isinstance(quiz_data, dict) or 'questions' not in quiz_data:
            print("Error: Invalid quiz structure")
            return None
        
        questions = quiz_data['questions']
        if not isinstance(questions, list) or len(questions) != 8:
            print(f"Error: Expected 5 questions, got {len(questions)}")
            return None

        # Validate each question
        for idx, q in enumerate(quiz_data['questions'], 1):
            if not all(key in q for key in ['Question', 'Options', 'Answer']):
                print(f"Error in quiz generation: Missing required fields in question {q.get('Question', f'{idx+1}')}")
                return None
            if not isinstance(q['Options'], list) or len(q['Options']) != 4:
                print(f"Error in quiz generation: Invalid options in question {q.get('Question', f'{idx+1}')}")
                return None
            if not isinstance(q['Answer'], int) or q['Answer'] not in [0, 1, 2, 3]:
                print(f"Error in quiz generation: Invalid answer in question {q.get('Question', f'{idx+1}')}")
                return None
            
        answers = {f"q{idx+1}": q["Answer"] for idx, q in enumerate(quiz_data["questions"])}
        path = "templates/quizes/answers.json"
        with open(path, "w") as f:
            json.dump(answers, f, indent=4)
        print(f"Answers saved to answers.json: {answers}")

        questions = {f"q{idx+1}": q["Question_id"] for idx, q in enumerate(quiz_data["questions"])}
        path_1 = "templates/quizes/question.json"
        with open(path_1, "w") as f:
            json.dump(questions, f, indent=4)
        print(f"Answers saved to questions.json: {questions}")
            
        return quiz_data
    
    except json.JSONDecodeError as e:
        print(f"JSON parsing error: {e}. Raw response: {raw_response}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None

if __name__ == "__main__":
    quiz = generate_quiz("python")
    if quiz:
        print("Generated quiz:", quiz)
    else:
        print("Failed to generate quiz.")