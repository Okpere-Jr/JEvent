# JEvent

**JEvent** is a lightweight Python library for using gamepad/joystick
input like keyboard input.

It is designed especially for simple games and applications where you
already have keyboard controls and want to add gamepad support without
rewriting your input system.


## Features

-   Converts gamepad events into keyboard-style events.
-    Provides a `keysym` attribute so the same callback can handle
    keyboard-like input.
-    Supports buttons, analog sticks, triggers, and the D-pad.
-    Customizable gamepad-to-keyboard mappings with `configure()`.
-    Handles controller disconnection and reconnection while the event
    loop is running.
-    Designed to be simple to add to existing Python programs.
-    Tested without requiring a gamepad-specific window.
-    Uses Pygame's joystick support.
-    Includes optional `doublify()` functionality for Tkinter
    integration. **`doublify()` is experimental/unstable and is not
    required.**

## Installation

``` bash
pip install JEvent
```

For TestPyPI:

``` bash
pip install -i https://test.pypi.org/simple/ JEvent
```

## Basic usage

``` python
import JEvent

def on_key_press(event):
    if event.keysym == 'a':
        move_left()
    elif event.keysym == 'd':
        move_right()

JEvent.mainloop(on_key_press)
```

`mainloop()` continuously checks for gamepad input and passes a `JEvent`
object to your callback.

The idea is simple: **let your existing keyboard-oriented code handle
gamepad input too.**

## The `JEvent` object

A `JEvent` contains:

``` python
event.key
event.type
event.value
event.keysym
```

### `key`

The gamepad control that generated the event. Supported controls
include:

``` text
A, B, X, Y
L1, R1, L2, R2
-, +, HOME
LPad, RPad
LPad X, LPad Y
RPad X, RPad Y
DPad
```

### `type`

Events use:

``` python
"<KeyPress>"
"<KeyRelease>"
```

Convenience properties are also available:

``` python
event.pressed
event.released
```

### `value`

The underlying state/value of the event.

Buttons normally use `1` for press and `0` for release. Analog controls
use normalized values, while D-pad events use an `(x, y)` pair.

### `keysym`

The keyboard-style key associated with the gamepad event.

For example:

``` python
if event.keysym == 'e':
    print("A button")
```

The mapping can be changed with `configure()`.

## Comparing events

`==` compares the event **type and control**:

``` python
if event == JEvent('A', '<KeyPress>', 1):
    ...
```

For an exact comparison, including the value, use:

``` python
if event.isnt(other_event):
    ...
```

This distinction is intentional: two motions of the same analog control
are still the same kind of event, while `isnt()` lets you check whether
their complete states differ.

`JEvent` also has a boolean representation:

``` python
if event:
    print("A real event was received")
```

An empty `JEvent()` evaluates as false.

## Custom mappings

Change the keyboard mapping with `configure()`:

``` python
JEvent.configure([
    'space', 'e', 'r', 'q',
    'shift_L', 'x', 'c', 'z',
    'Tab', 'Return', 'Escape',
    'ctrl_L', 'm',
    'a', 'd', 's', 'w',
    'j', 'l', 'k', 'i',
    '1', '2', '3', '4',
    'Left', 'Right', 'Up', 'Down'
])
```

The mapping order is:

``` text
B
A
X
Y
L1
R1
L2
R2
-
+
HOME
LPad
RPad
LPad Left
LPad Right
LPad Down
LPad Up
RPad Left
RPad Right
RPad Down
RPad Up
DPad NW
DPad NE
DPad SW
DPad SE
DPad W
DPad E
DPad N
DPad S
```

A dictionary can also be used to replace selected entries:

``` python
JEvent.configure({
    0: 'space',
    1: 'e'
})
```

## Analog sticks

Analog stick movement is translated into directional keyboard-style
events.

For example:

``` python
if event.keysym == 'a':
    move_left()
elif event.keysym == 'd':
    move_right()
elif event.keysym == 'w':
    move_up()
elif event.keysym == 's':
    move_down()
```

The analog value is available through `event.value`.

The neutral position is treated as a release, allowing an analog stick
to behave more like a keyboard direction.

## D-pad

D-pad events use:

``` python
event.key == 'DPad'
```

and store the D-pad position as an `(x, y)` pair.

JEvent also provides keyboard-style mappings for:

``` text
DPad NW
DPad NE
DPad SW
DPad SE
DPad W
DPad E
DPad N
DPad S
```

## Tkinter integration

JEvent was designed with Tkinter integration in mind.

A normal Tkinter-style callback can process a JEvent because it has a
`keysym` attribute:

``` python
def on_key_press(event):
    if event.keysym == 'a':
        move_left()
    elif event.keysym == 'd':
        move_right()
```

If you are running JEvent alongside Tkinter, pending Tk events can be
serviced with:

``` python
root.update()
```

For example:

``` python
def on_key_press(event):
    root.update()

    if event.keysym == 'a':
        move_left()
```

This can allow Tkinter callbacks, redraws, and scheduled work to be
processed while JEvent's loop is running.

## `mainloop()`

The main loop is:

``` python
JEvent.mainloop(event_func)
```

It also accepts:

``` python
JEvent.mainloop(
    event_func,
    condition=lambda: False,
    verbose=True
)
```

### `event_func`

The function receiving each `JEvent`:

``` python
def event_func(event):
    print(event)
```

### `condition`

A function that determines when the loop should stop:

``` python
running = True

def finished():
    return not running

JEvent.mainloop(event_func, finished)
```

The loop continues until `condition()` returns `True`.

### `verbose`

Controls warnings about gamepad availability:

``` python
JEvent.mainloop(event_func, verbose=False)
```

## No-window use

JEvent has been tested without requiring a gamepad-specific window.

This is useful when another framework already owns the application's
window, or when you simply want to receive controller input without
creating another one.

## Controller reconnection

The main loop can continue running if the controller is disconnected.

When no gamepad is available, the callback receives an empty:

``` python
JEvent()
```

When a gamepad becomes available again, JEvent reconnects to it.

This means an application does not have to restart its input loop just
because a controller was unplugged and plugged back in.

## Lower-level API: `on_pad_press()`

If you want to handle Pygame events yourself, `on_pad_press()` converts
a Pygame joystick event into a `JEvent`:

``` python
event = JEvent.on_pad_press(pygame_event)
```

This is useful when you need more control over the event loop.

## `eval_keys()`

A `JEvent` calculates its `keysym` from its current control and value.

You can re-evaluate it with:

``` python
event.eval_keys()
```

This is useful after changing an event's state or the mapping.

## `doublify()` --- Experimental

`doublify()` is **optional and unstable**.

It is intended to help connect JEvent input with an existing Tkinter
`<KeyPress>` binding.

You do **not** need `doublify()` to use JEvent.

For normal use, prefer:

``` python
JEvent.mainloop(...)
```

and the `event.keysym` interface.

## Example: add gamepad support to keyboard-style movement

``` python
import JEvent

x = 0

def move_left():
    global x
    x -= 1

def move_right():
    global x
    x += 1

def on_input(event):
    if event.keysym == 'a':
        move_left()
    elif event.keysym == 'd':
        move_right()

JEvent.mainloop(on_input)
```

The same movement functions can also be called by a normal keyboard
binding.

That is the main purpose of JEvent:

``` text
gamepad
   ↓
 JEvent
   ↓
keyboard-style event
   ↓
existing input handler
   ↓
game logic
```

Instead of rewriting a keyboard-controlled game to understand
controllers separately.

## Requirements

JEvent uses Pygame's joystick support.

It is intended for Python programs that can use Pygame's joystick
functionality.

