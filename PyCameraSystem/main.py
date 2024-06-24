# Press the green button in the gutter to run the script.
from ui import window_controller

if __name__ == '__main__':
    # base_url = "10.0.0.32"
    # remote_ip_addr = "192.168.0.0"
    # device_addr = "01"
    #
    # api = API(base_url, remote_ip_addr, device_addr)
    # print("testing connection")
    # api.test_connection()
    # print("getting protocols")
    # api.get_protocols()
    # # print("Device Name:", api.get_device_name())
    # # print("Device Model:", api.get_device_model())
    # # print("Device Location:", api.get_device_location())
    # print("switching states")
    # switch_states = [True, True, True, True, False, False, False, False]
    # api.switch_dout(api.convert_to_hex_string(switch_states))
    # print("switching single states")
    # api.switch_dout_single(1, True)
    # print("getting io status")
    # switch_states = api.get_io_status()
    # if switch_states:
    #     for state in switch_states:
    #         print(state)

    #
    # ui = CameraUI()
    # ui.start_camera("rtsp://admin:12345@10.0.0.30/Streaming/channels/2/picture")
    window_controller.run_ui()
