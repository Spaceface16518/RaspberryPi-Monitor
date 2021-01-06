import psutil
from flask import Flask, render_template,make_response

app = Flask(__name__)


def temperature(reading):
    return {name: [{'label': entry.label, 'current': entry.current, 'high': entry.high, 'critical': entry.critical} for
                   entry in entries] for name, entries in reading.items()}


@app.route('/')
def current_temperature():
    reading = psutil.sensors_temperatures()
    temps = temperature(reading)
    return render_template('dashboard.html', temps=temps)


@app.route('/health')
def health():
    response = make_response("Healthy", 200)
    response.mimetype = "text/plain"
    return response

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
