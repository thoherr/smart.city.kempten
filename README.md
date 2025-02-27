# smart.city.kempten

This repository contains the source code for a couple of microcontrollers,
sensors and other ICs implementing a digital twin of the [Smart City Kempten (Allgäu)](https://smartes.kempten.de/)
as a LEGO model.

The model was built by Marius Herrmann (https://steponabrick.com,
info@steponabrick.com), the electronics and software was implemented by me
(Thomas Herrmann, mail@thoherr.de).

The software is written in MicroPython (https://micropython.org), running on Raspberry Pico (2) W.

Currently the functionality is splitted to two Pico W (Inner City 1 and 2) and one Pico 2 W (Illerufer), in order to
distribute the functionality to more devices.

The entry point of the application is [main.py](main.py).

The file [setup_values.py](setup_values.py) specifies which of the three controller code bases
should run on the current device by setting a `controller_number`.
Furthermore it specifies the values of some timing variables and verbosity flags.

Network settings, especially for the MQTT server, are configured in [setup_mqtt_config.py](setup_mqtt_config.py).
See corresponding template files.

The coding of the three controllers is located in the directory [smart_city](smart_city).

For documentation of the electronics of the model, including the hardware used, wiring diagrams and layouts
see the document [CONTROLLERS](docs/CONTROLLERS.md), located in the [docs](docs) directory.
