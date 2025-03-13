import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI
from keywords import extract_keywords


# Load the .env file to access the OpenAI API key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    st.error("⚠️ API Key not found. Check your .env file.")
else:
    client = OpenAI(api_key=OPENAI_API_KEY)  # Create OpenAI client instance

# Set up Streamlit page
st.set_page_config(
    page_title="Storytelling with AI",  # Browser tab title
    page_icon="📖",  # Adds an icon (emoji or image path)
    layout="wide",  # Expands content for better UX
    initial_sidebar_state="expanded"  # Sidebar starts open
)


#st.title("📖 Storytelling with AI")
st.markdown(
    """
    <h1 style='text-align: center; 
               background-color: #0A2F6B; 
               color: #FFFFFF; 
               padding: 15px; 
               border-radius: 10px; 
               font-size: 36px; 
               font-family: "Arial", sans-serif;'>
        📖 Storytelling with AI
    </h1>
    <hr style='width: 50%; border: 3px solid #A02040; margin: auto;'>
    """,
    unsafe_allow_html=True
)

# Improved Subtitle with Styling
st.markdown(
    """
    <div style='text-align: center; 
                font-size: 20px; 
                font-weight: bold; 
                color: #0A2F6B; 
                margin-top: 15px;'>
        🖊️ Create a unique story using AI! <br> 
        Enter the story details and let the AI craft a creative story!
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("<hr style='border: 1px solid #A02040;'>", unsafe_allow_html=True)

# Sidebar Header
st.sidebar.header("📌 Story Setup")

# **Text Inputs with Unique Keys**
setting = st.sidebar.text_input("🌍 Setting", 
                                placeholder="e.g., Shanghai Thomas School, a bilingual school.", 
                                key="input_setting")

style = st.sidebar.text_input("🎭 Style", 
                              placeholder="e.g., Fantasy, like Harry Potter", 
                              key="input_style")

characters = st.sidebar.text_area("👥 Characters", 
                                  placeholder="e.g., Ellen, a new student in the school.", 
                                  key="input_characters")

main_event = st.sidebar.text_area("📌 Main Event", 
                                  placeholder="e.g., Middle school students discover a secret room by accident!", 
                                  key="input_main_event")

# **Set Story Details Button (Unique Key)**
if "story_details_saved" not in st.session_state:
    st.session_state["story_details_saved"] = False  # Track button press

if st.sidebar.button("✅ Set Story Details", key="btn_set_story"):
    if not (setting and style and characters and main_event):
        st.sidebar.warning("⚠️ Please fill in all fields before saving.")
    else:
        st.session_state["story_details"] = (
            f"**Setting:** {setting}\n"
            f"**Style:** {style}\n"
            f"**Characters:** {characters}\n"
            f"**Main Event:** {main_event}"
        )
        st.session_state["story_details_saved"] = True
        st.rerun()  # ✅ Forces a rerun to prevent duplicate button display

# **Show success message only after saving**
if st.session_state["story_details_saved"]:
    st.sidebar.success("✅ Story details saved! Now generate your story.")

# **Collapsible Help Section**
with st.sidebar.expander("💡 How to Fill These In"):
    st.write("""
    - **Setting:** Where does the story happen? (e.g., A futuristic city)
    - **Style:** What genre? (e.g., Adventure, Sci-Fi, Mystery)
    - **Characters:** Who is in the story? (e.g., Caroline, a young scientist)
    - **Main Event:** What is the central event? (e.g., They scientists discover an alien baby!)
    """)

# **Custom Sidebar Styling (Fixed Colors for Background, Text, and Buttons)**
st.markdown(
    """
    <style>
    /* Sidebar Background */
    [data-testid="stSidebar"] {
        background-color: #0A2F6B !important; /* Custom Dark Blue */
    }

    /* Sidebar Text Color */
    [data-testid="stSidebar"] * {
        color: #ffffff !important; /* White Text */
    }

    /* Fix Text Visibility in Input Fields */
    [data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
        color: #D3D3D3 !important; /* Light Grey Text */
        background-color: #0F3D75 !important; /* Slightly Lighter Blue Background */
        border-radius: 5px;
        padding: 8px;
        border: 1px solid #A0A0A0 !important; /* Subtle Border */
    }

    /* Make Placeholder Text More Visible */
    ::placeholder {
        color: #BBBBBB !important; /* Light Grey Placeholder */
    }

    /* Streamlit Buttons - Fix White Text on White Background */
    [data-testid="stSidebar"] button {
        background-color: #A02040 !important; /* Maroon Background */
        color: #FFFFFF !important; /* White Text */
        font-weight: bold;
        border-radius: 8px;
        padding: 10px;
        width: 100%;
        border: none;
    }

    /* Button Hover Effect */
    [data-testid="stSidebar"] button:hover {
        background-color: #d6284d !important; /* Lighter Red on Hover */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# Function to generate a story using OpenAI API
def generate_story():
    if not st.session_state["story_details"]:
        st.warning("⚠️ Please set the story details first.")
        return None

    prompt = (
    "You are a creative story-writing assistant for middle school students. "
    "Your task is to generate a short, engaging, and respectful story in simple English."
    "based on the following details provided by the student:\n\n"
    f"{st.session_state['story_details']}\n\n"
    "INSTRUCTIONS:\n"
    "- MOST IMPORTANT! Use simple and clear English (easy for non-native speakers).\n"
    "- Ensure the story is age-appropriate for middle school students.\n"
    "- Make the story exciting, engaging, and imaginative.\n"
    "- Structure the story with a clear beginning, middle, and end.\n"
    "- Use vivid but simple descriptions to bring the story to life.\n"
    "- DO NOT exceed 20 sentences.\n\n"
    "Write the story in a fun and easy-to-understand way. Keep sentences natural and engaging.\n\n"
    "STORY:\n"
)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a skilled and respectful short story writer for students. "
                                              "Write in simple  English and make the story easy to follow."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=750,  # Increased to allow for 20-25 sentences
            temperature=0.7,  # Slightly reduced to maintain coherence
            frequency_penalty=0.5,  # Reduces repetitive phrases
            presence_penalty=0.3  # Encourages diverse vocabulary
        )

        story = response.choices[0].message.content.strip()
        return story

    except Exception as e:
        st.error(f"❌ Error generating story: {e}")
        return None



# Generate Story Button
if st.button("📝 Write Your Story"):
    with st.spinner("Creating your story... ✨"):
        story = generate_story()
        if story:
            st.session_state["generated_story"] = story  # ✅ Store the story
            
# Always Display the Story if It Exists
if "generated_story" in st.session_state and st.session_state["generated_story"]:
    st.subheader("📖 Your AI-Generated Story:")
    st.markdown(
        f"""
        <div style='
            background-color: #f9f9f9; 
            border-radius: 10px; 
            padding: 15px; 
            box-shadow: 2px 2px 10px rgba(0,0,0,0.1); 
            border-left: 5px solid #1E3A8A;
            padding: 20px;
            margin-top: 10px;
        '>
            <p style='color: #333; font-size: 16px; line-height: 1.6;'>{st.session_state["generated_story"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # "Download Story" Button
    st.download_button(
        label="📥 Download the Story",
        data=st.session_state["generated_story"],
        file_name="AI_Generated_Story.txt",
        mime="text/plain"
    )

    # "Show Keywords" Button
    if st.button("🔍 Show Keywords & Translations"):
        with st.spinner("Extracting keywords..."):
            keywords = extract_keywords(st.session_state["generated_story"], client)
            if keywords:
                st.subheader("📖 Key Vocabulary & Translations:")
                st.markdown(
                    f"""
                    <div style='
                        background-color: #f0f0f0; 
                        border-radius: 10px; 
                        padding: 15px; 
                        box-shadow: 2px 2px 10px rgba(0,0,0,0.1); 
                        border-left: 5px solid #A02040;
                    '>
                        <pre style='color: #333; font-size: 16px; line-height: 1.6;'>{keywords}</pre>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

# Add empty space before footer
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)
st.markdown("<div style='height: 50px;'></div>", unsafe_allow_html=True)


# Separator Line
st.markdown("<hr style='border: 1px solid #A02040;'>", unsafe_allow_html=True)

# Footer Text
st.markdown(
    """
    <div style='text-align: left;'>
        <p>©Created by Nadia Urban for Shanghai Thomas School.<br>Powered by GPT-4o for creative storytelling.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# School Logo
st.image("school_logo.png", width=150)
