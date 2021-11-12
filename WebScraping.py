from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from flask import Flask, render_template, request
from flask_mail import Mail, Message

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'bobbot0008@gmail.com'
app.config['MAIL_PASSWORD'] = 'FehAQBhijQRz#cDuid^$RJYaFq$siW8'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


@app.route('/')
def home():
    url = request.args.get("URL_site", "")
    email = request.args.get("email", "")
    price_wanted = request.args.get("number", "")
    price(url, email, price_wanted)
    return render_template("index.html")


def price(url, email, price_wanted):

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        web = urlopen(req).read()
        page_soup = BeautifulSoup(web, "html.parser")

        title = page_soup.find("h1")
        title2 = ""
        for title1 in title:
            print(title1)
            title2 += title1

        containers = page_soup.find("span", "price_num")
        for container in containers:
            print(container)

        converted_price = float(container[0:5])

        if converted_price <= float(price_wanted):
            send_mail(email, url, title2)
        print(converted_price)

    except ValueError:
        return "invalid input"


@app.route('/')
def send_mail(email, url, title):
    msg = Message('Price fell down', sender='bobbot0008@gmail.com', recipients=[email])
    msg.body = 'You can verify the product, ' + title + ', at: ' + url
    mail.send(msg)


if __name__=="__main__":
    app.run(debug=True)
