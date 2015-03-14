# coding=utf-8
from __future__ import absolute_import


import octoprint.plugin
import octoprint.events
import octoprint.printer
import pigpio
import time
import threading

class IOPlugin(octoprint.plugin.EventHandlerPlugin,
              octoprint.plugin.StartupPlugin,
              octoprint.plugin.ShutdownPlugin,
              octoprint.plugin.SettingsPlugin,
              octoprint.plugin.TemplatePlugin,
              octoprint.plugin.AssetPlugin):
    
    def __init__(self):
        self._lock = threading.Lock()
        self.blink_led1 = False
        self.blink_led2 = False
        self.blink_state = 0
    
    def on_startup(self, host, port):        
        self.pi = pigpio.pi()
        self.blinker = threading.Thread(target=self.blink)
        self.blinker.daemon = True
        self.blinker.start()
        
        
    def on_settings_save(self, data):
        self._logger.info(data)
        
        if (data["button"] != self._button_pin and data["button"] != ""):
            self._button_pin = int(data["button"])
            self.setup_button()
        
        if (data["led1"] != self._led1_pin and data["led1"] != ""):
            self._led1_pin = int(data["led1"])
            self.setup_led1()

        if (data["led2"] != self._led2_pin and data["led2"] != ""):
            self._led2_pin = int(data["led2"])
            self.setup_led2()  
        
        super(IOPlugin, self).on_settings_save(data)
        
    def on_button_press(self, gpio, level, tick):
        
        time.sleep(0.1)
        
        if (level == 0):
            if (self.is_connected() is not False):
                if self._printer.is_printing():
                    self._printer.toggle_pause_print()
                else:
                    if self._printer.is_paused():
                        self._printer.toggle_pause_print()   
                    else:
                        self._printer.start_print()
                
    def setup_button(self):
        self.pi.set_mode(self._button_pin, pigpio.INPUT)
        self.pi.set_pull_up_down(self._button_pin, pigpio.PUD_UP)
        self.b1 = self.pi.callback(self._button_pin, pigpio.EITHER_EDGE, self.on_button_press)
        
    def setup_led1(self):
        self.pi.set_mode(self._led1_pin, pigpio.OUTPUT)
        self.pi.write(self._led1_pin, 0);
    
    def setup_led2(self):
        self.pi.set_mode(self._led2_pin, pigpio.OUTPUT)
        self.pi.write(self._led2_pin, 0);
    
    def on_after_startup(self):
        self._button_pin = int(self._settings.get(["button"]))
        self._led1_pin = int(self._settings.get(["led1"]))
        self._led2_pin= int(self._settings.get(["led2"]))
        
        if (self._button_pin):
            self.setup_button()
        if (self._led1_pin):
            self.setup_led1()
        if (self._led2_pin):
            self.setup_led2()
        
        
    def on_event(self, event, payload):
        with self._lock:
            
            self._logger.info(event)
            
            if event == octoprint.events.Events.PRINT_STARTED or event == octoprint.events.Events.PRINT_RESUMED:
                self.blink_led1 = True
                self.blink_led2 = False
                self.turnOffLed2()
            elif event == octoprint.events.Events.PRINT_DONE or event == octoprint.events.Events.PRINT_FAILED or event == octoprint.events.Events.PRINT_CANCELLED: 
                self.blink_led1 = False
                self.blink_led2 = False
                self.turnOffLed1()
                self.turnOffLed2()
            elif event == octoprint.events.Events.PRINT_PAUSED:
                self.blink_led2 = True
                self.blink_led1 = False
                self.turnOffLed1()
        
            
    def get_settings_defaults(self):
        return dict(button=None,led1=None,led2=None)

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]
    
    def is_connected(self):
        self._logger.info(self._printer.get_current_connection()[0])
        return (self._printer.get_current_connection()[0] != "Closed")
    
    def get_assets(self):
        return dict(
            js=['js/io.js'],
            css=['css/io.css']
        )
    
    def turnOffLed1(self):
        if self._led1_pin is not None:
            self.pi.write(self._led1_pin, 0)    
    
    def turnOffLed2(self):
        if self._led2_pin is not None:
            self.pi.write(self._led2_pin, 0)    
    
    def blink(self):
        
        while True:
            if self.blink_led1 is not False and self._led1_pin is not None:
                self.pi.write(self._led1_pin, self.blink_state)    
            
            if self.blink_led2 is not False and self._led2_pin is not None:
                self.pi.write(self._led2_pin, self.blink_state)    
                
            if self.blink_state == 1:
                self.blink_state = 0
            else:
                self.blink_state = 1
            
            time.sleep(0.5)

__plugin_implementations__ = [IOPlugin()]