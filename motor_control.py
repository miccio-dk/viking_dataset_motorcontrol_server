import time
from flask import Flask
from flask_serial import Serial

app = Flask(__name__)
app.config['SERIAL_TIMEOUT'] = 0.1
app.config['SERIAL_PORT'] = '/dev/tty.usbmodem14101'
app.config['SERIAL_BAUDRATE'] = 9600
app.config['SERIAL_BYTESIZE'] = 8
app.config['SERIAL_PARITY'] = 'N'
app.config['SERIAL_STOPBITS'] = 1
ser = Serial(app)

motor_state = {
    'M1': 'DONE',
    'M2': 'DONE'
}

@app.route('/move/<string:motor>/<string:direction>/<int:amount>')
def move(motor, direction, amount):
    motor = motor.upper()
    cmd = 'ROTATE_{}_{}_{:03d}\n'.format(
        motor, 
        direction.upper(), 
        amount
    )
    #print(cmd)
    ser.on_send(cmd)
    motor_state[motor] = 'WAIT'
    #print('MOVE', motor_state)
    return ''


@app.route('/poll/<string:motor>')
def poll(motor):
    #print('POLL', motor_state)
    motor = motor.upper()
    return motor_state[motor]


@ser.on_message()
def handle_message(msg):
    for motor in ['M1', 'M2']:
        if motor in msg.decode():
            motor_state[motor] = 'DONE'
            return
    print('ERROR!!! ', msg)
    # set motors to 
    for motor in ['M1', 'M2']:
        motor_state[motor] = 'DONE'
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)