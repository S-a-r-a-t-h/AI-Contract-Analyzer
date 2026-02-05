import streamlit as st
import requests

# 🔴 PUT YOUR NEW OPENROUTER KEY HERE (create new one)
API_KEY = "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"

st.title("AI Contract Risk Analyzer")

uploaded_file = st.file_uploader("Upload contract file", type=["txt"])

if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully")

    if st.button("Analyze Contract"):
        with st.spinner("Analyzing..."):

            url = "https://openrouter.ai/api/v1/chat/completions"

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "HTTP-Referer": "http://localhost",
                "X-Title": "AI Contract Analyzer",
                "Content-Type": "application/json"
            }

            data = {
                "model": "mistralai/mistral-7b-instruct",  # ⭐ stable free model
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

            # SAFE OUTPUT
            if "choices" in result:
                output = result["choices"][0]["message"]["content"]
                st.subheader("AI Analysis Result")
                st.write(output)
            else:
                st.error("API limit reached or key invalid")
                st.write(result)

# chat feature
st.subheader("Chat with contract")
user_q = st.text_input("Ask anything about contract")

if user_q:
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "http://localhost",
        "X-Title": "AI Contract Analyzer",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [
            {"role": "user", "content": user_q}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    result = response.json()

    if "choices" in result:
        st.write(result["choices"][0]["message"]["content"])
    else:
        st.error("Try again (free model busy)")

