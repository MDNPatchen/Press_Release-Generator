import streamlit as st
from google import genai

# 1. Set up the web page title and description
st.title("📰 Press Release to Business Brief")
st.write("Paste a bloated press release below. This tool will strip the marketing fluff and rewrite it into an objective, AP-style brief under 200 words.")

# 2. Ask the user for their API key (or you can securely hardcode yours later)
api_key = st.text_input("Enter Gemini API Key (get one at aistudio.google.com):", type="password")

# 3. Create a large text box for the press release
pr_text = st.text_area("Paste Raw Press Release Here:", height=250)

# 4. Create a "Generate" button
if st.button("Generate Brief"):
    if not api_key:
        st.error("Please enter an API key.")
    elif not pr_text:
        st.warning("Please paste a press release first.")
    else:
        # Show a loading spinner while the AI works
        with st.spinner("Editing..."):
            try:
                # Initialize client with the provided key
                client = genai.Client(api_key=api_key)
                
                # The prompt from your original script
                prompt = f"""
                You are a veteran newspaper copy editor. Take the following press release 
                and rewrite it into a clean, objective business brief for a newspaper.

                Strict Rules:
                1. Keep the total word count strictly under 200 words.
                2. Focus only on the core news: Who, what, when, where, and why.
                3. Strip out all marketing fluff, corporate jargon, and exaggerated claims.
                4. Write in traditional AP style (third-person, objective tone).
                5. Omit promotional quotes from executives unless they state a crucial material fact.

                Raw Press Release:
                {pr_text}
                """
                
                # Call the model
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=prompt,
                )
                
                # 5. Display the final result
                st.success("Brief generated successfully!")
                st.subheader("Your Business Brief:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
