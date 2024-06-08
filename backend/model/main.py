"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
from datetime import datetime
from pathlib import Path
from threading import Thread

load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

CONFIG = {
    "temperature": 0,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}


def run_models(
    vc_name: str,
    startup_name: str,
    startup_qa: str,
    logfolder: str = "./",
    loops: int = 3,
):
    """Run model interview process.

    <loops> is a variable determining how many cycles of questions and answers will occur between models
    Expects startup_qa to be question answer pairs joined by ;
    """
    startup_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=CONFIG,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction=f"Imagine you are a startup company named {startup_name}, you are interested in securing a fund from a Venture Capitalist (VC), answer the following questions as if you are answering the VC. You must not lie, and you should only generate content based on the data and information given. If you do not have an answer for a question, you should say 'I do not have data or information on this question' and nothing else. Your response will be the final answer given to the VC, hence, there should not be a placeholder for anything",
    )

    vc_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=CONFIG,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction=f"Imagine you are a venture capitalist called {vc_name}, you are interested in investing in a company called {startup_name}, ask questions as if you are interviewing the startup. You will be responded with an answer, either ask a follow up question to clarify further on the answer given, or ask a completely new question based on the list of information you are interested to know.",
    )

    startup_chat_session = startup_model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"For the questions listed below, the company {startup_name} answered in such way. You may gain any data or information from the answers {startup_name} given.",
                    "The format is as follow:",
                    f"Questions 1 ; Answer to Question 1 given by {startup_name}; Question 2 ; Answer to Question 2 given by {startup_name} ; so on",
                    startup_qa,
                    "From now on, answer the prompts as if you are answering a VC",
                ],
            },
        ]
    )

    vc_chat_session = vc_model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"Here is the list of preferences as given by {vc_name}"
                    "Preferred Investment Amount:"  # VC_Q1 Ans
                    "Preferred Startup Industry:"  # VC_Q2 Ans
                    "Preferred Startup Revenue Size:"  # VC_Q3 Ans
                    f"Here is the list of information that {vc_name} is interested to know, you should prioristise asking questions to get these information from {startup_name}",
                    "List of Information: Company Valuation; Company's Vision; Company's Plan for the Next 12 Months; Company's Expansion"  # VC_Q4 Ans
                    "Other than that, whenever a keyword from the following list of keywords are prompted, you should ask a follow up question relevant to the topic of the keyword and relevant to the startup company",
                    "List of Keywords: Budget, Transforming Industries, Expand",  # VC_Q4 Ans
                    "From now on, ask questions as if you are a VC interviewing a startup",
                ],
            },
        ]
    )

    # initiate conversation

    response_vc = vc_chat_session.send_message(
        "Start the conversation by prompting a question to gather information on the startup's expected investment amount, the industry the startup is in, the startup's current revenue size."
    )
    conversation_history = ""
    conversation_history += "VC:\n"
    conversation_history += response_vc.text
    conversation_history += "\n\n"

    response_startup = startup_chat_session.send_message(response_vc.text)
    conversation_history += "Startup:\n"
    conversation_history += response_startup.text
    conversation_history += "\n\n"

    for _ in range(loops):  # Loop the specific amount of times

        response_vc = vc_chat_session.send_message(response_startup.text)

        conversation_history += "VC:\n"
        conversation_history += response_vc.text
        conversation_history += "\n\n"

        response_startup = startup_chat_session.send_message(response_vc.text)
        conversation_history += "Startup:\n"
        conversation_history += response_startup.text
        conversation_history += "\n\n"

    def log_data():
        with open(
            Path(logfolder, datetime.now().strftime("%H-%M-%S")), "a"
        ) as file:
            file.write(conversation_history)

    # start logging the conversation
    writer = Thread(target=log_data)
    writer.start()

    # in the meantime, summarize the convo
    summary = ""

    # join and return
    writer.join()
    return summary
