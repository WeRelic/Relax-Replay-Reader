# RelaxReplayUI.py

import os, tkinter, RelaxReplay
from tkinter import ttk, filedialog, Label
from tkinter.ttk import Separator

# C:\Users\Wes\Documents\My Games\Rocket League\TAGame\Demos

root = tkinter.Tk()
root.title( "Replay Extractor" )
root.wm_iconbitmap( bitmap = "replay_icon.ico" )
replay_path = None
json_output_path = None
json_data = None

    

widget_list = {
    "orange" : [],
    "blue"   : []
}

class Statsheet:
    def __init__( self,
                  player_name,
                  team,
                  score = 0,
                  goals = 0,
                  assists = 0,
                  saves = 0,
                  shots = 0 ):
        self.name = player_name
        if team == 0:
            self.team = "Orange"
        elif team == 1:
            self.team = "Blue"
        self.widgets = {
            "name"     : Label( root, text = "{}:".format(player_name), justify = "left" ),
            "score"    : Label( root, text = str(score), justify = "center" ),
            "goals"    : Label( root, text = str(goals), justify = "center" ),
            "assists"  : Label( root, text = str(assists), justify = "center" ),
            "saves"    : Label( root, text = str(saves), justify = "center" ),
            "shots"    : Label( root, text = str(shots), justify = "center" )
        }


    def grid_format( self, which_row = 0 ):
        col = 0
        for k, v in self.widgets.items():
            v.grid( padx = (0,5)[k=="name"], column = col, row = which_row, sticky = 'w', columnspan = (1,2)[k=="name"] )
            col += (1,3)[k=="name"]


def load_replay():
    global json_data
    clear_ui()
    replay_path = filedialog.askopenfilename(initialdir="/")
    if replay_path != "" and replay_path != None:
        json_data = RelaxReplay.replay_to_json(replay_path)
        
        statsheets = RelaxReplay.get_stat_sheets(json_data)
        
        # Adding to the widget list.
        widget_list["gamemode"] = Label( root, text = RelaxReplay.get_game_mode(json_data) )
        widget_list["replayname"] = Label( root, text = RelaxReplay.get_replay_name(json_data) )
        for x in statsheets:
            if x["Team"] == 0:
                widget_list["orange"].append(
                    Statsheet( x["Name"], "Orange", x["Score"], x["Goals"], x["Assists"], x["Saves"], x["Shots"] )
                )
            else:
                widget_list["blue"].append(
                    Statsheet( x["Name"], "blue", x["Score"], x["Goals"], x["Assists"], x["Saves"], x["Shots"] )
                )
        draw_main_screen()
        os.remove( os.path.join( os.getcwd(), "output.json" ) )
        
    
def cleanup():
    global root, json_output_path
    if json_output_path != None:
        os.remove( json_output_path )
    root.destroy()
    
    
def clear_ui():
    for key, widget in widget_list.items():
        if key in [ "orange", "blue" ]:
            for i in widget:
                i.destroy()
        else:
            widget.destroy()


def draw_main_screen():
    Label( root, text = "Orange Team:", justify = "right" ).grid( row = 3, column = 0, columnspan = 2, sticky = 'w' )
    Label( root, text = "Blue Team:", justify = "right" ).grid( row = 9, column = 0, columnspan = 2, sticky = 'w' )
    Label( root, text = "Replay Name:", justify = "right" ).grid( row = 0, column = 0, sticky = 'w' )
    Label( root, text = "Gamemode:", justify = "right" ).grid( row = 1, column = 0, sticky = 'w' )
    Label( root, text = "Score", justify = "right" ).grid( row = 2, column = 3, sticky = 'e' )
    Label( root, text = "Goals", justify = "right" ).grid( row = 2, column = 4, sticky = 'e' )
    Label( root, text = "Assists", justify = "right" ).grid( row = 2, column = 5, sticky = 'e' )
    Label( root, text = "Saves", justify = "right" ).grid( row = 2, column = 6, sticky = 'e' )
    Label( root, text = "Shots", justify = "right" ).grid( row = 2, column = 7, sticky = 'e' )
    r = 4
    for i in widget_list["orange"]:
        i.grid_format( r )
        r += 1
    r = 10
    for i in widget_list["blue"]:
        i.grid_format( r )
        r += 1
    try:
        widget_list["gamemode"].grid( row = 1, column = 1, columnspan = 5 )
        widget_list["replayname"].grid( row = 0, column = 1, columnspan = 5 )
    except:
        pass

# Creating and populating the menu bar.
menubar = tkinter.Menu( root )
menu = tkinter.Menu( menubar, tearoff = 0 )
menu.add_command( label = "Load Replay", command = load_replay )
menu.add_command( label = "Exit", command = cleanup )
menubar.add_cascade( label="Menu", menu = menu )
root.config( menu = menubar )
draw_main_screen()
root.mainloop()
