import streamlit as st
from sentence_transformers import SentenceTransformer, util
from PIL import Image
import torch
import os
import glob
import shutil
import tempfile

# Function to load and encode images
def load_and_encode_images(img_paths):
    images = [Image.open(img) for img in img_paths]
    img_embeddings = img_model.encode(images)
    return img_embeddings

# Initialize models outside of the function to avoid reloading them on each run
img_model = SentenceTransformer('clip-ViT-B-32')
text_model = SentenceTransformer('sentence-transformers/clip-ViT-B-32-multilingual-v1')

# Streamlit UI
st.title("Image Search")

# User input for search query
search_query = st.text_input("Enter your search query:")

# Dropdown for selecting the input method
input_method = st.selectbox("Select an option to provide images:", ["Upload individual images (default)","Upload a zip file", "Specify a directory path"])

# Temporary directory to extract uploaded images
temp_dir = tempfile.mkdtemp()

if input_method == "Upload a zip file":
    # Option to upload a zip file containing images
    image_zip = st.file_uploader("Upload a zip file containing images:", type=["zip"])
    
    if image_zip:
        with open(os.path.join(temp_dir, 'images.zip'), 'wb') as f:
            f.write(image_zip.read())
        shutil.unpack_archive(os.path.join(temp_dir, 'images.zip'), temp_dir)
        img_paths = glob.glob(os.path.join(temp_dir, '*.jpg'))
        img_embeddings = load_and_encode_images(img_paths)

elif input_method == "Specify a directory path":
    # Option to specify a directory path
    image_directory = st.text_input("Enter the path to the folder containing images:")
    
    if image_directory:
        img_paths = glob.glob(os.path.join(image_directory, '*.jpg'))
        img_embeddings = load_and_encode_images(img_paths)

else:
    # Option to upload individual images (default)
    individual_images = st.file_uploader("Upload individual images:", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if individual_images:
        img_paths = [os.path.join(temp_dir, f.name) for f in individual_images]
        for img_file, img_path in zip(individual_images, img_paths):
            with open(img_path, 'wb') as f:
                f.write(img_file.read())
        img_embeddings = load_and_encode_images(img_paths)

# Determine the value of k based on the number of available images
k = min(len(img_paths), 11) if 'img_paths' in locals() else 1

# Search and Display Results
if st.button("Search") and search_query and k > 0:
    text_embeddings = text_model.encode([search_query])
    cos_sim = util.cos_sim(text_embeddings, img_embeddings)[0]

    # Get indices of the images with highest similarity scores
    top_indices = torch.topk(cos_sim, k=k).indices

    st.write("Most Relevant Image:")
    st.image(img_paths[top_indices[0]], caption="Top 1")

    st.write(f"Top {k-1} Relevant Images:")
    for idx in top_indices[1:]:
        st.image(img_paths[idx], caption=f"Score: {cos_sim[idx].item()}")

# Clean up temporary directory
shutil.rmtree(temp_dir)
