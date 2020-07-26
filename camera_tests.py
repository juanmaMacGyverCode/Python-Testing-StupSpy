import unittest

from camera import Controller, Sensor, Recorder
from doublex import Spy, Stub, assert_that, called

# Objetivo:
# Software para una camara de vigilancia.
# Partes:
#   Sensor de movimiento.
#       - Algo ha empezado a moverse.   TRUE
#       - Cuando llevamos X segundos en que nada se mueve   FALSE
#   Grabador.
#       - Empezar la grabación.     start_recording
#       - Detener la grabación.     stop_recording
#   Controlador (software)
#       - Nuestro objetivo es programar esta pieza
#

# Mocks - Test Doubles:
#   - Stub: Un código como sustituto de alguna funcionalidad. Simula comportamiento.
#   - Spy: Guarda y recuerda las llamadas. Es como un detective.
#   - Mock
#   - Proxy
#   - Fake
#   - Dummy

class CameraTestsUsingLibrearyDoublex(unittest.TestCase):

    def test_asks_the_recorder_to_stop_recording_when_no_information_received_from_sensor(self):
        sensor = Stub(Sensor)
        recorder = Spy(Recorder)
        controller = Controller(sensor, recorder)

        controller.record_movement()

        assert_that(recorder.stop_recording, called())

    # Si a la camara le ocurre algo incontrolable, quiero que se detenga
    def test_stops_the_recording_if_sensor_raises_an_exception(self):
        with Stub(Sensor) as sensor:
            sensor.is_detecting_movement().raises(ValueError)
        recorder = Spy(Recorder)
        controller = Controller(sensor, recorder)

        controller.record_movement()

        assert_that(recorder.stop_recording, called())

    def test_check_the_sensor_once_per_second(self):
        sensor = Stub(Sensor)
        recorder = Spy(Recorder)
        controller = Controller(sensor, recorder)

        controller.record_movement(3)

        assert_that(recorder.stop_recording, called().times(3))







class CameraTestsUsingMonkeyPatchingForMocks(unittest.TestCase):

    sensor: Sensor
    recorder: Recorder
    controller: Controller

    def setUp(self):
        self.sensor = Sensor()
        self.recorder = Recorder()
        self.controller = Controller(self.sensor, self.recorder)
        self.called = False

    def test_asks_the_recorder_to_stop_recording_when_no_information_received_from_sensor(self):
        ###### SIMULACIÓN monkey patching
        self.sensor.is_detecting_movement = lambda : False
        self.recorder.stop_recording = self.save_call
        ###### FIN SIMULACION

        self.controller.record_movement()  # Usa ya las dependencias simuladas
        self.assertTrue(self.called)

    def test_asks_the_recorder_to_start_recording_when_sensor_detects_movement(self):
        ###### SIMULACIÓN monkey patching
        self.sensor.is_detecting_movement = lambda: True
        self.recorder.start_recording = self.save_call
        ###### FIN SIMULACION

        self.controller.record_movement()  # Usa ya las dependencias simuladas
        self.assertTrue(self.called)

    def save_call(self):
        self.called = True

class StubMovementSensor(Sensor):
    def is_detecting_movement(self)->bool:
        return True

class StubNoMovementSensor(Sensor):
    def is_detecting_movement(self) -> bool:
        return False

class SpyRecorder(Recorder):
    start_called = False
    stop_called = False

    def start_recording(self):
        self.start_called = True
    def stop_recording(self):
        self.stop_called = True

class CameraTestsUsingInheritanceMocks(unittest.TestCase):
    def test_asks_the_recorder_to_stop_recording_when_no_information_received_from_sensor(self):
        sensor = StubNoMovementSensor()
        recorder = SpyRecorder()
        controller = Controller(sensor, recorder)

        controller.record_movement()
        self.assertTrue(recorder.stop_called)

    def test_asks_the_recorder_to_start_recording_when_sensor_detects_movement(self):
        sensor = StubMovementSensor()
        recorder = SpyRecorder()
        controller = Controller(sensor, recorder)

        controller.record_movement()
        self.assertTrue(recorder.start_called)

