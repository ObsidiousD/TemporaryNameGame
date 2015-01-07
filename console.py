#Developer Functions
#
#Written By MM12
import os
import json

local_dir = os.getcwd()+'/'
resource_dir = local_dir+'Resources/'
player_dir = local_dir+'Resources/player_data/'
room_dir = local_dir+'Resources/room_data/'
enemy_dir = local_dir+'Resources/enemy_data/'
#
#
#
#
#
#Create Room Function
def create_room():
    global room_dir
    room = {}

    room_id = str(raw_input('Room ID: '))
    room['name'] = raw_input('Name: ')
    room['desc'] = raw_input('Description of room: ')
    room['spawn_chance'] = raw_input('Odds enemy will spawn (out of 100): ')
    room['max_enemy'] = raw_input('Max enemy level: ')
    room['min_enemy'] = raw_input('Min enemy level: ')
    room['loot_chance'] = raw_input('Loot chance (out of 100): ')
    room['effects'] = raw_input('Effect codes: ')
    room['north'] = raw_input('Room north: ')
    room['north_id'] = raw_input('North ID: ')
    room['south'] = raw_input('Room south: ')
    room['south_id'] = raw_input('South ID: ')
    room['east'] = raw_input('Room east: ')
    room['east_id'] = raw_input('East ID: ')
    room['west'] = raw_input('Room west: ')
    room['west_id'] = raw_input('West ID: ')

    print 'Saving room...',
    room_str = json.dumps(room)
    fileout = open(room_dir+room_id,'w')
    fileout.write(room_str)
    fileout.close()
    print 'Done'
    return True
