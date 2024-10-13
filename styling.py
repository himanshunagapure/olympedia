import streamlit as st

def load_css(file_name: str):
    """
    Loads a CSS file and injects it into the Streamlit app.

    Parameters:
    - file_name (str): Path to the CSS file.
    """
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning(f"CSS file `{file_name}` not found. Proceeding without custom styles.")

def set_title(title: str, color: str = "#457B9D"):
    """
    Sets a styled title using Markdown.

    Parameters:
    - title (str): The title text.
    - color (str): The color of the title text.
    """
    st.markdown(f"<h1 style='text-align: center; color: {color};'>{title}</h1>", unsafe_allow_html=True)

def set_subtitle(subtitle: str, color: str = "#457B9D"):
    """
    Sets a styled subtitle using Markdown.

    Parameters:
    - subtitle (str): The subtitle text.
    - color (str): The color of the subtitle text.
    """
    st.markdown(f"<h2 style='text-align: center; color: {color};'>{subtitle}</h2>", unsafe_allow_html=True)
