from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify
import PIL.Image
import io
import base64
import os

# Initialize Flask app
app = Flask(__name__)

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Configure Gemini AI
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-2.0-flash")


# Function to encode image as Base64
def encode_image_from_bytes(image_bytes):
    """Encode image bytes as Base64 string."""
    return base64.b64encode(image_bytes).decode("utf-8")  # Convert to Base64 string


@app.route("/")
def home():
    """Serve the HTML form."""
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask_image():
    """Handle the image upload and query."""
    uploaded_file = request.files.get("image")  # Uploaded image file
    query = request.form.get("query")  # Get query text from the user

    if not uploaded_file or not query:
        return jsonify({"error": "Both an image and a query are required!"})

    try:
        # Read the image file as bytes and encode as Base64
        image_bytes = uploaded_file.read()
        image_base64 = encode_image_from_bytes(image_bytes)

        # Generate AI response
        response = model.generate_content([
            {"mime_type": uploaded_file.mimetype, "data": image_base64},
            query
        ])

        # Return the AI response as JSON
        return jsonify({"ai_response": response.text})
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"})


if __name__ == "__main__":
    app.run(debug=True)
