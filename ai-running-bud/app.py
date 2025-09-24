from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

WEATHER_API_KEY = "7dd26626d28e8f5a08b800cc9c488f45"

# Motivational messages
good_messages = [
   "Time to hit the streets! 🏃‍♀️💨",
    "Your sneakers are calling! 👟",
    "A perfect day for a run! 🌞",
    "Run like the wind! 🌬️💪",
    "The pavement is begging for your footsteps! 🛣️✨",
    "Your future self will thank you for this run! 🙏💫",
    "Channel your inner cheetah! 🐆⚡",
    "The only bad run is the one you didn't take! 😉🌟",
    "Make the squirrels jealous of your pace! 🐿️💨",
    "Running: because adulting is hard and this is cheaper than therapy! 🏃‍♀️💸",
    "Go burn some calories so you can eat more pizza later! 🍕🔥",
    "Your couch will still be there when you get back! 🛋️⏳",
    "Run now, brag later! 💪😎",
    "The weather gods are smiling upon your running plans! ☀️🙌",
    "Outrun your responsibilities! 🏃‍♀️📊",
    "Your dog would be proud! 🐶❤️",
    "Think of the amazing shower you'll have after this! 🚿✨",
    "Running: the only time it's acceptable to chase nothing! 🎯😂",
    "Go be the main character in your running movie! 🎬🌟",
    "Your fitness tracker is getting lonely! ⌚💔"
]

bad_messages = [
    "Try yoga or indoor exercises today! 🧘‍♀️",
    "No worries, your workout can wait indoors! 🏋️‍♀️",
    "Stay active inside with a fun routine! 🏠💪",
    "Keep moving, even if it's inside! 🌟",
    "Mother Nature says: 'Netflix and treadmill?' 📺🏃‍♀️",
    "Perfect weather for becoming an indoor ninja! 🥷✨",
    "Your running shoes need a spa day too! 👟💆‍♀️",
    "The universe wants you to discover the joy of dancing in your living room! 💃🎶",
    "Bad weather = perfect excuse to try that weird workout video! 📹🤪",
    "Indoor workouts: because puddles are not foot baths! 💦🙅‍♀️",
    "Channel your inner hamster on the wheel! 🐹🏃‍♀️",
    "The couch is judging you less today! 🛋️😌",
    "Perfect day to practice your 'running in place' technique! 🏃‍♀️📍",
    "Your future dry self will thank you! 🌧️🙏",
    "Indoor cardio: where the only thing wet is your forehead! 💦😅",
    "Time to become one with your yoga mat! 🧘‍♀️📜",
    "The weather says 'rest day' but your muscles say 'creative workout!' 💡💪",
    "Perfect conditions for becoming a living room athlete! 🏠🥇",
    "Your umbrella is on strike - respect its boundaries! ☔✊",
    "Indoor workout: because wind-blown hair only looks good in movies! 💨🎬"
]

def get_motivational_message(temp, description):
    if temp is not None and description is not None:
        if 10 <= temp <= 30 and "rain" not in description and "snow" not in description:
            return random.choice(good_messages)
        else:
            return random.choice(bad_messages)
    return "Stay motivated! 💪"

@app.route("/", methods=["GET", "POST"])
def home():
    city = None
    temp = None
    description = None
    message = None
    icon = None
    weather_class = ""

    if request.method == "POST":
        city = request.form["city"]
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={WEATHER_API_KEY}"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_data.get("cod") == 200:
            temp = weather_data['main']['temp']
            description = weather_data['weather'][0]['description']
            icon_code = weather_data['weather'][0]['icon']
            icon = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            message = get_motivational_message(temp, description)

            # Determine color for styling if its good weather or bad weather
            if 10 <= temp <= 30 and 'rain' not in description and 'snow' not in description:
                weather_class = "good"
            else:
                weather_class = "bad"
        else:
            message = "City not found. Please try again."
            weather_class = "bad"

    return render_template(
        "index.html",
        city=city,
        temp=temp,
        description=description,
        message=message,
        icon=icon,
        weather_class=weather_class
    )

if __name__ == "__main__":
    app.run(debug=True)