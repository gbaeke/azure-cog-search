
import requests
import streamlit as st
from config import *
import json

# Azure OpenAI REST endpoint
endpoint = f"https://{AZURE_OPENAI_RESOURCE}.openai.azure.com/openai/deployments/{AZURE_OPENAI_MODEL}/extensions/chat/completions?api-version={AZURE_OPENAI_PREVIEW_API_VERSION}"
    

# endpoint headers with Azure OpenAI key
headers = {
    'Content-Type': 'application/json',
    'api-key': AZURE_OPENAI_KEY
}

# Streamlit app title
st.title("🤖 Azure Add Your Data Bot")

# Keep messages array in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous chat messages from history on app rerun
# Add your data messages include tool responses and assistant responses
# Exclude the tool responses from the chat display
for message in st.session_state.messages:
    if message["role"] != "tool":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# if user provides chat input, get and display response
# add user question and response to previous chat messages
if user_prompt := st.chat_input():
    st.chat_message("user").write(user_prompt)
    with st.chat_message("assistant"):
        with st.spinner("🧠 thinking..."):
            # add the user query to the messages array
            st.session_state.messages.append({"role": "user", "content": user_prompt})
            body = {
                "messages": st.session_state.messages,
                "temperature": float(AZURE_OPENAI_TEMPERATURE),
                "max_tokens": int(AZURE_OPENAI_MAX_TOKENS),
                "top_p": float(AZURE_OPENAI_TOP_P),
                "stop": AZURE_OPENAI_STOP_SEQUENCE.split("|") if AZURE_OPENAI_STOP_SEQUENCE else None,
                "stream": False,
                "dataSources": [
                    {
                        "type": "AzureCognitiveSearch",
                        "parameters": {
                            "endpoint": f"https://{AZURE_SEARCH_SERVICE}.search.windows.net",
                            "key": AZURE_SEARCH_KEY,
                            "indexName": AZURE_SEARCH_INDEX,
                            "fieldsMapping": {
                                "contentField": AZURE_SEARCH_CONTENT_COLUMNS.split("|") if AZURE_SEARCH_CONTENT_COLUMNS else [],
                                "titleField": AZURE_SEARCH_TITLE_COLUMN if AZURE_SEARCH_TITLE_COLUMN else None,
                                "urlField": AZURE_SEARCH_URL_COLUMN if AZURE_SEARCH_URL_COLUMN else None,
                                "filepathField": AZURE_SEARCH_FILENAME_COLUMN if AZURE_SEARCH_FILENAME_COLUMN else None,
                                "vectorFields": AZURE_SEARCH_VECTOR_COLUMNS.split("|") if AZURE_SEARCH_VECTOR_COLUMNS else []
                            },
                            "inScope": True if AZURE_SEARCH_ENABLE_IN_DOMAIN.lower() == "true" else False,
                            "topNDocuments": AZURE_SEARCH_TOP_K,
                            "queryType":  AZURE_SEARCH_QUERY_TYPE,
                            "roleInformation": AZURE_OPENAI_SYSTEM_MESSAGE,
                            "embeddingEndpoint": AZURE_OPENAI_EMBEDDING_ENDPOINT,
                            "embeddingKey": AZURE_OPENAI_EMBEDDING_KEY
                        }
                    }   
                ]
            }  

            # send request to chat completion endpoint
            try:
                response = requests.post(endpoint, headers=headers, json=body)

                # there will be a tool response and assistant response
                tool_response = response.json()["choices"][0]["messages"][0]["content"]
                tool_response_json = json.loads(tool_response)
                assistant_response = response.json()["choices"][0]["messages"][1]["content"]

                # get urls
                urls = [citation["url"] for citation in tool_response_json["citations"]]


            except Exception as e:
                st.error(e)
                st.stop()
            
           
            # replace [docN] with urls and use 0-based indexing
            for i, url in enumerate(urls):
                assistant_response = assistant_response.replace(f"[doc{i+1}]", f"[[{i}]({url})]")
            

            # write the response to the chat
            st.write(assistant_response)

            # write the urls to the chat; gpt response might not refer to all
            st.write(urls)

            # add both responses to the messages array
            st.session_state.messages.append({"role": "tool", "content": tool_response})
            st.session_state.messages.append({"role": "assistant", "content": assistant_response})
            

            