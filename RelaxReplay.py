

import os, json, ntpath, threading

rattlepath = os.path.join( os.getcwd(), "win_rattle.exe" )

def get_stat_sheets( json_data ):
    """ Get the stat sheets of all players in the replay file. """
    get_entries = lambda v : v['header']['properties']['value']['PlayerStats']['value']['array_property']
    team_value = lambda v : v['value']['Team']['value']['int_property']
    player_name = lambda v : v['value']['Name']['value']['str_property']
    assist_value = lambda v : v['value']['Assists']['value']['int_property']
    goal_value = lambda v : v['value']['Goals']['value']['int_property']
    saves_value = lambda v : v['value']['Saves']['value']['int_property']
    shots_value = lambda v : v['value']['Shots']['value']['int_property']
    score_value = lambda v : v['value']['Score']['value']['int_property']
    
    return [{
                "Team"    : team_value( key ),
                "Name"    : player_name( key ),
                "Assists" : assist_value( key ),
                "Goals"   : goal_value( key ),
                "Saves"   : saves_value( key ),
                "Shots"   : shots_value( key ),
                "Score"   : score_value( key )
            } for key in get_entries( json_data ) ]
    

def call_rattle( replay, path ):
    cmd = "win_rattle.exe decode \"{}\" > \"{}\"".format( replay, path )
    os.system( cmd )


def replay_to_json( replay ):
    """ Convert a replay to JSON using rattletrap. """
    json_path = os.path.join( os.getcwd(), "output.json" )
    call_rattle( replay, json_path )
    with open( json_path, 'r' ) as f:
        json_data = json.load( f )
    return json_data


def get_roster( json_data, team ):
    team_value = lambda v : v['value']['Team']['value']['int_property']
    player_name = lambda v : v['value']['Name']['value']['str_property']
    get_roster = lambda v : v['header']['properties']['value']['PlayerStats']['value']['array_property']
    rosters = [ ( team_value( key ), player_name( key ) ) for key in get_roster( json_data ) ]
    return [ key[1] for key in rosters if key[0] == team ]


def get_orange_roster( json_data ):
    """ Get the roster of the orange team. """
    return get_roster( json_data, 0 )


def get_blue_roster( json_data ):
    """ Get the roster of the blue team. """
    return get_roster( json_data, 1 )
    

def get_replay_name( json_data ):
    """ Get the name of the parsed replay file. """
    return json_data['header']['properties']['value']['ReplayName']['value']['str_property']


def get_game_mode( json_data ):
    """ Return a string representing the game mode of the parsed replay. """
    return "{}v{}".format( len( get_blue_roster(json_data) ), len( get_orange_roster(json_data) ) )


    
if __name__ == "__main__":
    replay_file_path = os.path.join( os.getcwd(), "test_replay.replay" )
    json_data = replay_to_json( replay_file_path )

    print( "Replay Name:\n\t{}".format( get_replay_name( json_data ) ) )
    print( "Game Mode:\n\t{}".format( get_game_mode( json_data ) ) )

    print( "Orange Team:\n\t{}\n".format(
        "\n\t".join( get_orange_roster(json_data) ) )
    )
    
    print( "Blue Team:\n\t{}\n".format(
        "\n\t".join( get_blue_roster(json_data) ) )
    )
    
