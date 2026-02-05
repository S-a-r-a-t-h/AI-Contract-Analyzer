import streamlit as st
import requests

API_KEY = "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"

st.title("AI Contract Risk Analyzer for SMEs")

uploaded_file = st.file_uploader("Upload contract", type=["txt"])

if uploaded_file is not None:
    contract_text = uploaded_file.read().decode("utf-8")
    st.success("File uploaded successfully")

    if st.button("Analyze Contract"):

        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "HTTP-Referer": "https://localhost",
            "X-Title": "AI Contract Analyzer",
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

        # SAFE CHECK
        if "choices" in result:
            output = result["choices"][0]["message"]["content"]
            st.subheader("AI Analysis Result")
            st.write(output)
        else:
            st.error("API error or free model limit reached")
            st.write(result)
