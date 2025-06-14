import requests
import json
import ast
import resume.api_cred as api_cred

def generate_text(prompt, model="gemini-2.5-flash-preview-05-20"):    #"gemini-2.0-flash" "gemini-2.0-pro-exp-02-05" "gemini-2.5-flash-preview-05-20"
    """
    Generates text using the Gemini API.

    Args:
        prompt: The text prompt to send to the API.
        model: The name of the Gemini model to use (e.g., "gemini-1.5-flash").

    Returns:
        The generated text, or None if an error occurs.
    """

    # api_key = os.environ.get("GEMINI_API_KEY") # Get the API key from environment variables

    # if not api_key:
    #     raise ValueError("GEMINI_API_KEY environment variable not set.")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_cred.api_key}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        status = response.status_code
        if not response.ok:
            return None, status
        
        response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
        response_json = response.json()

        # Extract the generated text. The structure of the response might vary, so handle it carefully.
        if "candidates" in response_json and response_json["candidates"]:
            if "content" in response_json["candidates"][0] and "parts" in response_json["candidates"][0]["content"]:
                parts = response_json["candidates"][0]["content"]["parts"]
                generated_text = "".join([part.get("text", "") for part in parts])
                return generated_text or None, status
            else:
                 print(f"Unexpected response structure: {response_json}")
                 return None, status
        else:
            print(f"No candidates found in response: {response_json}")
            return None, status

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        if response is not None:
            print(f"Response content: {response.text}") # print the response content for debug
        return None, status
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON response: {e}")
        if response is not None:
            print(f"Response content: {response.text}") # print the response content for debug
        return None, status



def job_technical_skill_with_weightage(text):
    Tech_prompt = text + "\n" + "From this text, identify all technical skills, provide weightage(an integer value out of 10) to them based on their importance in a job description and return the result as a value to a python dictionary, where the first coloumn consists of the skills and the second coloumn consists of the weightage of the corresponding skills. respond with only the code as your response will be directly forwarded to a dictionary variable. Do not provide any explanations or code, only the literal of the dictionary. Do not include any text within parenthesis. Do not combine multiple skill with &."
    generated_text_tech, status_code = generate_text(Tech_prompt)

    print(generated_text_tech)

    if generated_text_tech:
        if generated_text_tech.startswith("```python"):
            generated_text_tech=generated_text_tech[10:-4]        

        # Convert string to list
        skills_list = ast.literal_eval(generated_text_tech)

        print(skills_list)

        return skills_list, status_code
    else:
        
        print("Failed to generate text.")
        return {}, status_code


def job_soft_skill_with_weightage(text):
    Soft_prompt = text + "\n" + "From this text, identify all soft skills, provide weightage(an integer value out of 10) to them based on their importance in a job description and return the result as a value to a python dictionary, where the first coloumn consists of the skills and the second coloumn consists of the weightage of the corresponding skills. respond with only the code as your response will be directly forwarded to a dictionary variable. Do not provide any explanations or code, only the literal of the dictionary. Do not include any text within parenthesis. Do not combine multiple skill with &."
    generated_text_soft, status_code = generate_text(Soft_prompt)

    print(generated_text_soft)

    if generated_text_soft:
        if generated_text_soft.startswith("```python"):
            generated_text_soft=generated_text_soft[10:-4]


        # Convert string to list
        skills_list = ast.literal_eval(generated_text_soft)

        print(skills_list)

        return skills_list, status_code
    else:
        print("Failed to generate text.")
        return {}, status_code


def resume_technical_skill(text):
    resume_tech_prompt = text + "\n" + "From this text, identify all technical skills and return the result as a value to a python list. respond with only the code as your response will be directly forwarded to a list variable. Do not provide any explanations or code, only the literal of the list. Do not include any text within parenthesis. Do not combine multiple skill with &."

    generated_text_tech, status_code = generate_text(resume_tech_prompt)
    print(generated_text_tech)


    if generated_text_tech:
        if generated_text_tech.startswith("```python"):
            generated_text_tech = generated_text_tech[10:-4]
        

        # Convert string to list
        skills_list = ast.literal_eval(generated_text_tech)
        print(skills_list)


        return skills_list, status_code
    else:
        print("Failed to generate text.")
        return [], status_code


def resume_soft_skill(text):
    resume_soft_prompt=text + "\n" + "From this text, identify all soft skills and return the result as a value to a python list. respond with only the code as your response will be directly forwarded to a list variable. Do not provide any explanations or code, only the literal of the list. Do not include any text within parenthesis. Do not combine multiple skill with &."
    generated_text_soft, status_code = generate_text(resume_soft_prompt)

    print(generated_text_soft)

    if generated_text_soft:
        if generated_text_soft.startswith("```python"):
            generated_text_soft=generated_text_soft[10:-4]
        

        # Convert string to list
        skills_list = ast.literal_eval(generated_text_soft)
        print(skills_list)

        return skills_list, status_code
    
    else:
        print("Failed to generate text.")
        return [], status_code


def suggestion(resume_text, all_unmatched_skill):
    suggestion_prompt = resume_text + "\n\n" + "this is a resume text and giving some unmatched skills which are present in job description but not in resume,"+ "\n\n" + all_unmatched_skill + "\n\n" + "read the resume and suggest me how to add these keyword in the resume, do not rewrite the resume with new keyword, just give me the updated line or made a new line based on the resume given, also can give me some suggention"

    generated_suggestion_prompt, status_code = generate_text(suggestion_prompt)

    print(generated_suggestion_prompt)
    print(type(generated_suggestion_prompt))

    if generated_suggestion_prompt:
        return generated_suggestion_prompt, status_code
    else:
        blank_string=""
        return blank_string, status_code
