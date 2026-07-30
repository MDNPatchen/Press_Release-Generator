import streamlit as st
from google import genai

# 1. Page Title and Instructions
st.title("📰 Press Release to Business Brief")
st.write("Paste a bloated press release below. This tool will strip the marketing fluff and rewrite it into an objective, AP-style brief less than 200 words.")

# 2. Securely load the API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API key configuration error. Please ensure GEMINI_API_KEY is added to your Streamlit Secrets.")
    client = None

# 3. Input text box for the press release
pr_text = st.text_area("Paste Raw Press Release Here:", height=250)

# 4. Generate button logic
if st.button("Generate Brief"):
    if not client:
        st.error("The tool cannot run without a configured API key.")
    elif not pr_text:
        st.warning("Please paste a press release first.")
    else:
        with st.spinner("Editing..."):
            try:
                prompt = f"""
                You are a veteran newspaper copy editor. Take the following press release 
                and rewrite it into a clean, objective business brief for a newspaper.

                Strict Rules:
                1. Keep the total word count strictly less than 200 words.
                2. Focus only on the core news: Who, what, when, where, and why.
                3. Strip out all marketing fluff, corporate jargon, and exaggerated claims.
                4. Write in traditional AP style (third-person, objective tone).
                5. Omit promotional quotes from executives unless they state a crucial material fact.

                Raw Press Release:
                {pr_text}
                """
                
                response = client.models.generate_content(
                    model='gemini-1.5-flash',
                    contents=prompt,
                )
                
                st.success("Brief generated successfully!")
                st.subheader("Your Business Brief:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
