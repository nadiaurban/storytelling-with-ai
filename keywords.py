import openai
import streamlit as st

# Function to extract difficult words and translate them into Chinese
def extract_keywords(story, client):
    prompt = (
        f"Find the most difficult words in this story that middle school students might not understand, "
        f"and translate them into Chinese:\n\n"
        f"### Story:\n{story}\n\n"
        "Provide only the keywords one keyword per line:\n\n"
        "**Word (English) | Translation (Chinese)**\n"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a language assistant specializing in vocabulary learning."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200,
            temperature=0.5,
        )

        keywords = response.choices[0].message.content.strip()
        return keywords

    except Exception as e:
        st.error(f"❌ Error extracting keywords: {e}")
        return None
