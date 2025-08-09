from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
import time
import threading
from src.cubit import Qubit
import json
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

cubit = None
is_running = False
current_data = {
    'sensor_value': 0,
    'timestamp': '',
    'high_count': 0,
    'low_count': 0,
    'total_count': 0,
    'high_percentage': 0,
    'low_percentage': 0,
    'hardware_state': '0',
    'midpoint': 512
}

def calibrate_midpoint(cubit_instance, samples=20):
    readings = []
    print("Calibrating midpoint...")
    for _ in range(samples):
        try:
            reading = cubit_instance.read_sensor()
            if reading is not None:
                readings.append(float(reading))
        except (TypeError, ValueError):
            continue
    if not readings:
        return 512
    readings.sort()
    midpoint = (readings[len(readings) // 2] + readings[(len(readings) - 1) // 2]) / 2
    print(f"Calibration complete. Midpoint: {midpoint}")
    return midpoint

def sensor_reader():
    global cubit, is_running, current_data
    
    if cubit is None:
        return
    
    high = 0
    low = 0
    
    midpoint = calibrate_midpoint(cubit)
    current_data['midpoint'] = midpoint
    
    while is_running:
        try:
            cubit.on()
            reading = cubit.read_sensor()
            
            if reading is not None:
                if reading > midpoint:
                    high += 1
                else:
                    low += 1
                
                total = high + low
                high_percentage = (high / total) * 100 if total > 0 else 0
                low_percentage = (low / total) * 100 if total > 0 else 0
                
                current_data.update({
                    'sensor_value': reading,
                    'timestamp': datetime.now().strftime('%H:%M:%S'),
                    'high_count': high,
                    'low_count': low,
                    'total_count': total,
                    'high_percentage': round(high_percentage, 1),
                    'low_percentage': round(low_percentage, 1),
                    'hardware_state': cubit.get_hardware_state() or '0'
                })
                
                socketio.emit('sensor_data', current_data)
                
                if total >= 100:
                    high = 0
                    low = 0
                    
        except (TypeError, UnicodeDecodeError):
            pass
        except Exception as e:
            print(f"Error in sensor reader: {e}")
            
        time.sleep(0.1)

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/api/sensor-data')
def get_sensor_data():
    return jsonify(current_data)

@app.route('/api/coin-flip')
def coin_flip():
    global cubit
    if cubit is None:
        return jsonify({'error': 'Sensor not connected'}), 500
    
    try:
        cubit.on()
        reading = cubit.read_sensor()
        if reading is not None:
            result = 'heads' if reading > current_data['midpoint'] else 'tails'
            return jsonify({
                'result': result,
                'sensor_value': reading,
                'midpoint': current_data['midpoint'],
                'timestamp': datetime.now().strftime('%H:%M:%S')
            })
        else:
            return jsonify({'error': 'No sensor reading available'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/start')
def start_sensor():
    global cubit, is_running
    try:
        if cubit is None:
            cubit = Qubit(port='COM5')
            for _ in range(5):
                cubit.on()
            time.sleep(2)
        
        if not is_running:
            is_running = True
            thread = threading.Thread(target=sensor_reader)
            thread.daemon = True
            thread.start()
        
        return jsonify({'status': 'started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stop')
def stop_sensor():
    global cubit, is_running
    is_running = False
    if cubit:
        cubit.close()
        cubit = None
    return jsonify({'status': 'stopped'})

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('sensor_data', current_data)

@socketio.on('disconnect')
def on_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
    socketio.run(app, debug=True, host='127.0.0.1', port=5000)
