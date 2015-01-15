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
item_dir = local_dir+'Resources/item_data/'
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
#
#
#
#
#
#Add Item Function
def add_item():
    global resource_dir
    fulldesc = str()
    
    item_id = int(raw_input('Item ID: '))
    item_id = str(item_id)
    name = raw_input('Item name: ')
    item = {}
    item['name'] = name
    print 'Description:'
    while True:
        text = raw_input('')
        if text == '':
            break
        fulldesc = fulldesc+text+'\\n'
    item['desc'] = fulldesc

    item['type'] = raw_input('Item Type: ')
    item['level'] = int(raw_input('Item Level: '))
    item['attack'] = int(raw_input('Item Attack: '))
    item['defense'] = int(raw_input('Item Defense: '))
    item['health'] = int(raw_input('Item Health: '))
    item['mana'] = int(raw_input('Item Mana: '))
    item['crit'] = int(raw_input('Critical chance (out of 100): '))
    item['effect'] = int(raw_input('Effect ID: '))
    item['phrase'] = raw_input('Item Attack Phrase: ')

    item['class'] = []
    if raw_input('Warrior Usable (y/n): ') == 'y':
        item['class'].append('Warrior')
    if raw_input('Ranger Usable (y/n): ') == 'y':
        item['class'].append('Ranger')
    if raw_input('Mage Usable (y/n): ') == 'y':
        item['class'].append('Mage')

    print 'Saving item...'
    try:
        fileout = open(item_dir+item_id,'w')
        fileout.write(json.dumps(item))
        fileout.close()
    except:
        print 'Failed'
    else:
        print 'Success'
#
#
#
#
#
#Add Enemy Function
def add_enemy():
    enemy = {}
    fulldesc = str()

    enemy['name'] = raw_input('Enemy Name: ')
    enemy['level'] = int(raw_input('Enemy Level: '))

    print 'Enemy Description:'
    while True:
        text = raw_input('')
        if text == '':
            break
        fulldesc = fulldesc+text+'\\n'
    enemy['desc'] = fulldesc

    enemy['attack_phrases'] = []
    print 'Please enter a series of attack phrases'
    print 'Enter a blank line when done'
    while True:
        phrase = raw_input('AP: ')
        if phrase == '':
            break
        enemy['attack_phrases'].append(phrase)
    enemy['health'] = int(raw_input('Enemy Health: '))
    enemy['attack'] = int(raw_input('Enemy Attack: '))
    enemy['defense'] = int(raw_input('Enemy Defense: '))
    enemy['death_phrase'] = raw_input('Enemy Death Phrase: ')

    print 'Saving enemy file...',
    try:
        fileout = open(enemy_dir+enemy['name'],'w')
        fileout.write(json.dumps(enemy))
        fileout.close()
    except:
        print 'Failed'
    else:
        print 'Success'
#
#
#
#
#
#Update Item Function
def update_item(item_id):
    global item_dir
    item_id = str(item_id)

    try:
        filein = open(item_dir+item_id,'r')
        item = json.loads(filein.read())
        filein.close()
    except:
        return 'Failed to load item'

    attribute = raw_input('Attribute to update: ')
    try:
        print item[attribute]
        print ''
    except:
        print 'This item doesn\'t exist. Create it? (y/n)'
    else:
        print 'Do you wish to edit this? (y/n)'

    resp = raw_input('> ')
    if resp == 'n':
        return False

    item[attribute] = raw_input(attribute+': ')

    try:
        fileout = open(item_dir+item_id,'w')
        fileout.write(json.dumps(item))
        fileout.close()
    except:
        print 'Failed to save'
    else:
        print 'Saved'
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
