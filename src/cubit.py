import serial
import time
from colorama import Fore, Style, init


init(autoreset=True)

class Qubit:
    def __init__(self, port: str = 'COM5'):
        self.state = '0'
        self.port = port
        print(f"{Fore.YELLOW}[{self.port}]{Fore.RESET} Initializing Qubit on port {port} at {time.strftime('%H:%M:%S')}{Style.RESET_ALL}")
        while True:
            try:
                self.serial = serial.Serial(port, 9600, timeout=1)
                if self.serial.is_open:
                    print(f"{Fore.YELLOW}[{self.port}]{Fore.RESET} Waiting for serial data...{Style.RESET_ALL}")
                    while True:
                        if self.serial.in_waiting > 0:
                            break
                        time.sleep(0.1)
                    break
            except serial.SerialException:
                print(f"{Fore.RED}[{self.port}]{Fore.RESET} SerialException: {Style.RESET_ALL}")
                continue
            print(f"{Fore.RED}[{self.port}]{Fore.RESET} Waiting for connection...{Style.RESET_ALL}")
            time.sleep(1)
        print(f"{Fore.GREEN}[{self.port}]{Fore.RESET} Qubit initialized at {time.strftime('%H:%M:%S')}{Style.RESET_ALL}")

    def send_command(self, state: str):
        self.serial.write(state.encode())
    
    def get_state(self):
        return self.state
    
    def get_hardware_state(self):
        try:
            sensor_value, state = self._read_sensor_and_state()
            return state
        except (ValueError, TypeError):
            return None
    
    def on(self):
        self.state = '1'
        self.send_command(self.state)
        print(f"{Fore.GREEN}[{self.port}]{Fore.RESET} Lazer ON at {time.strftime('%H:%M:%S')}{Style.RESET_ALL}")
        return self.state
    
    def off(self):
        self.state = '0'
        self.send_command(self.state)
        print(f"{Fore.RED}[{self.port}]{Fore.RESET} Lazer OFF at {time.strftime('%H:%M:%S')}{Style.RESET_ALL}")
        return self.state

    def _read_sensor_and_state(self):
        line = self.serial.readline().decode().strip()
        if ',' in line:
            parts = line.split(',')
            if len(parts) == 2:
                sensor_value = int(parts[0]) if parts[0].isdigit() else None
                state = int(parts[1]) if parts[1].isdigit() else None
                return sensor_value, state
        raise ValueError("Invalid data format")

    def read_sensor(self):
        try:
            sensor_value, state = self._read_sensor_and_state()
            print(f"{Fore.CYAN}[{self.port}]{Fore.RESET} SENSOR READ at {time.strftime('%H:%M:%S')}: {sensor_value} (State: {state}){Style.RESET_ALL}")
            return sensor_value
        except (ValueError, TypeError):
            print(f"{Fore.CYAN}[{self.port}]{Fore.RESET} SENSOR READ at {time.strftime('%H:%M:%S')}: Invalid data{Style.RESET_ALL}")
            return None
    
    def close(self):
        if self.serial.is_open:
            self.serial.close()
            print(f"{Fore.YELLOW}[{self.port}]{Fore.RESET} Serial connection closed at {time.strftime('%H:%M:%S')}{Style.RESET_ALL}")

if __name__ == "__main__":
    cubit = Qubit(port='COM5')
    while True:
        cubit.on()
        time.sleep(0.1)
        cubit.off()
        time.sleep(0.1)
        