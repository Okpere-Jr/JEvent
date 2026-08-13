# JEvent

JEvent is a Python library that makes it easy to add gamepad support to keyboard-controlled Tkinter games.

The gamepad is translated into keyboard-style events, so your existing keyboard input functions can handle both.

## Installation

```bash
pip install JEvent
```

## Basic usage

Suppose your game already has:

```python
def on_key_press(event):
    if event.keysym == "w":
        player.move_up()
    elif event.keysym == "s":
        player.move_down()

root.bind("<KeyPress>", on_key_press)
```

Add:

```python
import JEvent
```

and replace:

```python
root.mainloop()
```

with:

```python
JEvent.mainloop(on_key_press)
```

Because JEvent runs alongside Tkinter, add:

```python
root.update()
```

to your input function.

That's it.

## How it works

JEvent converts gamepad input into `JEvent` objects containing:

- `event.key` — the gamepad control
- `event.keysym` — the corresponding keyboard key
- `event.type` — `<KeyPress>` or `<KeyRelease>`
- `event.value` — the control's current value

For example:

```text
Gamepad Left Stick Up
        ↓
JEvent(keysym="w")
        ↓
your existing keyboard handler
```

This means your game can use the same input logic for keyboard and gamepad controls.

## Custom controls

Use `JEvent.configure()` to change the default mapping:

```python
JEvent.configure(...)
```

This allows different games to use different keyboard mappings.

## Direct gamepad input

JEvent can also be used for games that aren't keyboard-based.

You can inspect:

```python
event.key
event.value
event.keysym
event.pressed
event.released
```

This lets you use both the translated keyboard-style input and the original gamepad-oriented information.

## `doublify()` — Experimental

JEvent also provides `doublify()` as an optional convenience feature.

It is intended to make adding gamepad support to an existing Tkinter game even easier by working with the game's existing keyboard input setup.

**`doublify()` is experimental and unstable. It is not required to use JEvent.**

If you prefer a predictable and explicit setup, use `JEvent.mainloop()` directly as described above.

## Why JEvent?

Without JEvent, adding gamepad support to a keyboard-controlled game often means writing separate input handling:

```text
Keyboard ──→ game logic
Gamepad  ──→ game logic
```

With JEvent:

```text
Keyboard ──┐
           ├──→ existing input handler ──→ game logic
Gamepad ───┘
```

Your game can therefore be designed around keyboard input first, then gain gamepad support without rewriting its game logic.

The reverse is also possible: a game can use JEvent's gamepad events directly and later accept keyboard input through the same keyboard-style interface.

## Scope

JEvent is designed primarily for simple, single-gamepad Tkinter games.

It is not intended to replace Pygame's full joystick API.
