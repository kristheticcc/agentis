from models import ParsedProfile
from clients import openai, gpt_model

system_prompt = """Extract the user details from the text completely and accurately.
                 If information is explicitly provided, extract it. If it is not provided, use None. 
                 Only infer a value when it is strongly and directly supported by the patient's information. 
                 Do not assume that omitted information means the patient does not have that history.
                 for any list or boolean field: if the patient's text does not mention that topic at all, output None; 
                 if the text explicitly states its absence, output False or an empty list"""

def profile_parser(text):
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": text},
    ]

    response = openai.responses.parse(
        model = gpt_model,
        input = messages,
        text_format = ParsedProfile,
    )

    return response.output_parsed