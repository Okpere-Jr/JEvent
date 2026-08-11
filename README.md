# JEvent
A Python library to add Single Gamepad Support to simple Tkinter games easily    
#### Basic Usage Information    
For most single-player keyboard games designed with Tkinter, gamepad support can be added with:    
1. => Add to the beginning of the main file:     
>`import JEvent`

2. => Add in your on_key_press function:    
>`root.update()`

3. => Replace:    
>`root.mainloop()`

with:    
>`JEvent.mainloop(on_key_press)`

If the Controls/Mapping feels a bit off, you can use `JEvent.configure()` to adjust it.    
#### Random Information.    
(I'm also not the best at writing documentations)
