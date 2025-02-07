# from flask import Flask, render_template, request, jsonify
# import PIL.Image
# import io

# # Initialize Flask app
# app = Flask(__name__)

# # Configure the AI model
# api_key = "AIzaSyBxg2Vzurrs7giquvhPlghaxZO0ya2MdK8"  # Replace with your actual key
# genai.configure(api_key=api_key)
# model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# # Load sample images
# sample_file_2 = PIL.Image.open('circuit.png')
# sample_file_3 = PIL.Image.open('firefighter.jpg')

# # Convert image to bytes
# def encode_image(image_obj):
#     img_byte_array = io.BytesIO()
#     image_obj.save(img_byte_array, format='PNG')  # Convert to PNG format
#     return img_byte_array.getvalue()  # Return binary data

# @app.route("/")
# def home():
#     return render_template("index.html")  # Serve a simple HTML form

# @app.route("/ask", methods=["POST"])
# def ask_image():
#     image_choice = request.form.get("image_choice")
#     query = request.form.get("query")

#     # Select the correct image based on user choice
#     if image_choice == "circuit":
#         selected_image = sample_file_2
#     elif image_choice == "firefighter":
#         selected_image = sample_file_3
#     else:
#         return jsonify({"error": "Invalid image choice! Please choose 'circuit' or 'firefighter'."})

#     # Convert the image to binary format
#     selected_image_binary = encode_image(selected_image)

#     # Generate the AI response
#     response = model.generate_content([
#         {"mime_type": "image/png", "data": selected_image_binary},
#         query
#     ])

#     # Return the AI response as JSON
#     return jsonify({"ai_response": response.text})

# if __name__ == "__main__":
#     app.run(debug=True)





############################################################################################################

from dotenv import load_dotenv
import google.generativeai as genai
import json
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
def encode_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")  # Convert to Base64 string


@app.route("/")
def home():
    return render_template("index.html")  # Serve an HTML form

@app.route("/ask", methods=["POST"])
def ask_image():
    image_choice = request.form.get("image_choice")
    query = request.form.get("query")

    # Select image based on user choice
    if image_choice == "circuit":
        image_path = "circuit.png"
    elif image_choice == "firefighter":
        image_path = "firefighter.jpg"
    else:
        return jsonify({"error": "Invalid image choice! Choose 'circuit' or 'firefighter'."})

    # Encode image as Base64
    image_base64 = encode_image(image_path)

    # Generate AI response
    response = model.generate_content([
        {"mime_type": "image/png", "data": image_base64},
        query
    ])

    # Return the AI response as JSON
    return jsonify({"ai_response": response.text})

if __name__ == "__main__":
    app.run(debug=True)

