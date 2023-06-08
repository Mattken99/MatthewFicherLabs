import time
from Model import *
from Button import *
from CompositeLights import *
from Displays import *
from Buzzer import *
from myclasses import *

class TrafficLightController:
    def __init__(self):
        # Instantiate the main and aux traffic lights
        self._main_light = TrafficLight(GreenLight(16), YellowLight(18), RedLight(19))
        self._aux_light = TrafficLight(GreenLight(11), YellowLight(12), RedLight(13))
        
        # Instantiate the pedestrian button and set the handler to self
        self._button = Button(4, "PedestrianButton", buttonhandler=self)
        
        # Instantiate the LCD display
        self._display = LCDDisplay(sda=0, scl=1, i2cid=0)
        
        # Instantiate the model with 5 states and set self as the handler
        self._model = Model(5, self, debug=True)

        self._buzzer = ActiveBuzzer(15)

        self._pir = MotionSensor(28)
        
        # Add the button to the model
        self._model.addButton(self._button)
        
        # Define the transitions between states

        self._model.addTransition(0, TIMEOUT, 1)
        self._model.addTransition(1, TIMEOUT, 2)
        self._model.addTransition(2, TIMEOUT, 3)
        self._model.addTransition(3, TIMEOUT, 0)
        self._model.addTransition(4, TIMEOUT, 0)

        self._model.addTransition(0, BTN1_PRESS, 4)
        self._model.addTransition(1, BTN1_PRESS, 4)
        self._model.addTransition(2, BTN1_PRESS, 4)
        self._model.addTransition(3, BTN1_PRESS, 4)


    
    def run(self):
        # Run the model
        self._model.run()
    
    def stateDo(self, state):

        if state == 0:
            # State 0 do/actions
            if self._pir.motionDetected():
                self._model.gotoState(4)
        elif state == 1:
            # State 1 do/actions
            if self._pir.motionDetected():
                self._model.gotoState(4)
        elif state == 2:
            # State 1 do/actions
            if self._pir.motionDetected():
                self._model.gotoState(4)        
        elif state == 3:
            # State 1 do/actions
            if self._pir.motionDetected():
                self._model.gotoState(4)
            pass

    def stateEntered(self, state):
        # Perform actions when entering a state
        if state == 0:
            # Start the main light on green
            self._display.reset()
            self._main_light.go()
            self._aux_light.stop()
            self._display.showText("Do Not Walk")
            time.sleep(5)
            self.timeout()  # Call the timeout method after 5 seconds
        elif state == 1:
            # Start the main light on yellow
            self._main_light.caution()
            self._aux_light.stop()
            self._display.showText("Do Not Walk")
            time.sleep(2)
            self.timeout()  # Call the timeout method after 2 seconds
        elif state == 2:
            # Start the main light on red and the aux light on green
            self._display.reset()
            self._main_light.stop()
            self._aux_light.go()
            self._display.showText("Do Not Walk")
            time.sleep(5)
            self.timeout()  # Call the timeout method after 5 seconds
        elif state == 3:
            # Start the aux light on yellow
            self._display.reset()
            self._main_light.stop()
            self._aux_light.caution()
            self._display.showText("Do Not Walk")
            time.sleep(2)
            self.timeout()  # Call the timeout method after 2 seconds
        elif state == 4:
            # Stop both lights and display "Walk" with countdown
            self._buzzer.play()
            self._buzzer.stop()
            self._display.reset()
            self._main_light.stop()
            self._aux_light.stop()
            
            countdown = 10  # Countdown from 10 seconds
            while countdown >= 0:
                self._display.showText("Walk: {:02d}".format(countdown))
                time.sleep(1)
                countdown -= 1

            self.timeout()  # Call the timeout method to transition to the next state
    
    
    def stateLeft(self, state):
        # Perform actions when leaving a state
        pass
    
    def buttonPressed(self, name):
        # Handle the button press event
        if self._model.getState() != 4:
            # Transition to state 4 on button press
            self._model.gotoState(4)
    
    def buttonReleased(self, name):
        # Handle the button release event
        pass
    
    def timeout(self):
        self._model.processEvent(TIMEOUT)

if __name__ == '__main__':
    # Create an instance of the TrafficLightController and run it
    TrafficLightController().run()
