import RPi.GPIO as GPIO

class Encoder:
    def __init__(self, ena_pin, enb_pin):
        self.ena_pin = ena_pin
        self.enb_pin = enb_pin
        self.count = 0
        self.state = '00'
        self.direction = None


        GPIO.setup(self.ena_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(self.enb_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.add_event_detect(self.ena_pin, GPIO.BOTH, callback=self.transitionOccurred)  
        GPIO.add_event_detect(self.enb_pin, GPIO.BOTH, callback=self.transitionOccurred)  


    def transitionOccurred(self, channel):
        p1 = GPIO.input(self.leftPin)
        p2 = GPIO.input(self.rightPin)
        newState = "{}{}".format(p1, p2)

        if self.state != newState:
            self.count += 1
            self.state = newState

    def getCount(self):
        return self.count


