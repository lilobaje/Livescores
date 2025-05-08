# LiveScore Flask Application

A simple Flask-based live score application that provides real-time sports scores and updates.

## Features

- Real-time sports scores updates
- Responsive design for all devices
- Clean, intuitive user interface
- Automatic updates without page refresh
- Grouped matches by leagues and countries

## Prerequisites

- Python 3.7+
- Flask
- API key from a sports data provider (e.g., API-Football)

## Installation

1. Clone this repository or download the code
2. Create a virtual environment:
   ```
   python -m venv venv
   ```
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - MacOS/Linux: `source venv/bin/activate`
4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```
5. Create a `.env` file in the root directory and add your API key:
   ```
   API_KEY=your_api_key_here
   ```

## Usage

### Running the Application

1. With your virtual environment activated, run:
   ```
   python app.py
   ```
   or
   ```
   python improved_app.py  # For the version with mock data
   ```

2. Open your browser and navigate to `http://127.0.0.1:5000`

### Testing Without an API Key

If you don't have an API key yet, you can test the application using mock data:

1. Run the improved version: `python improved_app.py`
2. Navigate to `http://127.0.0.1:5000`
3. The application will automatically use mock data if no API key is provided

## Getting an API Key

To get real live score data, you'll need an API key from a sports data provider. Some options include:

1. [API-Football](https://www.api-football.com/) - Used in this example
2. [SportRadar](https://sportradar.com/)
3. [The Sports DB](https://www.thesportsdb.com/api.php) (Free tier available)

Register on their website and follow their instructions to get an API key.

## Project Structure

```
livescore-app/
├── app.py                 # Main Flask application
├── improved_app.py        # Enhanced version with mock data
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (API keys)
├── templates/
│   └── index.html         # Main template file
└── README.md              # This file
```

## Customization

### Changing Sports

To change the sport being tracked, modify the `SPORT` variable in `app.py` or `improved_app.py`:

```python
SPORT = "basketball"  # Options depend on your API provider
```

### Styling

The application uses Bootstrap for styling. You can customize the look and feel by modifying the CSS in `templates/index.html`.

## Deployment

To deploy this application to a production server:

1. Set up a proper web server (e.g., Nginx, Apache)
2. Use Gunicorn as the WSGI server:
   ```
   gunicorn -w 4 app:app
   ```
3. Set up proper environment variables on your server
4. Consider using a service like Heroku, Render, or DigitalOcean App Platform for simple deployment

## Contributing

Feel free to fork this project and make your own modifications. Pull requests are welcome!

## License

This project is open source and available under the MIT License.