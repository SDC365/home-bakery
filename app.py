from flask import Flask, render_template, request, redirect
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/menu')
def menu():
    if os.path.exists('cakes.csv'):
        cakes = pd.read_csv('cakes.csv').to_dict(orient='records')
    else:
        cakes = []
    return render_template("menu.html", cakes=cakes)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        name = request.form['name']
        weight = request.form['weight']
        price = request.form['price']
        image = request.files['image']

        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            data = {'name': name, 'weight': weight, 'price': price, 'image': image.filename}
            df = pd.DataFrame([data])

            if os.path.exists('cakes.csv'):
                df.to_csv('cakes.csv', mode='a', header=False, index=False)
            else:
                df.to_csv('cakes.csv', index=False)

            return redirect('/menu')

    return render_template("upload.html")

@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        dob = request.form['dob']

        message = f"Hello, I'm {name} ({dob}) - my number is {mobile}. I'd like to inquire about your cakes."
        whatsapp_url = f"https://wa.me/91{mobile}?text={message.replace(' ', '%20')}"

        data = {'name': name, 'mobile': mobile, 'dob': dob, 'datetime': datetime.now()}
        df = pd.DataFrame([data])

        if os.path.exists('inquiries.csv'):
            df.to_csv('inquiries.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('inquiries.csv', index=False)

        return redirect(whatsapp_url)

    return render_template("inquiry.html")

if __name__ == '__main__':
    app.run(debug=True)
