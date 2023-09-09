import socket
import network
import machine
from secrets import secrets
from machine import Pin,PWM,UART,WDT
import time 

ssid = secrets['ssid']
password = secrets['pw']

led = machine.Pin("LED",Pin.OUT)

ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)
#wdt = WDT(timeout=8000)

while ap.active() == False:
  pass

print('Connection successful')
print(ap.ifconfig()) 

def generateHTML():
    html = """<!DOCTYPE html>
    <html>
        <head> 
            <title>Hackspace Bot</title> 
            <style>
            button {
                width:175px;
                height:100px;
                background-color:#0000ff;
                color:#ffffff;
                font-size:25pt
            }
            </style>
        </head>
        <body>
            <div>
                <form action="" method="post">
                <table class="controller">
                <tr>
                    <td></td>
                    <td>
                        <button type="submit" formaction="forwards">&#8593</button>
                    </td>
                    <td></td>
                </tr>
                <tr>
                    <td><button type="submit" formaction="left">&#8592</button></td>
                    <td>
                        <button type="submit" formaction="stop">Stop</button>
                    </td>
                    <td>
                        <button type="submit" formaction="right">&#8594</button>
                    </td>
                </tr>
                <tr>
                    <td></td>
                    <td>
                        <button type="submit" formaction="backwards" >&#8595</button>
                    </td>
                    <td></td>
                </tr>
                </table>
            </div>
            """
    html = html + f"""
            <div>
            <table>
                <tr>
                    <td>SSID</td>
                    <td>PASSWORD</td>
                    <td>IP</td>
                </tr>
                <tr>
                    <td>{ssid}</td>
                    <td>{password}</td>
                    <td>{ap.ifconfig()}</td>
                </tr>
            </table>
            </div>
            </form>
    </body>
        </html>
    """
    return html

addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

In1=Pin(6,Pin.OUT)  #IN1
In2=Pin(7,Pin.OUT)  #IN2


#OUT3  and OUT4
In3=Pin(4,Pin.OUT)  #IN3
In4=Pin(3,Pin.OUT)  #IN4

EN_A=PWM(Pin(8))
EN_B=PWM(Pin(2))
# Defining frequency for enable pins
EN_A.freq(1500)
EN_B.freq(1500)

# Setting maximum duty cycle for maximum speed (0 to 65025)
EN_A.duty_u16(65025)
EN_B.duty_u16(65025)

def restart():
    stop()

    
# Left
def turn_left():
    print("Left I go")
    
    In1.high()
    In2.low()
    In3.low()
    In4.high()
    
def turn_right():
    print("Right I go")
    
    In1.low()
    In2.high()
    In3.high()
    In4.low()
    
# Backward
def move_backward():
    print("Back up Back up")
    
    In1.low()
    In2.high()
    In3.low()
    In4.high()
    
# Forward
def move_forward():
    print("Onwards!")
    
    In1.high()
    In2.low()
    In3.high()
    In4.low()
        
# Stop
def stop():
    print("All Stop")
    
    In1.low()
    In2.low()
    In3.low()
    In4.low()

print('listening on', addr)

# Listen for connections
while True:
    try:
        led.toggle()
        #wdt.feed()
        cl, addr = s.accept()
        print('client connected from', addr)
        request = cl.recv(1024)
        data = str(request)
        direction = (data[1:20].split(' ')[1].replace('/',''))
        
        if(direction =='forwards'):
            move_forward()
        elif(direction == 'left'):
            turn_left()
        elif(direction == 'right'):
            turn_right()
        elif(direction == 'backwards'):
            move_backward()
        elif(direction == 'stop'):
            stop()
            
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        time.sleep(0.2)
        cl.send(generateHTML())
        cl.close()


    except OSError as e:
        cl.close()
        s.close()
        print(f'{e}')
        blink_error(e)
        print('connection closed')
        restart()