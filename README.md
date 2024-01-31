# Image Search Application

This is a Streamlit-based image search application that allows users to search for images based on a text query using Sentence Transformers and cosine similarity. Users can provide images by uploading a zip file, specifying a directory path, or uploading individual images.

## Features

- Upload a zip file containing images for searching.
- Specify a directory path where images are stored.
- Upload individual images for searching (default option).
- Enter a text query to find relevant images.
- Display the most relevant image and the top 10 relevant images based on cosine similarity.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your-username/image-search-app.git
   cd image-search-app
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   streamlit run app.py
   ```

## Usage

1. Choose one of the options to provide images: upload a zip file, specify a directory path, or upload individual images.
2. Enter a text query in the input field.
3. Click the "Search" button.
4. The most relevant image and the top relevant images will be displayed based on the text query.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Make sure to replace "your-username" with your actual GitHub username in the repository URL. This `readme.md` provides instructions on how to install and use your image search application, along with information about licensing.
