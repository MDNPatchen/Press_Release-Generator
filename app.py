import streamlit as st
from google import genai

# 1. Page Title and Instructions
st.title("📰 Press Release to Business Brief")
st.write("Paste a bloated press release below. This tool will strip the marketing fluff and rewrite it into an objective, AP-style brief.")

# 2. Securely load the API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("API key configuration error. Please ensure GEMINI_API_KEY is added to your Streamlit Secrets.")
    client = None

# 3. UI Controls
# Added: Dropdown menu for editors to select the maximum word count
word_count = st.selectbox(
    "Select maximum word count:",
    [100, 200, 300, 400, 500],
    index=1 # Defaults to 200 words
)

# Input text box for the press release
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
                # UPDATED PROMPT: Dynamic word count, strict AP style, and paragraph form only
                prompt = f"""
                You are a veteran newspaper copy editor. Take the following press release 
                and rewrite it into a clean, objective business brief for a newspaper.

                Strict Rules:
                1. Keep the total word count strictly under {word_count} words.
                2. Write ONLY in standard paragraph form. Do not use bullet points, numbered lists, or special formatting.
                3. Write in strict AP (Associated Press) style (third-person, objective tone, correct dateline formatting, proper title capitalization, etc.).
                4. Focus only on the core news: Who, what, when, where, and why.
                5. Strip out all marketing fluff, corporate jargon, and exaggerated claims.
                6. Omit promotional quotes from executives unless they state a crucial material fact.

                Raw Press Release:
                {pr_text}
                """
                
                # Using the latest supported model
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                )
                
                st.success("Brief generated successfully!")
                st.subheader("Your Business Brief:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
