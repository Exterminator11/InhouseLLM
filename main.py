import streamlit as st
import streamlit.components.v1 as components
from streamlit_option_menu import option_menu
import os
import base64
import streamlit as st
from utils_rachit import generate
import pdfplumber

# from dotenv import load_dotenv
import requests

# import evaluate
import textwrap
from json import dumps

# from langchain.document_loaders import PyPDFLoader, UnstructuredPDFLoader, PyPDFium2Loader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
import graph_utils
import my_utils
import extract_graph as extract_graph
import webbrowser
from pathlib import Path
from streamlit.components.v1 import html


def open_page(url):
    open_script = """
        <script type="text/javascript">
            window.open('%s', '_blank').focus();
        </script>
    """ % (
        url
    )
    html(open_script)


HUGGINGFACE_BACKUP_KEY = "HUGGINGFACE API KEY HERE"


def read_pdf(file):
    data = []
    with pdfplumber.load(file) as pdf:
        pages = pdf.pages
        for p in pages:
            data.append(p.extract_tables())
    return data


def wrap(string, max_width=130):
    return textwrap.fill(string, max_width)


def query_grammar(payload):
    API_URL = "https://api-inference.huggingface.co/models/pszemraj/flan-t5-large-grammar-synthesis"
    headers = {"Authorization": f"Bearer {'KEY HERE'}"}
    print(wrap(payload))
    payload = {"inputs": payload}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        print("\n\nGenerated text: ", wrap(response.json()[0]["generated_text"]))
    except:
        print("\nUnexpected Behaviour:\n")
        print(response.json())
    return response


def query_summary_news(payload):
    API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
    headers = {"Authorization": f"Bearer {'KEY HERE'}"}
    print(wrap(payload))
    payload = {"inputs": payload}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        print("\n\nGenerated text: ", wrap(response.json()[0]["summary_text"]))
    except:
        print("\nUnexpected Behaviour:\n")
        print(response.json())
    return response


def query_summary_scientific(payload):
    API_URL = "https://api-inference.huggingface.co/models/sambydlo/bart-large-scientific-lay-summarisation"
    headers = {"Authorization": f"Bearer {'KEY HERE'}"}
    print(wrap(payload))
    payload = {"inputs": payload}
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        print("\n\nGenerated text: ", wrap(response.json()[0]["summary_text"]))
    except:
        print("\nUnexpected Behaviour:\n")
        print(response.json())
    return response


# *streamlit
st.set_page_config(
    page_title="Closed AI",
    page_icon="wifi_off",
    layout="wide",
    initial_sidebar_state="auto",
)

selected = option_menu(
    menu_title=None,
    options=["News", "Scientific Paper summary", "Grammar", "Upload", "Chat"],
    icons=["newspaper", "option", "spellcheck", "file-pdf-fill"],
    default_index=0,
    orientation="horizontal",
)

if selected == "Grammar":
    st.title("Grammar Checker")
    st.text("Correct your grammar with the help of LLM Technology")
    prompt = st.text_input("What would you like to check?")

    if st.button("Analyze"):
        if prompt:
            print(prompt)
            response = query_grammar(prompt)
            print(response.status_code)
            if response.status_code == 200:
                server_response = response.json()
                print(server_response)
                if server_response:
                    st.write(server_response)
                else:
                    st.write("Sorry our servers are busy")
            elif response.status_code == 503:
                st.write("The model is being initialized, Please wait...")
            else:
                st.write(
                    "Your request was not sent, can you check your internet connection?"
                )
        else:
            st.write("You have to write some text first!!!")


if selected == "News":
    st.title("News Article Summarization")
    st.text("Summarize news article")

    prompt = st.text_input("What would you like to ask?")
    st.write("OR")
    txt_doc = st.file_uploader(
        "Upload your text file here and click on 'Summarise'",
        accept_multiple_files=False,
        type=["txt"],
    )

    if st.button("Summarize"):
        if txt_doc:
            file_content = txt_doc.read().decode("utf-8")
            print(file_content)
            response = query_summary_news(file_content)
            print(response.status_code)
            if response.status_code == 200:
                server_response = response.json()
                print(server_response)
                if server_response:
                    st.write(server_response[0]["summary_text"])
                else:
                    st.write("Sorry our servers are busy")
            elif response.status_code == 503:
                st.write("The model is being initialized, Please wait...")
            else:
                st.write(
                    "Your request was not sent, can you check your internet connection?"
                )

        elif prompt:
            print(prompt)
            response = query_summary_news(prompt)
            print(response.status_code)
            if response.status_code == 200:
                server_response = response.json()
                print(server_response)
                if server_response:
                    st.write(server_response[0]["summary_text"])
                else:
                    st.write("Sorry our servers are busy")
            elif response.status_code == 503:
                st.write("The model is being initialized, Please wait...")
            else:
                st.write(
                    "Your request was not sent, can you check your internet connection?"
                )
        else:
            st.write("You have to write some text first!!!")


if selected == "Scientific Paper summary":
    st.title("Summary Generator")
    st.text("Understand Research Papers with intuitive summary.")

    prompt = st.text_input("What would you like to summarize?")
    st.write("OR")
    txt_doc = st.file_uploader(
        "Upload your text file here and click on 'Summarise'",
        accept_multiple_files=False,
        type=["txt"],
    )

    if st.button("Summarize"):
        if txt_doc:
            file_content = txt_doc.read().decode("utf-8")
            print(file_content)
            response = query_summary_news(file_content)
            print(response.status_code)
            if response.status_code == 200:
                server_response = response.json()
                print(server_response)
                if server_response:
                    st.write(server_response[0]["summary_text"])
                else:
                    st.write("Sorry our servers are busy")
            elif response.status_code == 503:
                st.write("The model is being initialized, Please wait...")
            else:
                st.write(
                    "Your request was not sent, can you check your internet connection?"
                )
        elif prompt:
            print(prompt)
            response = query_summary_scientific(prompt)
            print(response.status_code)
            if response.status_code == 200:
                server_response = response.json()
                print(server_response)
                if server_response:
                    st.write(server_response)
                    # rouge=evaluate.load("rouge")
                    predictions = [server_response[0]["summary_text"]]
                    references = [prompt]
                    # scores = rouge.compute(predictions=predictions, references=references)
                    # print(scores)
                else:
                    st.write("Sorry our servers are busy")
            elif response.status_code == 503:
                st.write("The model is being initialized, Please wait...")
            else:
                st.write(
                    "Your request was not sent,please check your internet connection?"
                )
        else:
            st.write("You have to write some text first!!!")


if selected == "Upload":
    st.title("Visualise your PDFs in the form of a graph database")
    st.text("Talk to your PDFs with the help of LLM Technology")

    pdf_doc = st.file_uploader(
        "Upload your PDFs here and click on 'Process'", accept_multiple_files=False
    )

    if pdf_doc:
        with st.spinner("Creating Graph"):
            if st.button("Create Graph"):
                dir_name = pdf_doc.name.split(".")[0]
                print(f"dir_name= {dir_name}")

                inputdir, outputdir = graph_utils.set_data_dir(dir_name)
                isGraphPresent = graph_utils.make_dir()

                if not isGraphPresent:
                    print("Putting input files in the input directory")
                    my_utils.read_file_and_write_to_txt(
                        pdf_doc.getvalue(), inputdir.joinpath("input_text.txt")
                    )

                else:
                    print("Graph already present")

                # making/loading graph
                df = extract_graph.load_pdf(inputdir)

                nodes, dfg = extract_graph.load_graph(
                    df, outputdir, (not isGraphPresent)
                )
                G = extract_graph.visualize_graph(nodes, dfg)
                visualization_dir = extract_graph.generate_visualization(G)
                print("Visualization Generated")
                print(visualization_dir)
                # webbrowser.open_new_tab(visualization_dir)
                webbrowser.get("safari").open(f'http://127.0.0.1:5500/{visualization_dir[2:]}')
    else:
        st.write("You have to upload a file first!!!")

if selected == "Chat":
    st.title("Chat with your PDFs with the help of LLM Technology")
    pdf_do = st.file_uploader(
        "Upload your PDFs here and click on 'Chat'", accept_multiple_files=False
    )
    if pdf_do and st.button("Chat"):
        if "messages" not in st.session_state:
            st.session_state.messages = [
                {"role": "assistant", "content": "How may I help you?"}
            ]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Function for generating LLM response
        def generate_response(prompt_input, all_text):
            response = generate(prompt_input, all_text)
            return response

        # User-provided prompt
        if prompt := st.chat_input():
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(prompt, read_pdf(pdf_do))
                    st.write(response)
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)
