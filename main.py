import instaloader
import streamlit as st
import os
import shutil
import tempfile

# Set the main styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f0f0;
        font-family: 'Arial', sans-serif;
    }

    .container {
        max-width: 600px;
        margin: auto;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #fff;
    }

    h1 {
        color: #333;
        text-align: center;
        margin-bottom: 20px;
    }

    .button {
        background-color: #4CAF50;
        color: white;
        padding: 10px 20px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        border-radius: 5px;
        cursor: pointer;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to download Instagram post
def download_post(url, output_folder):
    L = instaloader.Instaloader()
    post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])

    # Create a temporary directory for downloading
    temp_dir = tempfile.mkdtemp()

    try:
        # Download the post to the temporary directory
        L.download_post(post, target=temp_dir)

        # Move the relevant file to the desired output folder
        if post.is_video:
            video_filename = f"{post.date_utc}_UTC.mp4"
            print(f"Moving video file: {video_filename}")
            shutil.move(os.path.join(temp_dir, video_filename), os.path.join(output_folder, video_filename))
        else:
            image_filename = f"{post.date_utc}_UTC.jpg"
            print(f"Moving image file: {image_filename}")
            shutil.move(os.path.join(temp_dir, image_filename), os.path.join(output_folder, image_filename))
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Cleanup: Remove the temporary directory
        print(f"Removing temporary directory: {temp_dir}")
        shutil.rmtree(temp_dir)

# Main content
st.title("Instagram Downloader")
st.markdown("Download photos, videos, or stories in the highest quality.")

# Input field for Instagram post URL
post_url = st.text_input("Enter Instagram Post URL:")

# Download button with improved styling
if st.button("Download", key="download_button"):
    if post_url:
        output_folder = "."  # Use "." for the current working directory
        print(f"Downloading post from URL: {post_url}")
        download_post(post_url, output_folder)
        st.success(f"Download complete! Check your output folder: {output_folder}")
    else:
        st.warning("Please enter a valid Instagram post URL.")
''