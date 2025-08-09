# Cubit - The Homemade Quantum Coinflip

A homemade quantum probability project using a sensor connected via serial port, with a modern Flask dashboard for real-time monitoring and interaction.

## Features
- **Live Sensor Monitoring**: Real-time display of sensor readings with automatic updates
- **Statistics Display**: Shows high/low reading percentages and counts
- **Quantum Coin Flip**: Interactive coin flip using actual sensor data for randomness
- **Modern UI**: Responsive design with smooth animations and gradient backgrounds
- **WebSocket Support**: Real-time data updates without page refresh

## Quick Start

1. **Make sure your sensor is connected to COM5**

2. **Run the dashboard**:
   - Double-click `start_dashboard.bat` (Windows)
   - Or run manually: `python app.py`

3. **Open your browser and go to**: http://localhost:5000

4. **Click "Start Sensor"** to begin monitoring

## How to Use

### Sensor Monitoring
- Click "Start Sensor" to begin data collection
- The dashboard will show real-time sensor values
- Statistics are calculated and reset every 100 readings
- Click "Stop Sensor" to end monitoring

### Coin Flip Feature
- Click the coin or the "Flip Coin" button
- The system fetches the latest sensor reading
- Values above the calibrated midpoint = Heads
- Values below the calibrated midpoint = Tails
- Watch the animated coin flip!

## Technical Details

- **Backend**: Flask with SocketIO for real-time communication
- **Frontend**: Modern HTML5/CSS3/JavaScript with animations
- **Sensor Communication**: Serial communication via pyserial
- **Auto-calibration**: The system automatically calibrates the sensor midpoint on startup

## Files Structure

```
cubit/
├── app.py                 # Main Flask application
├── start_dashboard.bat    # Windows startup script
├── requirements.txt       # Python dependencies
├── templates/
│   └── dashboard.html     # Dashboard UI
├── src/
│   ├── __init__.py
│   └── cubit.py          # Sensor communication class
└── main.py               # Original command-line script
```

## Dependencies
- Flask 2.3.2
- Flask-SocketIO 5.3.4
- pyserial 3.5
- matplotlib 3.7.1
- colorama 0.4.6
- python-socketio 5.8.0
- eventlet 0.33.3

## API Endpoints

- `GET /` - Dashboard homepage
- `GET /api/sensor-data` - Get current sensor data
- `GET /api/coin-flip` - Perform a coin flip using sensor data
- `GET /api/start` - Start sensor monitoring
- `GET /api/stop` - Stop sensor monitoring

## Troubleshooting

- **Sensor not connecting**: Check that the device is connected to COM5
- **Port access denied**: Make sure no other application is using the serial port
- **Dashboard not loading**: Ensure all dependencies are installed (`pip install -r requirements.txt`)

## Browser Compatibility

Works with all modern browsers:
- Chrome/Chromium
- Firefox
- Safari
- Edge
