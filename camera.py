import time

class Sensor:
    # Simulado
    def is_detecting_movement(self) -> bool:
        """ Mucho código """
        pass


class Recorder:
    # Simulado
    def start_recording(self):
        """ Mucho código """
        pass

    # Simulado
    def stop_recording(self):
        """ Mucho código """
        pass

############################################

class Controller:

    def __init__(self, sensor: Sensor, recorder: Recorder):
        self.__sensor = sensor
        self.__recorder = recorder

    # Dos tests
    def record_movement(self, number_of_seconds=1):
        for i in range(number_of_seconds):
            try:
                if self.__sensor.is_detecting_movement():
                    self.__recorder.start_recording()
                else:
                    self.__recorder.stop_recording()
            except ValueError as e:
                self.__recorder.stop_recording()
            time.sleep(1)

