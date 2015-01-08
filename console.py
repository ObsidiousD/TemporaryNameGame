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
    print 'Description of room:\n'

    while True:
        text = raw_input('')
        if text == '':
            break
        room['desc'] = room['desc']+text+'\\n'
    
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
def add_item():
    global resource_dir
    items = {}
    fulldesc = str()
    
    try:
        filein = open(resource_dir+'item_list.dat','r')
        items = filein.read()
        filein.close()
        os.remove(resource_dir+'item_list.dat')
        items = json.loads(items)
    except:
        print 'Pre-existing item file was corrupt | A new one will be created'
        try:
            filein = open(resource_dir+'item_list.dat','w')
            filein.close()
            items = {}
        except:
            print 'Couldn\'t create the new file'
            return False
    item_id = int(raw_input('Item ID: '))
    name = raw_input('Item name: ')
    items[item_id] = {}
    items[item_id]['name'] = name
    print 'Description:'
    while True:
        text = raw_input('')
        if text == '':
            break
        fulldesc = fulldesc+text+'\\n'
    items[item_id]['desc'] = fulldesc

    items[item_id]['type'] = raw_input('Item Type: ')
    items[item_id]['attack'] = int(raw_input('Item Attack: '))
    items[item_id]['defense'] = int(raw_input('Item Defense: '))
    items[item_id]['health'] = int(raw_input('Item Health: '))
    items[item_id]['mana'] = int(raw_input('Item Mana: '))
    items[item_id]['crit'] = int(raw_input('Critical chance (out of 100): '))
    items[item_id]['effect'] = int(raw_input('Effect ID: '))

    print 'Saving item...',
    try:
        items_str = json.dumps(items)
        filein = open(resource_dir+'item_list.dat','w')
        filein.write(items_str)
        filein.close()
    except:
        print 'Failed'
        return False
    else:
        print 'Success'
        return True
#
#
#
#
#
#Console Command Entry
'''
while True:
    command = raw_input('Command >')

    if command == 'create room':
        create_room()

    if command == 'add item':
        add_item()
'''
