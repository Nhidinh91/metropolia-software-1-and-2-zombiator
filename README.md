# Metropolia Software 1 and 2 - Zombiator

This repository contains the source code for a game named Zombiator developed as part of Metropolia Software 1 and 2 courses. The game involves various functionalities such as managing airports, weather conditions, pollution levels, and rewards.

## Installation

Before running the application, make sure to install the required Python libraries using the following commands:

```bash
pip install cachetools
pip install Flask-SQLAlchemy
pip install flask-login
pip install Flask
pip install python-dotenv
```

These libraries are necessary for handling caching, database operations, user authentication, and web development in Flask.
## Setup .env file
```bash
SECRET_KEY=123456
DATABASE_URI=mysql+mysqlconnector://YOUR_DB_USERNAME:YOUR_DB_PASSWORD@localhost/zombiator
GOOGLE_MAPS_API_KEY=YOUR_GOOGLE_API_KEY
OPEN_WEATHER_API_KEY=YOUR_WEATHER_API_KEY
```
To get the YOUR_GOOGLE_API_KEY and YOUR_WEATHER_API_KEY, please follow these materials

**GOOGLE_API_KEY** : https://developers.google.com/maps/get-started

**WEATHER_API_KEY** : https://openweathermap.org/appid

## Run Database script
Run the database script ```create_table_and_data.sql``` in the folder /database_script

## Installation
To run the Zombiator game, execute the main application file. Make sure you have set up the required environment variables, database configurations, and other necessary settings.

```bash
python main_app.py
```

## Demo
https://www.youtube.com/watch?v=dvaXOy4q1Bc&ab_channel=ThaoNhiDinh

## Additional Notes
- This project uses Flask, a web framework for Python, for developing the game application.
- The game involves features related to weather, pollution, rewards, and airport management.
- Ensure that you have a working environment with Python installed before running the application.

Feel free to explore and modify the code for learning purposes or further development.
