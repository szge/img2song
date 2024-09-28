import os
import google.generativeai as genai
from google.ai.generativelanguage_v1beta.types import content
import json
from activities import Activity

with open("config.json", "r") as f:
    config = json.load(f)
    gemini_api_key = config.get("gemini_api_key")
genai.configure(api_key=gemini_api_key)


def upload_to_gemini(path, mime_type=None):
    file = genai.upload_file(path, mime_type=mime_type)
    print(f"Uploaded file '{file.display_name}' as: {file.uri}")
    return file


generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_schema": content.Schema(
        type=content.Type.OBJECT,
        properties={
            "activity": content.Schema(
                type=content.Type.STRING,
            ),
        },
    ),
    "response_mime_type": "application/json",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config,
    # safety_settings = Adjust safety settings
    # See https://ai.google.dev/gemini-api/docs/safety-settings
)


def get_activity_from_image(image_path: str) -> Activity:
    file = upload_to_gemini(image_path, mime_type="image/png")

    activity_list = ", ".join([activity.name for activity in Activity])

    prompt = f"What activity is shown in this image? Choose from: [{activity_list}]. Respond with just the activity name."
    # print(prompt)
    
    response = model.generate_content([
        file,
        "\n\n",
        prompt,
    ])
    try:
        response_json = json.loads(response.text)
        activity = Activity[response_json["activity"]]
    except (json.JSONDecodeError, KeyError):
        activity = Activity.NONE_OF_THE_ABOVE
    return activity


if __name__ == "__main__":
    activity = get_activity_from_image("./test_imgs/coding.png")
    print(activity)
