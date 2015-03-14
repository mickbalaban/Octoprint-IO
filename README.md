This plugin is experimental, it may not work and it may destoy your pi, so be careful!

You will need to install and run pigpiod http://abyz.co.uk/rpi/pigpio/index.html in order to use this module. 

What is this?
============

This simple plugin allows you to connect a button and two LEDs to Raspberry Pi and Octoprint. It lets you start/pause prints using a button connected to Raspberry pi GPIO pins. 

When you first press the button, it will tell octoprint to start printing. In order for this to work, you need to load the file you wish to print using Octoprint web console. If no file is loaded, nothing will happen.

While printer is running, LED1 will flash. If you press the button while printer is printing, it will go into pause state, and LED2 will start flashing (LED1 will turn off). If you press the button again, printer will continue printing, and LED1 will continue flashing...


GPIO
====

You will need to configure 1 pin as input for button and 2 pins as output for LEDs. This can be done using settings panel in Octoprint. Look for a section "io" in navigation menu under plugins. This plugin uses pigpiod library, which uses BCM numbering, so make sure you assign the correct pin!
If you are not sure which pin you connected your button and LEDs, install wiringPi and run:


```
$ gpio readall

 +-----+-----+---------+------+---+-Model B2-+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5V      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |  OUT | 0 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |   IN | 1 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |  OUT | 1 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI |   IN | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO |   IN | 0 | 21 || 22 | 0 | IN   | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK |   IN | 0 | 23 || 24 | 0 | IN   | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 0 | IN   | CE1     | 11  | 7   |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |  28 |  17 | GPIO.17 | ALT2 | 1 | 51 || 52 | 0 | ALT2 | GPIO.18 | 18  | 29  |
 |  30 |  19 | GPIO.19 | ALT2 | 0 | 53 || 54 | 0 | ALT2 | GPIO.20 | 20  | 31  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+-Model B2-+---+------+---------+-----+-----+
 ```
 
 Numbers will be different depending on which version of Pi you are using, so do not use table above as reference!
 
 Installation
 ============
 
run
```
pip install https://github.com/mickbalaban/OctoPrint-IO/archive/master.zip
```
