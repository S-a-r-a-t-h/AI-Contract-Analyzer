import streamlit as st
import requests

# 🔴 PASTE YOUR OPENROUTER KEY HERE
API_KEY = "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"

st.set_page_config(page_title="AI Contract Risk Analyzer", layout="wide")
st.title("AI Contract Risk Analyzer for SMEs")

st.write("Upload a contract file and get AI risk analysis instantly.")

uploaded_file = st.file_uploader("Upload contract file", type=["txt"])

if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully")

    # 🔍 ANALYZE BUTTON
    if st.button("Analyze Contract"):
        with st.spinner("Analyzing contract..."):

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
You are a legal AI assistant.

Analyze this contract and provide:
1. Summary
2. Risk level (Low/Medium/High)
3. Risky clauses
4. Suggestions

Contract:
{contract_text[:3000]}
"""
                    }
                ]
            }

            try:
                response = requests.post(url, headers=headers, json=data)
                result = response.json()

                if "choices" in result:
                    output = result["choices"][0]["message"]["content"]
                    st.subheader("AI Analysis Result")
                    st.write(output)
                else:
                    st.error("API busy or invalid key. Try again.")
                    st.write(result)

            except Exception as e:
                st.error("Error occurred")
                st.write(e)

    # 💬 CHAT WITH CONTRACT (winning feature)
    st.subheader("Chat with Contract")
    user_q = st.text_input("Ask any question about contract")

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

Answer this question:
{user_q}
"""
                }
            ]
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            result = response.json()

            if "choices" in result:
                st.write(result["choices"][0]["message"]["content"])
            else:
                st.error("API busy. Try again.")

        except Exception as e:
            st.error("Error occurred")
            st.write(e)
