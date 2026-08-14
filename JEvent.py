import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
from math import ceil, isclose
import pygame
os.environ['SDL_VIDEODRIVER'] = 'windib'
import warnings


buttons = ['B','A','X','Y','L1','R1','-','+','LPad',"RPad",'HOME','LPad X','LPad Y','RPad X','RPad Y', 'L2','R2']
keymap =['space','e','r','q','shift_L','x','c','z','Tab','Return','Escape','ctrl_L','m','a','d','w','s','j','l','i','k','1','2','3','4','Left','Right','Up','Down']


class JEvent:
    """
    Stands for: (Joshua Event / Joystick Event), Whichever you choose.
    A simple type which makes it easy to process Gamepad Events with features for integration with Tkinter.
    Stores the Gamepad Interaction which occured, if a key was pressed or released, an the state as a number from the range (0,1) [The Origin is Bottom-Left]
    ==> Also includes a keysym value, so a classic Tkinter-based function can process JEvents like Tkinter events.
        The tkinter keymap can be changed with the configure function.
    ==> Has a self.isnt()  -handy for checking if 2 JEvents are different [And by implication if a button has been pressed]
    ==> Has a self.eval_keys() to re-evaluate the keysym if any values change.
    """
    def __init__(self,key='',type=None,value=0):
        self.type = type
        self.key = key
        self.value = value
        self.keysym = ''
        self.eval_keys()
        
    def isnt (self,event2):
        if self.type == event2.type:
            if self.key == event2.key:
                if self.value == event2.value:
                    return False
        return True
    
    @property
    def pressed(self):
        return self.type == "<KeyPress>"

    @property
    def released(self):
        return self.type == "<KeyRelease>"
    
    def __repr__(self):
        return f"JEvent({self.key!r}, {self.type!r}, {self.value!r})"
    
    def __eq__(self, other):
        return (
            self.type == other.type and
            self.key == other.key and
            self.value == other.value
        )
    
    def __bool__(self):
        return self.isnt(JEvent())
   
    def eval_keys(self):
        global keymap
        if self.key == 'A':
            self.keysym = keymap[0]
        elif self.key == 'B':
            self.keysym = keymap[1]
        elif self.key == 'X':
            self.keysym = keymap[2]
        elif self.key == 'Y':
            self.keysym = keymap[3]
        elif self.key == 'L1':
            self.keysym = keymap[4]
        elif self.key == 'R1':
            self.keysym = keymap[5]
        elif self.key == 'L2':
            self.keysym = keymap[6]
        elif self.key == 'R2':
            self.keysym = keymap[7]
        elif self.key == '-':
            self.keysym = keymap[8]
        elif self.key == '+':
            self.keysym = keymap[9]
        elif self.key == 'HOME':
            self.keysym = keymap[10]
        elif self.key == 'LPad':
            self.keysym = keymap[11]
        elif self.key == 'RPad':
            self.keysym = keymap[12]
        
        # ===== ANALOG STICKS (with threshold) =====
        elif self.key == 'LPad X':
            if self.value < -0.5: self.keysym = keymap[13]
            elif self.value > 0.5: self.keysym = keymap[14]
            else: self.keysym = None
        elif self.key == 'LPad Y':
            if self.value < -0.5: self.keysym = keymap[15]
            elif self.value > 0.5: self.keysym = keymap[16]
            else: self.keysym = None
        elif self.key == 'RPad X':
            if self.value < -0.5: self.keysym = keymap[17]
            elif self.value > 0.5: self.keysym = keymap[18]
            else: self.keysym = None
        elif self.key == 'RPad Y':
            if self.value < -0.5: self.keysym = keymap[19]
            elif self.value > 0.5: self.keysym = keymap[20]
            else: self.keysym = None
        
        elif self.key == 'DPad':
            x, y = self.value
            
            # Diagonals (both axes active)
            if x < -0.5 and y < -0.5:
                self.keysym = keymap[21]      # Up-Left (or use 'q' / '7')
            elif x > 0.5 and y < -0.5:
                self.keysym = keymap[22]      # Up-Right (or use 'e' / '9')
            elif x < -0.5 and y > 0.5:
                self.keysym =   keymap[23]     # Down-Left (or use 'z' / '1')
            elif x > 0.5 and y > 0.5:
                self.keysym = keymap[24]     # Down-Right (or use 'c' / '3')
            # Cardinals
            elif x < -0.5:
                self.keysym = keymap[25]      # Left
            elif x > 0.5:
                self.keysym = keymap[26]      # Right
            elif y < -0.5:
                self.keysym = keymap[27]      # Up
            elif y > 0.5:
                self.keysym = keymap[28]      # Down
            else:
                self.keysym = None          

def configure(keyboard_map):
    global keymap
    '''
    Changes the keysyms for events binded.
    The keyboard_map sould be an array corresponding to which keys/events should be binded to presses on the gamepad.
    The events/keys they map to, in order, are:
        ['B/⭕','A/❌ ','X/☐','Y/△️','L1','R1','L2','R2','-','+','HOME','LPad',"RPad",'LPad Left','LPad Right','LPad Up','LPad Down','RPad Left','RPad Right','RPad Up','RPad Down','DPad NW','DPad NE','DPad SW','DPad SE','DPad W','DPad E','DPad N','DPad S']
    '''
    if isinstance(keyboard_map,dict):
        for elem in list(keyboard_map):
            keymap[elem] = keyboard_map[elem]
    keymap = list(keyboard_map)
    
def on_pad_press(event):
    btn=''
    typ=None
    val=0
    if event.type == pygame.JOYBUTTONDOWN:
        typ = "<KeyPress>"
        btn = buttons[event.button]
        val = 1
    if event.type == pygame.JOYBUTTONUP:
        typ = '<KeyRelease>'
        btn = buttons[event.button]
        val = 0
    if event.type == pygame.JOYAXISMOTION:
        typ = "<KeyPress>"       
        val = (event.value + 1)/2
        if (event.axis == 1) or (event.axis == 3):
            val = 1 - val
            #val += 1
        if isclose(val, 0.5, rel_tol=1e-3):
            typ = '<KeyRelease>'
        val = round(val,2)
        if (event.axis == 4) or (event.axis == 5):
            val = ceil(val)
            if val == 0:
                typ = '<KeyRelease>'       
        btn = buttons[event.axis+11]
    if event.type == pygame.JOYHATMOTION:
        typ = "<KeyPress>"
        btn = "DPad"
        if event.value == (0,0):
            typ = '<KeyRelease>'
        val =  event.value   
    return JEvent(btn,typ,val)    

def mainloop(event_func, condition = (lambda : False) ):
    '''
    condition -> A function to check when the main/'game' loop should exit
    event_func -> A function called with the latest available gamepad event.
    Call event_func(event) for each Event/Button Press from a single gamepad until condition() returns False
    '''
    pygame.init()
    pygame.joystick.init()
    if pygame.joystick.get_count() == 0:
        warnings.warn("NO gamepad detected.")#,category=ResourceWarning)
        while not condition() :
            if pygame.joystick.get_count() != 0:
                break
            event_func(JEvent())
    gamepad = pygame.joystick.Joystick(0)
    event = pygame.event.get()[-1]
    while not condition() :
        try:
            if pygame.joystick.get_count() == 0:
                warnings.warn("NO gamepad detected.")
                mainloop(event_func,condition)
            event =  pygame.event.get()[-1]
            jevent = on_pad_press(event)
            event_func(jevent)
        except IndexError as e:
            pass # No button was pressed


def doublify(root):
    """Return the actual function object bound to <KeyPress>"""
    bindings = root.bind()
    import ast
    try:
        binding_tuple = ast.literal_eval(bindings)
        for event_seq, callback, add_flag in binding_tuple:
            if event_seq in ["<KeyPress>", "<Key>"]:
                return callback
    except:
        return None
    def mask():
        callback()
        root.update()
    mainloop(mask) 

if __name__ == "__main__":
    print('JE to TK loaded successfully')
    sentinel = JEvent()
    
    def test(event):
        global sentinel
        if event.isnt(JEvent()):
            print(event)
        sentinel = event

    def B_pressed():
        global sentinel
        return sentinel == JEvent('B','<KeyRelease>',0)

    mainloop(test,B_pressed) # Print info about each event until B is pressed.
    pygame.quit()
