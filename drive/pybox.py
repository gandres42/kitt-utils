import pygame
import threading

_values = {
    'l_joy_x': 0,
    'l_joy_y': 0,
    'r_joy_x': 0,
    'r_joy_y': 0,
    'd_pad_x': 0,
    'd_pad_y': 0,
    'l_trigger': 0,
    'r_trigger': 0,
    'l_bumper': 0,
    'r_bumper': 0,
    'select': 0,
    'start': 0,
    'r_joy_button': 0,
    'l_joy_button': 0,
    'a_button': 0,
    'b_button': 0,
    'x_button': 0,
    'y_button': 0
}

_callbacks = {
    'l_joy_x': None,
    'l_joy_y': None,
    'r_joy_x': None,
    'r_joy_y': None,
    'd_pad_x': None,
    'd_pad_y': None,
    'l_trigger': None,
    'r_trigger': None,
    'l_bumper': None,
    'r_bumper': None,
    'select': None,
    'start': None,
    'r_joy_button': None,
    'l_joy_button': None,
    'a_button': None,
    'b_button': None,
    'x_button': None,
    'y_button': None
}


_listen_thread = None
_active = False
_controller = None

def listen():
    while _active:
        for event in pygame.event.get():
            if 'joy' in event.dict:
                if 'axis' in event.dict:
                    if event.dict['axis'] == 0:
                        _values['l_joy_x'] = round(event.dict['value'], 3)
                        _call('l_joy_x')
                    if event.dict['axis'] == 1:
                        _values['l_joy_y'] = round(event.dict['value'] * -1, 3)
                        _call('l_joy_y')
                    if event.dict['axis'] == 2:
                        _values['r_joy_x'] = round(event.dict['value'], 3)
                        _call('r_joy_x')
                    if event.dict['axis'] == 3:
                        _values['r_joy_y'] = round(event.dict['value'] * -1, 3)
                        _call('r_joy_y')
                    if event.dict['axis'] == 4:
                        _values['r_trigger'] = round((event.dict['value'] + 1) / 2, 3)
                        _call('r_trigger')
                    if event.dict['axis'] == 5:
                        _values['l_trigger'] = round((event.dict['value'] + 1) / 2, 3)
                        _call('l_trigger')
                if 'button' in event.dict:
                    if event.dict['button'] == 0:
                        if _values['a_button'] == 0:
                            _values['a_button'] = 1
                        else:
                            _values['a_button'] = 0
                        _call('a_button')
                    if event.dict['button'] == 1:
                        if _values['b_button'] == 0:
                            _values['b_button'] = 1
                        else:
                            _values['b_button'] = 0
                        _call('a_button')
                    if event.dict['button'] == 2:
                        if _values['x_button'] == 0:
                            _values['x_button'] = 1
                        else:
                            _values['x_button'] = 0
                        _call('x_button')
                    if event.dict['button'] == 3:
                        if _values['y_button'] == 0:
                            _values['y_button'] = 1
                        else:
                            _values['y_button'] = 0
                        _call('y_button')
                    if event.dict['button'] == 4:
                        if _values['l_bumper'] == 0:
                            _values['l_bumper'] = 1
                        else:
                            _values['l_bumper'] = 0
                        _call('l_bumper')
                    if event.dict['button'] == 5:
                        if _values['r_bumper'] == 0:
                            _values['r_bumper'] = 1
                        else:
                            _values['r_bumper'] = 0
                        _call('r_bumper')
                    if event.dict['button'] == 6:
                        if _values['select'] == 0:
                            _values['select'] = 1
                        else:
                            _values['select'] = 0
                        _call('select')
                    if event.dict['button'] == 7:
                        if _values['start'] == 0:
                            _values['start'] = 1
                        else:
                            _values['start'] = 0
                    if event.dict['button'] == 9:
                        if _values['l_joy_button'] == 0:
                            _values['l_joy_button'] = 1
                        else:
                            _values['l_joy_button'] = 0
                        _call('l_joy_button')
                    if event.dict['button'] == 10:
                        if _values['r_joy_button'] == 0:
                            _values['r_joy_button'] = 1
                        else:
                            _values['r_joy_button'] = 0
                        _call('r_joy_button')
                if 'hat' in event.dict:
                    _values['d_pad_x'] = event.dict['value'][0]
                    _values['d_pad_y'] = event.dict['value'][1]

def _call(key):
    if _callbacks[key] is not None:
          _callbacks[key]()

def init():
    global _listen_thread, _active, _controller
    pygame.init()
    pygame.joystick.init()
    joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
    _controller = pygame.joystick.Joystick(0)
    _controller.init()
    _listen_thread = threading.Thread(target=listen, daemon=True)
    _active = True
    _listen_thread.start()

def stop():
    global _listen_thread, _active
    _active = False
    if _listen_thread is not None:
        _listen_thread.join()
        _listen_thread = None

def get_l_joy_x():
        return _values['l_joy_x']

def get_l_joy_y():
        return _values['l_joy_y']

def get_r_joy_x():
        return _values['r_joy_x']

def get_r_joy_y():
        return _values['r_joy_y']

def get_d_pad_x():
        return _values['d_pad_x']

def get_d_pad_y():
        return _values['d_pad_y']

def get_l_trigger():
        return _values['l_trigger']

def get_r_trigger():
        return _values['r_trigger']

def get_l_bumper():
        return _values['l_bumper']

def get_r_bumper():
        return _values['r_bumper']

def get_select():
        return _values['select']

def get_start():
        return _values['start']

def get_r_joy_button():
        return _values['r_joy_button']

def get_l_joy_button():
        return _values['l_joy_button']

def get_a_button():
        return _values['a_button']

def get_b_button():
        return _values['b_button']

def get_x_button():
        return _values['x_button']

def get_y_button():
        return _values['y_button']

def set_callback_l_joy_x(func):
        _callbacks['l_joy_x'] = func

def set_callback_l_joy_y(func):
        _callbacks['l_joy_y'] = func

def set_callback_r_joy_x(func):
        _callbacks['r_joy_x'] = func

def set_callback_r_joy_y(func):
        _callbacks['r_joy_y'] = func

def set_callback_d_pad_x(func):
        _callbacks['d_pad_x'] = func

def set_callback_d_pad_y(func):
        _callbacks['d_pad_y'] = func

def set_callback_l_trigger(func):
        _callbacks['l_trigger'] = func

def set_callback_r_trigger(func):
        _callbacks['r_trigger'] = func

def set_callback_l_bumper(func):
        _callbacks['l_bumper'] = func

def set_callback_r_bumper(func):
        _callbacks['r_bumper'] = func

def set_callback_select(func):
        _callbacks['select'] = func

def set_callback_start(func):
        _callbacks['start'] = func

def set_callback_r_joy_button(func):
        _callbacks['r_joy_button'] = func

def set_callback_l_joy_button(func):
        _callbacks['l_joy_button'] = func

def set_callback_a_button(func):
        _callbacks['a_button'] = func

def set_callback_b_button(func):
        _callbacks['b_button'] = func

def set_callback_x_button(func):
        _callbacks['x_button'] = func

def set_callback_y_button(func):
        _callbacks['y_button'] = func