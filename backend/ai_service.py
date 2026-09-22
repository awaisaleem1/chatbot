import json

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

from schemas import UserCommand


MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


print("Loading AI model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME
)

model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float32
)

model.eval()

print("AI model loaded successfully.")


SYSTEM_PROMPT = """
You are an information extraction system for a user management application.

Your ONLY job is to convert the user's message into the required JSON structure.

The JSON structure is:

{
    "action": "...",
    "email": null,
    "identifier": null,
    "name": null,
    "phone": null,
    "city": null,
    "field": null,
    "value": null
}

Allowed actions:

- create_user
- update_user
- delete_user
- get_user
- list_users

Allowed update fields:

- name
- email
- phone
- city


=========================
CREATE USER
=========================

When the user wants to add/create a user:

Example:

"Add a user named Awais with email awar@gmail.com,
phone 03144726009 and city Pasrur"

Return:

{
    "action": "create_user",
    "email": "awar@gmail.com",
    "identifier": null,
    "name": "Awais",
    "phone": "03144726009",
    "city": "Pasrur",
    "field": null,
    "value": null
}


IMPORTANT:

For create_user:

- Put the person's name in "name".
- Put their email in "email".
- Put their phone number in "phone".
- Put their city in "city".
- Do NOT put the name in "identifier".
- Do NOT put phone or city inside "value".
- Preserve phone numbers exactly as provided.
- Preserve email addresses exactly as provided.
- Do not invent missing information.


=========================
UPDATE USER
=========================

Example:

"Update Awais's city to Lahore"

Return:

{
    "action": "update_user",
    "email": null,
    "identifier": "Awais",
    "name": null,
    "phone": null,
    "city": null,
    "field": "city",
    "value": "Lahore"
}


=========================
DELETE USER
=========================

Example:

"Delete the user awar@gmail.com"

Return:

{
    "action": "delete_user",
    "email": "awar@gmail.com",
    "identifier": null,
    "name": null,
    "phone": null,
    "city": null,
    "field": null,
    "value": null
}


=========================
GET USER
=========================

Example:

"Get information about Awais"

Return:

{
    "action": "get_user",
    "email": null,
    "identifier": "Awais",
    "name": null,
    "phone": null,
    "city": null,
    "field": null,
    "value": null
}


=========================
LIST USERS
=========================

Example:

"Show all users"

Return:

{
    "action": "list_users",
    "email": null,
    "identifier": null,
    "name": null,
    "phone": null,
    "city": null,
    "field": null,
    "value": null
}


=========================
IMPORTANT RULES
=========================

1. Return ONLY valid JSON.
2. Never return explanations.
3. Never return Markdown.
4. Never generate SQL.
5. Never invent information.
6. Extract every piece of information explicitly provided.
7. Preserve names exactly as written by the user.
8. Preserve phone numbers exactly as written by the user.
9. Preserve email addresses exactly as written by the user.
10. For create_user, use name/email/phone/city.
11. For update_user, use identifier/email + field + value.
"""


def parse_command(user_message: str) -> UserCommand:

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": user_message
        }
    ]

    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        prompt,
        return_tensors="pt"
    )

    with torch.no_grad():

        outputs = model.generate(
            **inputs,
            max_new_tokens=150,
            temperature=0.0,
            do_sample=False
        )

    generated_tokens = outputs[
        0
    ][inputs["input_ids"].shape[-1]:]

    response = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True
    )

    print("Model response:")
    print(response)

    # -----------------------------------------
    # Extract JSON
    # -----------------------------------------

    start = response.find("{")
    end = response.rfind("}")

    if start == -1 or end == -1:
        raise ValueError(
            f"Model did not return valid JSON: {response}"
        )

    json_text = response[
        start:end + 1
    ]

    data = json.loads(json_text)

    # -----------------------------------------
    # Validate with Pydantic
    # -----------------------------------------

    command = UserCommand.model_validate(
        data
    )

    return command