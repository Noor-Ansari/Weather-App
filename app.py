from flask import Flask, render_template, request, redirect, flash
import waitress
import requests 
from datetime import datetime


app = Flask(__name__)
app.config["SECRET_KEY"] = "iohdwiye9823769408cn93hn4890c40398c4"
url = "http://api.openweathermap.org/data/2.5/weather?q={}&appid=2cd00effe34e29a0eb6dc0f15a976857"

@app.route("/")
def home():
    default_city = "Delhi"
    result = requests.get(url.format(default_city)).json()
    default_weather = {
        "city" : result["name"],
        "temp" : round((result["main"]["temp"] - 273.15)),
        "description" : result["weather"][0]["description"],
        "country" : result["sys"]["country"],
        "icon" : result["weather"][0]["icon"],
        "day" : datetime.now().strftime("%A")
    }
    return render_template("index.html", weather = default_weather)

@app.route("/get_weather", methods=["GET","POST"])
def get_weather():
    if request.method=="POST":
        city_name=request.form["search"]
        if city_name != "":
            result = requests.get(url.format(city_name)).json()
            if result["cod"] != "404":
                weather = {
                    "entered_city" : city_name,
                    "city" : result["name"],
                    "temp" : round((result["main"]["temp"] - 273.15)),
                    "description" : result["weather"][0]["description"],
                    "country" : result["sys"]["country"],
                    "icon" : result["weather"][0]["icon"],
                    "day" : datetime.now().strftime("%A")
                }
                return render_template("index.html", weather = weather)
            else:
                flash("Enter valid city")
                return redirect('/')
        else:
            flash("Enter the city ")
            return redirect('/')
    else:
        return redirect("/")

if __name__ == "__main__":
    waitress.serve(app)