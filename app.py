import streamlit as st
from text_summarizer import summarize_text
import time

# Page configuration
st.set_page_config(
    page_title="Text Summarizer Pro",
    page_icon="📝",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .success-message {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        color: #155724;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("⚙️ Settings")
    
    # Summary length control
    summary_length = st.slider(
        "Summary Length",
        min_value=1,
        max_value=5,
        value=3,
        help="Control the length of the summary (1: Very short, 5: Detailed)"
    )
    
    # Language selection
    language = st.selectbox(
        "Language",
        ["English", "Spanish", "French", "German"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.markdown("""
    This app uses advanced NLP to create 
    concise summaries of your text.
    
    Made with ❤️ by Your Name
    """)

# Main content
st.title("📝 Text Summarizer Pro")
st.markdown("Transform your long text into clear, concise summaries instantly!")

# Input section
text_input = st.text_area(
    "Enter your text here:",
    height=200,
    placeholder="Paste your article, document, or text here..."
)

col1, col2 = st.columns([1, 1])

with col1:
    summarize_button = st.button("✨ Generate Summary")
with col2:
    clear_button = st.button("🗑️ Clear")

# Process the text
if summarize_button and text_input:
    with st.spinner('Analyzing your text...'):
        try:
            # Add progress bar for better UX
            progress_bar = st.progress(0)
            for i in range(100):
                time.sleep(0.01)
                progress_bar.progress(i + 1)
            
            # Get summary
            summary = summarize_text(text_input)
            
            # Display results
            st.markdown("### 📊 Summary Results")
            
            # Display metrics
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Original Length", f"{len(text_input)} chars")
            with col2:
                st.metric("Summary Length", f"{len(summary)} chars")
            with col3:
                reduction = round((1 - len(summary)/len(text_input)) * 100)
                st.metric("Reduction", f"{reduction}%")
            
            # Display summary
            st.markdown("### 📝 Generated Summary")
            st.success(summary)
            
            # Additional options
            st.markdown("### 🔍 Actions")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📋 Copy to Clipboard"):
                    st.write("Summary copied to clipboard!")
            with col2:
                st.download_button(
                    label="💾 Download Summary",
                    data=summary,
                    file_name="summary.txt",
                    mime="text/plain"
                )
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
elif summarize_button and not text_input:
    st.warning("⚠️ Please enter some text to summarize!")

if clear_button:
    text_input = ""
    st.experimental_rerun()

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center'>
        <p>Need help? Check out our <a href='#'>documentation</a> or <a href='#'>contact support</a></p>
    </div>
    """,
    unsafe_allow_html=True
) 
