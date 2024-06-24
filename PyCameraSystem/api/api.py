import socket


class API:
    def __init__(self, base_url, remote_ip_addr, device_addr):
        self.BASE_URL = base_url
        self.REMOTE_IP_ADDR = remote_ip_addr
        self.DEVICE_ADDR = device_addr
        self.tcp_connection = None

    def connect(self):
        try:
            self.tcp_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_connection.connect((self.BASE_URL, 9500))
            return True
        except Exception as e:
            print(f"Error connecting: {e}")
            return False

    def disconnect(self):
        try:
            if self.tcp_connection:
                self.tcp_connection.close()
        except Exception as e:
            print(f"Error disconnecting: {e}")

    def send_command(self, command):
        try:
            if not self.tcp_connection:
                raise ValueError("Socket not connected")
            self.tcp_connection.sendall(command.encode() + b"\r\n")
            response = self.tcp_connection.recv(1024).strip()
            return response.decode()
        except Exception as e:
            print(f"Error sending/receiving command: {e}")
            return ""
    def test_connection(self):
        if not self.connect():
            return False

        try:
            response = self.send_command("$01M")
            print("Response:", response)
            return True
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            self.disconnect()

    def get_protocols(self):
        if not self.connect():
            return

        try:
            print("Read Device Name:", self.send_command(f"${self.DEVICE_ADDR}M"))
            print("Read Digital I/O Status:", self.send_command(f"@{self.DEVICE_ADDR}"))
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.disconnect()

    def get_device_name(self) -> str:
        if not self.connect():
            return ""

        try:
            response = self.send_command(f"${self.DEVICE_ADDR}M")
            if response.startswith("!"):
                response = response[3:]
            return response
        except Exception as e:
            print(f"Error: {e}")
            return ""
        finally:
            self.disconnect()

    def get_device_model(self) -> str:
        if not self.connect():
            return ""

        try:
            response = self.send_command(f"${self.DEVICE_ADDR}M0")
            if response.startswith("!"):
                response = response[3:]
            return response
        except Exception as e:
            print(f"Error: {e}")
            return ""
        finally:
            self.disconnect()

    def get_device_location(self) -> str:
        if not self.connect():
            return ""

        try:
            response = self.send_command(f"${self.DEVICE_ADDR}M1")
            if response.startswith("!"):
                response = response[1:]
            return response
        except Exception as e:
            print(f"Error: {e}")
            return ""
        finally:
            self.disconnect()

    def switch_dout(self, hex_value) -> bool:
        if not self.connect():
            return False

        try:
            response = self.send_command(f"#{self.DEVICE_ADDR}00{hex_value}")
            print("Switch multiple DOuts:", response)
            return response.startswith(">")
        except Exception as e:
            print(f"Error: {e}")
            return False
        finally:
            self.disconnect()

    def switch_dout_single(self, dout, check):
        if not self.connect():
            return

        try:
            response = self.send_command(f"#{self.DEVICE_ADDR}1{dout}{1 if check else 0}")
            print(f"DOut {dout} Switched response:", response)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            self.disconnect()

    def get_io_status(self):
        if not self.connect():
            return None

        try:
            response = self.send_command(f"@{self.DEVICE_ADDR}")
            print("Read IO Status:", response)
            if response.startswith(">"):
                return self.convert_to_boolean(response[1:])
            else:
                return None
        except Exception as e:
            print(f"Error: {e}")
            return None
        finally:
            self.disconnect()

    @staticmethod
    def convert_to_hex_string(outputs):
        hex_value = sum([(1 << i) for i in range(len(outputs)) if outputs[i]])
        return f"{hex(hex_value)[2:]:0>2}".upper()

    @staticmethod
    def convert_to_boolean(hex_value):
        value = int(hex_value, 16)
        return [value & (1 << i) == 0 for i in range(8)]

