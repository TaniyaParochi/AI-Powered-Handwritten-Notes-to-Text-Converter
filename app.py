from flask import Flask, render_template
import google.generativeai as genai
import httpx
import base64

app = Flask(__name__)

# Configure API key for Google Generative AI
genai.configure(api_key="AIzaSyBxg2Vzurrs7giquvhPlghaxZO0ya2MdK8")

@app.route("/")
def home():
    # Retrieve an image from a URL
    image_path = "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg/2560px-Palace_of_Westminster_from_the_dome_on_Methodist_Central_Hall.jpg"
    image = httpx.get(image_path)

    # Choose the Gemini model
    model = genai.GenerativeModel(model_name="gemini-2.0-flash")

    # Create a prompt
    prompt = "Caption this image."
    
    # Generate the content (caption for the image)
    response = model.generate_content(
        [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(image.content).decode("utf-8"),
            },
            prompt,
        ]
    )

    # Get the caption text from the response
    caption = response.text

    # Return the caption on the webpage
    return render_template("index.html", caption=caption)

if __name__ == "__main__":
    app.run(debug=True)
