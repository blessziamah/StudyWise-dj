import openai
import requests
import json
from pydub import AudioSegment

openai_token = "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"
openai.api_key = openai_token
hf_api_key = "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"

openai_header = {
    "Content-Type": "application/json",
    "Authorization": "Bearer {}".format(openai_token)
}


# audio transcription function
def transcribe_audio_variable(audio_data, model='whisper-1', language='en'):
    headers = {
        'Authorization': f'Bearer {openai_token}'
    }

    # Prepare the payload data
    files = {
        'file': ("audio.wav", audio_data),
        'model': (None, model),
        'language': (None, language)
    }

    transcribed_response = requests.post('https://api.openai.com/v1/audio/transcriptions', headers=headers, files=files)

    # Check if the request was successful
    if transcribed_response.status_code == 200:
        response_data = json.loads(transcribed_response.text)
        transcribed_text = response_data['text']
        return transcribed_text
    else:
        error_message = transcribed_response.text
        return f"API Request Failed with Status Code: {transcribed_response.status_code}\nError Message: {error_message}"


# Clean up function
def clean_up(transcribed_text, model="gpt-3.5-turbo", headers=openai_header):
    prompt = "Your task is to correct any spelling discrepancies in the transcribed text.Only add necessary punctuation such as periods, commas, and capitalization, and use only the context provided. Also review the text and replace any words or phrases that are considered offensive, harmful, or inappropriate with more respectful and safe alternatives. Ensure that the replacements maintain the overall meaning and context of the text."

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"{prompt} {transcribed_text}"
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_header, json=data)
    full_message = json.loads(response.text)

    # Extract and return the corrected text from the model's response
    corrected_text = full_message['choices'][0]['message']['content']
    return corrected_text


# Summarization function
def summarize(corrected_text, model="gpt-3.5-turbo", headers=openai_header):
    summarize_prompt = "Please summarize the text to provide a concise and coherent summary of its content."

    data = {
        "model": model,
        "messages": [
            {
                "role": "user",
                "content": f"{summarize_prompt} {corrected_text}"
            }
        ]
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=openai_header, json=data)
    full_message = json.loads(response.text)

    # Extract and return the cleaned text and summary from the model's response
    summary = full_message['choices'][0]['message']['content']

    return summary


""" # CALLS
# audio transcription
transcribed_text = transcribe_audio_variable(audio_data)
print("INITIAL TEXT:" + transcribed_text)

# text cleanup
corrected_text = clean_up(transcribed_text)
print("CORRECTED TEXT: " + corrected_text)

# Summary
if should_summarize:
    summary = summarize(corrected_text)
    print("SUMMARY: " + summary)
else:
    print("Summarization is not enabled.") """
