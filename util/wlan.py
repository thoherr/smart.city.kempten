from utime import sleep
from ntptime import settime

import network


def initialize_wlan(ssid, password, verbose=False):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    wlan.connect(ssid, password)

    connection_timeout = 10
    while connection_timeout > 0:
        if wlan.status() >= 3:
            break
        connection_timeout -= 1
        if verbose:
            print('Waiting for Wi-Fi connection...')
        sleep(1)

    if wlan.status() != 3:
        return False
    else:
        if verbose:
            print('Connection successful!')
            network_info = wlan.ifconfig()
            print('IP address:', network_info[0])
        settime()
        return True
