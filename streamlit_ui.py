from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import datetime
import streamlit as st
import os
import praw
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Streamlit UI
st.title("Reddit Persona Generator")

# Input fields
SUBREDDIT_NAME = st.text_input("Subreddit Name", placeholder="Put subreddit you like to analyse")
CLIENT_ID = st.text_input("Client ID", placeholder="Your Reddit Client ID", type="password")
CLIENT_SECRET = st.text_input("Client Secret", placeholder="Your Reddit Client Secret", type="password")
USER_AGENT = st.text_input("User Agent", placeholder="Your Reddit User Agent")
GOOGLE_API_KEY = st.text_input("Google Gemini API Key", placeholder="Your Google Gemini API Key", type="password")

# Model selection
model_options = ["gemini-2.5-pro-experimental", "gemini-2.0-flash", "gemini-2.0-flash-lite", "gemini-1.5-pro", "gemini-1.5-flash", "gemini-1.0-nano"]
selected_model = st.selectbox("Select Gemini Model", model_options)

# Initialize session state
if 'persona_generated' not in st.session_state:
    st.session_state.persona_generated = False
    st.session_state.subreddit_sentiment = ""
    st.session_state.persona_map = ""
    st.session_state.word_data = None
    st.session_state.pdf_data = None
    st.session_state.output_filename = ""

# Function to fetch subreddit comments
def get_subreddit_comments(reddit, subreddit_name, limit=100):
    try:
        subreddit = reddit.subreddit(subreddit_name)
        comments = subreddit.comments(limit=limit)
        comment_list = [{"id": c.id, "body": c.body, "author": c.author.name if c.author else None, 
                         "score": c.score, "created_utc": c.created_utc} for c in comments]
        return comment_list
    except Exception as e:
        st.error(f"Error getting comments from {subreddit_name}: {e}")
        return None

# Function to analyze sentiment
def analyze_subreddit_sentiment(comments):
    comments_text = "\\n".join([comment["body"] for comment in comments])
    model = ChatGoogleGenerativeAI(model=selected_model, google_api_key=GOOGLE_API_KEY)
    prompt = f"""You are an expert in sentiment analysis. Analyze the following comments and determine the overall sentiment of the subreddit.
    Comments:
    {{comments_text}}
    Overall Sentiment:"""
    prompt_template = ChatPromptTemplate.from_template(prompt)
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({"comments_text": comments_text})

# Function to create persona map
def create_persona_map(comments):
    comments_text = "\\n".join([comment["body"] for comment in comments])
    model = ChatGoogleGenerativeAI(model=selected_model, google_api_key=GOOGLE_API_KEY)
    prompt = f"""You are an expert in creating persona maps. Analyze the following comments and create a persona map that can be created from that subreddit.
    Comments:
    {{comments_text}}
    Persona Map:"""
    prompt_template = ChatPromptTemplate.from_template(prompt)
    chain = prompt_template | model | StrOutputParser()
    return chain.invoke({"comments_text": comments_text})

# Generate persona button
if st.button("Generate Persona"):
    if not all([SUBREDDIT_NAME, CLIENT_ID, CLIENT_SECRET, USER_AGENT, GOOGLE_API_KEY]):
        st.warning("Please fill in all the input fields.")
    else:
        try:
            os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
            reddit = praw.Reddit(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, user_agent=USER_AGENT)
            comments = get_subreddit_comments(reddit, SUBREDDIT_NAME)
            if comments:
                # Generate sentiment and persona map
                st.session_state.subreddit_sentiment = analyze_subreddit_sentiment(comments)
                st.session_state.persona_map = create_persona_map(comments)
                st.session_state.output_text = f"Subreddit Sentiment: {st.session_state.subreddit_sentiment}\nPersona Map: {st.session_state.persona_map}"

                # Generate Word file
                doc = Document()
                doc.add_paragraph(st.session_state.output_text)
                bio_word = BytesIO()
                doc.save(bio_word)
                bio_word.seek(0)
                st.session_state.word_data = bio_word.getvalue()

                # Generate PDF file
                bio_pdf = BytesIO()
                c = canvas.Canvas(bio_pdf, pagesize=letter)
                textobject = c.beginText()
                textobject.setTextOrigin(10, 730)
                textobject.textLines(st.session_state.output_text)
                c.drawText(textobject)
                c.save()
                bio_pdf.seek(0)
                st.session_state.pdf_data = bio_pdf.getvalue()

                st.session_state.persona_generated = True
            else:
                st.error(f"Could not retrieve comments from {SUBREDDIT_NAME}")
        except Exception as e:
            st.error(f"Error: {e}")

# Display output and download options if persona is generated
if st.session_state.persona_generated:
    output_filename = f"Persona_generate_{SUBREDDIT_NAME}_{USER_AGENT}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Collapsible output window
    with st.expander("View Output", expanded=True):
        st.subheader("Subreddit Sentiment:")
        st.write(st.session_state.subreddit_sentiment)
        st.subheader("Persona Map:")
        st.write(st.session_state.persona_map)

    st.subheader("Download Options")
    st.download_button(
        label="Download as Word",
        data=st.session_state.word_data,
        file_name=f"{output_filename}.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
    st.download_button(
        label="Download as PDF",
        data=st.session_state.pdf_data,
        file_name=f"{output_filename}.pdf",
        mime="application/pdf"
    )
else:
    st.info("Please click 'Generate Persona' to create the persona map.")

st.markdown("---")
st.markdown("Made with Love by Arpan Guria")
st.markdown("[Connect with me on LinkedIn](https://www.linkedin.com/in/arpan-guria/)")
st.markdown("[FAQ](https://drive.google.com/drive/folders/1Gtp5Gu1qIXJym6Xb8JbhHUD_R1yPlosU?usp=sharing)")
st.markdown("[Setup Guide](https://drive.google.com/drive/folders/1Gtp5Gu1qIXJym6Xb8JbhHUD_R1yPlosU?usp=sharing)")
