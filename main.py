from src import *
import time

LOW = 175
HIGH = 1023

def calibrate_midpoint(cubit, samples=20):
    readings = []
    print("Calibrating midpoint... Please keep the sensor in a neutral position.")
    for _ in range(samples):
        try:
            reading = cubit.read_sensor()
            if reading is not None:
                readings.append(float(reading))
        except (TypeError, ValueError):
            continue
    if not readings:
        raise ValueError("No valid readings collected for calibration.")
    readings.sort()
    midpoint = (readings[len(readings) // 2] + readings[(len(readings) - 1) // 2]) / 2
    print(f"Calibration complete. Midpoint: {midpoint}")
    return midpoint

def main():
    low = 0
    high = 0

    cubit = Qubit(port='COM5')
    cubit.on()
    cubit.on()
    cubit.on()
    cubit.on()
    cubit.on()

    time.sleep(5)

    MIDPOINT = calibrate_midpoint(cubit)

    try:
        while True:
            cubit.on()
            try:
                reading = cubit.read_sensor()
                if reading is not None:
                    if reading > MIDPOINT:
                        high += 1
                    else:
                        low += 1
                    
                    total = high + low
                    if total > 0:
                        high_percentage = (high / total) * 100
                        low_percentage = (low / total) * 100
                        print(f"High: {high_percentage:.1f}% ({high}) | Low: {low_percentage:.1f}% ({low}) | Total: {total}")
                        print(f"State: {cubit.get_hardware_state()}")
                        if total >= 100:
                            high = 0
                            low = 0
                    else:
                        print("Collecting data...")
            except (TypeError, UnicodeDecodeError):
                pass

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nInterrupted by user. Closing serial connection...")
        cubit.close()

if __name__ == "__main__":
    main()
