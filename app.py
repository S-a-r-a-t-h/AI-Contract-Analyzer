
import streamlit as st
import requests

API_KEY = "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"

st.set_page_config(page_title="AI Contract Risk Analyzer", layout="wide")
st.title("AI Contract Risk Analyzer for SMEs")

uploaded_file = st.file_uploader("Upload Contract", type=["txt"])

if uploaded_file:
    contract_text = uploaded_file.read().decode("utf-8")
    st.success("Contract uploaded!")

    if st.button("Analyze Contract"):
        with st.spinner("Analyzing..."):

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/mixtral-8x7b-instruct",
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
Analyze this contract and give:
1. Summary
2. Risk level
3. Risky clauses
4. Suggestions

Contract:
{contract_text[:3000]}
"""
                    }
                ]
            }

            response = requests.post(url, headers=headers, json=data)
            result = response.json()
            output = result['choices'][0]['message']['content']

            st.subheader("AI Result")
            st.write(output)

    st.subheader("Chat with contract")
    user_q = st.text_input("Ask anything")

    if user_q:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mixtral-8x7b-instruct",
            "messages": [
                {
                    "role": "user",
                    "content": f"""
Contract:
{contract_text[:3000]}

Answer:
{user_q}
"""
                }
            ]
        }

        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        st.write(result['choices'][0]['message']['content'])
