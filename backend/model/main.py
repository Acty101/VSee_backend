"""
Install the Google AI Python SDK

$ pip install google-generativeai

See the getting started guide for more information:
https://ai.google.dev/gemini-api/docs/get-started/python
"""

import google.generativeai as genai
from dotenv import load_dotenv
import os
import re
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
    vc_qa: list,
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

    summ_model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=CONFIG,
        # safety_settings = Adjust safety settings
        # See https://ai.google.dev/gemini-api/docs/safety-settings
        system_instruction=f"Imagine you are a Venture Capitalist (VC) analyst, your company, {vc_name} is interested in investing in a startup company called {startup_name}, your boss would like to know more about the company to make an informed decision on whether to proceed with the next round of company evaluation. Hence, your job, as an analyst, is to answer all the following questions based on the conversation history.",
    )

    startup_chat_session = startup_model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    f"For the questions listed below, the company {startup_name} answered in such way. You may gain any data or information from the answers {startup_name} given.",
                    "The format is as follows:",
                    f"Question 1 ; Answer to Question 1 given by {startup_name}; Question 2 ; Answer to Question 2 given by {startup_name} ; so on",
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
                    f"Preferred Investment Amount: {vc_qa[1]}",  # VC_Q1 Ans
                    f"Preferred Startup Industry: {vc_qa[3]}",  # VC_Q2 Ans
                    f"Preferred Startup Revenue Size: {vc_qa[5]}",  # VC_Q3 Ans
                    f"Here is the list of information that {vc_name} is interested to know, you should prioristise asking questions to get these information from {startup_name}",
                    f"List of Information: {vc_qa[7]}"  # VC_Q4 Ans
                    "Other than that, whenever a keyword from the following list of keywords are prompted, you should ask a follow up question relevant to the topic of the keyword and relevant to the startup company",
                    f"List of Keywords: {vc_qa[9]}",  # VC_Q5 Ans
                    f"Here are more data on what {vc_name} is looking for in investing",
                    "The format is as follow: ['Question 1','Answer to Question 1 by VC', 'Question 2','Answer to Question 2 by VC'] etc.",
                    *vc_qa,
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

    conversation_history = re.sub(r"\*", "", conversation_history)

    def log_data(text_file):
        with open(text_file, "a") as file:
            file.write(conversation_history)

    # start logging the conversation
    text_file = Path(logfolder, f'{datetime.now().strftime("%H-%M-%S")}.txt')
    writer = Thread(target=log_data, args=(text_file,))
    writer.start()

    summ_chat_session = summ_model.start_chat(
        history=[
            {
                "role": "user",
                "parts": [
                    "Here is the entire conversation history between your VC and the startup company.",
                    conversation_history,
                    f"Here is the list of preference as given by your VC company, {vc_name}",
                    f"Preferred Investment Amount: {vc_qa[1]}",  # VC_Q1 Ans
                    f"Preferred Startup Industry: {vc_qa[3]}",  # VC_Q2 Ans
                    f"Preferred Startup Revenue Size: {vc_qa[5]}",  # VC_Q3 Ans
                    f"Here is the list of information that {vc_name} is interested to know",
                    f"List of Information: {vc_qa[7]}",  # VC_Q4 Ans
                    f"Here is the list of keywords {vc_name} is looking for"
                    f"List of Keywords: {vc_qa[9]}",  # VC_Q5 Ans
                    f"Here are more data on what {vc_name} is looking for in investing",
                    "The format is as follow: ['Question 1','Answer to Question 1 by VC', 'Question 2','Answer to Question 2 by VC'] etc.",
                    *vc_qa,
                    f"From now on, answer the prompts as if you are an analyst for {vc_name}",
                ],
            },
        ]
    )

    summ_history = ""

    summ_history += "\n Match Analysis Report ==========\n"

    response_summ = summ_chat_session.send_message(
        "Compare your VC's preferences with the information gathered from the startup, determine if it is a good match based on the differences"
    )

    summ_history += response_summ.text

    summ_history += "\n\n Summary Report ==========\n"

    response_summ = summ_chat_session.send_message(
        "Generate a summary of the conversation history, focusing mainly on the information that your VC is interested to know. The summarized content should be around one fifth the length of the original conversation"
    )

    summ_history += response_summ.text

    summ_history += "\n\n Market Analysis ==========\n"

    response_summ = summ_chat_session.send_message(
        "Considering the current market trends and the history of similar startups, provide a 100-word analysis of this investment opportunity."
    )

    summ_history += response_summ.text

    summ_history += (
        "\n\n Recommendation for Further Clarification ==========\n"
    )

    response_summ = summ_chat_session.send_message(
        "Assume that your VC has decided to proceed to the next round, based on the conversation, suggest 3 questions that we should clarify with the startup in the next round to gather information that we were not able to gather through the conversation history. For example, questions that the startup do not have data for should be a good question to clarify in the next round."
    )

    summ_history += response_summ.text

    summ_history = re.sub(r"\*", "", summ_history)

    # join and return
    writer.join()
    return summ_history, text_file
