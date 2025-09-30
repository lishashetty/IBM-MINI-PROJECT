from flask import Flask, render_template, request
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Load trained model
model = joblib.load("model.pkl")

# Load dataset for reference/fallback
dataset_path = "dataset.csv"
if os.path.exists(dataset_path):
    df_dataset = pd.read_csv(dataset_path)
else:
    df_dataset = pd.DataFrame()  # empty if file not found

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# About page
@app.route("/about")
def about():
    return render_template("about.html")

# Gallery page
@app.route("/gallery")
def gallery():
    images_folder = os.path.join(app.static_folder, "images")
    image_files = [f for f in os.listdir(images_folder)
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
    return render_template("gallery.html", images=image_files)

@app.route("/contact", methods=["GET", "POST"])
def contact():
    message_sent = False  # flag to indicate form submission

    if request.method == "POST":
        # You can process the form data here if needed
        name = request.form.get("name")
        email = request.form.get("email")
        subject = request.form.get("subject")
        message = request.form.get("message")

        # For now, we just show a thank-you message
        message_sent = True

    return render_template("contact.html", message_sent=message_sent)

# Predict route
@app.route("/predict", methods=["GET","POST"])
def predict():
    predicted_price = None
    selected_image = None
    dataset = None

    if request.method == "POST":
        try:
            # Get form inputs
            type_ = request.form['type']
            brand = request.form['brand']
            material = request.form['material']
            size = request.form['size']
            season = request.form['season']

            # Prepare input for model
            input_df = pd.DataFrame([[type_, brand, material, size, season]],
                                    columns=['type','brand','material','size','season'])
            
            # Predict price
            predicted_price = round(model.predict(input_df)[0], 2)

            # Select corresponding image
            images = {
                'T-Shirt': 'tshirt.jpeg',
                'Jeans': 'jeans.jpeg',
                'Dress': 'dress.jpg',
                'Jacket': 'jacket.jpeg',
                'Shirt': 'shirt.jpg',
                'Skirt': 'skirt.jpeg',
                'Saree':'saree.jpg',
                'Wedding-Lehenga':'Lehenga.jpg',
                'Sharara':'sharara.jpg',
                'Formal-Wear':'Formal-Wear.jpeg'
            }
            selected_image = images.get(type_, 'default.jpeg')

        except Exception as e:
            print("Error:", e)
            # Instead of error, show dataset
            predicted_price = None
            selected_image = None
            dataset = df_dataset.to_html(classes='dataset-table', index=False)

    return render_template("predict.html",
                           predicted_price=predicted_price,
                           selected_image=selected_image,
                           dataset=dataset)
@app.route("/shops")
def shops():
    return render_template("shops.html")



if __name__ == "__main__":
    app.run(debug=True)
