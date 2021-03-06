#Server Framework
#
#Written By MartianMellow12 (MM12) And ObsidiousD
import thread
import socket
import os
import time
import json
import sys
import string
import webbrowser
from random import randint
from copy import deepcopy

name = 'Game Thing'
version = '0.1'
local_dir = os.getcwd()+'/'
resource_dir = local_dir+'Resources/'
player_dir = local_dir+'Resources/player_data/'
room_dir = local_dir+'Resources/room_data/'
enemy_dir = local_dir+'Resources/enemy_data/'
item_dir = local_dir+'Resources/item_data/'

host = ''
port = 8080
newline = [chr(13)+chr(10),chr(13),chr(10)]

player_data = {}
player_passwords = {}
room_data = {}
enemy_data = {}
enemy_index = []
item_data = {}
kicklist = []
banlist = []

class_chart = '''

1 | Warrior
You receive 10 extra strength points

2 | Ranger
You receive 10 extra agility points

3 | Mage
You receive 5 SP attack points and 5 SP defense points

'''
#
#
#
#
#
#In List Function
def in_list(obj,key):
    counter = int()
    
    for i in range(0,len(obj)):
        t = obj[i]
        if t == key:
            counter = counter+1
    return counter
#
#
#
#
#
#Generate Map Function
def generate_map(north,south,east,west):
    current_map = str()
    
    if north == True:
        current_map = current_map+'    N\n    |\n'
    else:
        current_map = current_map+'\n\n'
    if west == True:
        current_map = current_map+'W --'
    if east == True and west == True:
        current_map = current_map+' -- E\n'
    elif east == True and west == False:
        current_map = current_map+'     -- E\n'
    else:
        current_map = current_map+'\n'
    if south == True:
        current_map = current_map+'    |\n    S'

    return current_map
#
#
#
#
#
#Save Player Function
def save_player(player_name):
    global player_data
    global player_dir
    
    data = json.dumps(player_data[player_name])
    try:
        filein = open(player_dir+player_name+'/info.dat','w')
        filein.write(data)
        filein.close()
    except:
        return False
    return True
#
#
#
#
#
#Load Player Function
def load_player(player_name):
    global player_data
    global player_dir

    try:
        filein = open(player_dir+player_name+'/info.dat','r')
        player_data[player_name] = json.loads(filein.read())
        filein.close()
        filein = open(player_dir+player_name+'/password.dat','r')
        player_passwords[player_name] = filein.read()
        filein.close()
    except:
        return False
    return True
#
#
#
#
#
#Load Room Function
def load_room(room_id):
    global room_dir
    global room_data

    try:
        filein = open(room_dir+str(room_id),'r')
        room_data[str(room_id)] = json.loads(filein.read())
        filein.close()
    except:
        return False
    return True
#
#
#
#
#
#Create Player Function
def create_player(player_name,player_password,player_class):
    global player_dir
    global player_data

    if os.path.isdir(player_dir+player_name):
        return 2 #Code for a name that's already taken
    
    try:
        os.mkdir(player_dir+player_name)
        fileout = open(player_dir+player_name+'/password.dat','w')
        fileout.write(player_password)
        fileout.close()
    except:
        return 0 #Code for failure

    info = {
        'health':20,
        'max_health':20,
        'mana':20,
        'max_mana':20,
        'inventory':[1,2],
        'level':1,
        'class':player_class,
        'strength':10,
        'agility':10,
        'defense':10,
        'sp_attack':10,
        'sp_defense':10,
        'enemies_killed':0,
        'bosses_killed':0,
        'equipped_weapon':0,
        'equipped_shield':0,
        'equipped_item':0,
        'messages':[]
        }

    if player_class == 'Warrior':
        info['strength'] = info['strength']+10
    elif player_class == 'Ranger':
        info['agility'] = info['agility']+10
    elif player_class == 'Mage':
        info['sp_defense'] = info['sp_defense']+5
        info['sp_attack'] = info['sp_attack']+5

    player_data[player_name] = info
    save_player(player_name)
#
#
#
#
#
#Receive Function
def receive(connection):
    data = str()
    data_full = str()
    
    while True:
        data = connection.recv(1024)
        data = data.rstrip('\n')
        data = data.rstrip('\r')
        return data
#
#
#
#
#
#Clear Player Screen Function
def clear_player_screen(conn):
    try:
        for i in range(0,100):
            conn.sendall('\n')
    except:
        return False
    else:
        return True
#
#
#
#
#
#Login Function
def player_login(conn,addr):
    global name
    global class_chart
    username = str()
    password = str()
    
    conn.sendall('Please log in, or enter the username you wish to use\n')

    while True:
        conn.sendall('Username:')
        username = receive(conn)
        conn.sendall('Password:')
        password = receive(conn)

        if username in player_data:
            if password == player_passwords[username]:
                conn.sendall('Successfully logged in as '+username+'\n')
                time.sleep(1)
                clear_player_screen(conn)
                break
            else:
                conn.sendall('Incorrect password for user <'+username+'>\n')
        else:
            conn.sendall('The user <'+username+'> does not exist\n')
            conn.sendall('Would you like to create an account with the provided information (Y/N)?\n')
            answer = string.lower(receive(conn))
            if answer == 'y':
                conn.sendall('-------------------------------------\n')
                conn.sendall('What class would you like to be?\n')
                conn.sendall('Please enter the number to the left of that class\n')
                conn.sendall('\n')
                conn.sendall('Entering a custom class instead of a number is allowed\n')
                conn.sendall('but you will not receive any bonuses\n')
                conn.sendall(class_chart)
                
                pclass = str(receive(conn))
                if pclass == '1':
                    pclass = 'Warrior'
                elif pclass == '2':
                    pclass = 'Ranger'
                elif pclass == '3':
                    pclass = 'Mage'

                print 'Creating player '+username+'...',
                conn.sendall('Creating player <'+username+'>...')
                create_player(username,password,pclass)
                conn.sendall('Done\n')
                print 'Done'
                print 'Saving and loading data for '+username+'...',
                conn.sendall('Saving your player to the server...')
                save_player(username)
                load_player(username)
                conn.sendall('Done\n')
                print 'Done'
                conn.sendall('You are now logged in as '+username+'!\n')
                time.sleep(1)
                clear_player_screen(conn)
                break
    return str(username)
#
#
#
#
#
#Send Room Function
def send_room(conn,room_id,user):
    global room_data
    global player_data
    room_id = str(room_id)
    dash_length = (45/2)-2-(len(room_data[room_id]['name'])/2)
    
    clear_player_screen(conn)
    for i in range(0,dash_length):
        conn.sendall('-')
    conn.sendall(' '+room_data[room_id]['name']+' ')
    for i in range(0,dash_length):
        conn.sendall('-')
    conn.sendall('\n')
    conn.sendall(room_data[room_id]['desc'].replace('\\n','\n')+'\n')
    conn.sendall('---------------------------------------------\n')
    conn.sendall(user+' | Health ('+str(player_data[user]['health'])+'/'+str(player_data[user]['max_health'])+') | Mana ('+str(player_data[user]['mana'])+'/'+str(player_data[user]['max_mana'])+')\n')
    conn.sendall('---------------------------------------------\n')

    if len(player_data[user]['messages']) > 1:
        conn.sendall(str(len(player_data[user]['messages']))+' new messages\n')
    elif len(player_data[user]['messages']) == 1:
        conn.sendall('1 new message\n')
    else:
        conn.sendall('No new messages\n')
    conn.sendall('---------------------------------------------\n')
#
#
#
#
#
#Send Help Function
def send_help(conn):
    clear_player_screen(conn)
    conn.sendall('''
-------------------- Help Menu ---------------------
Go - Travel north, south, east, or west, as long as
     the room has paths there.

Inventory - View and edit your inventory

Help - Display this menu

Exit - Log out of the game

Refresh - Refresh the menu

Stats - View your stats

Messages - View your received messages

Send Message - Send a message to another player
----------------------------------------------------
Press <RETURN> to exit this menu
''')
    receive(conn)
    clear_player_screen(conn)
    return
#
#
#
#
#
#View Item Function
def view_item(conn,item):
    global item_data
    item = str(item)
    
    clear_player_screen(conn)
    conn.sendall('------------ '+item_data[item]['name']+' ------------\n')
    conn.sendall('Type: '+item_data[item]['type']+'\n')
    conn.sendall('Attack: '+str(item_data[item]['attack'])+'\n')
    conn.sendall('Defense: '+str(item_data[item]['defense'])+'\n')
    conn.sendall('Health: '+str(item_data[item]['health'])+'\n')
    conn.sendall('Mana: '+str(item_data[item]['mana'])+'\n')
    conn.sendall('------------ Description ------------\n')
    conn.sendall(item_data[item]['desc'].replace('\\n','\n')+'\n')
    conn.sendall('-------------------------------------\n')
    conn.sendall('Press <RETURN> to exit')
    receive(conn)
    clear_player_screen(conn)
    return
#
#
#
#
#
#Send Inventory Function
def send_inventory(conn,user):
    global player_data
    global item_data
    inventory_message = 'Type "help" for help\n'

    while True:
        inventory = {}
        for i in range(0,len(player_data[user]['inventory'])):
            item = str(player_data[user]['inventory'][i])
            if not item in inventory:
                inventory[item] = {
                    'name':item_data[item]['name'],
                    'qty':str(in_list(player_data[user]['inventory'],int(item)))
                    }
        clear_player_screen(conn)

        conn.sendall('------------ Inventory ------------\n')
        if len(inventory) == 0:
            conn.sendall('You don\'t have any items\n')
        for i in range(0,len(inventory)):
            item = str(player_data[user]['inventory'][i])
            conn.sendall(item+' | '+inventory[item]['name']+' (x'+inventory[item]['qty']+') ['+item_data[item]['type'][:1]+']\n')
        conn.sendall('-----------------------------------\n')
        conn.sendall(inventory_message)
        conn.sendall('-----------------------------------\n')
        conn.sendall('>')

        command = string.lower(receive(conn))

        if command == 'exit' or command == '':
            return True

        if command[:5] == 'drop ':
            item = int(command[5:])

            if item == 1 or item == 2:
                inventory_message = 'Think of the poor admins...\n'
            else:
                player_data[user]['inventory'].remove(item)
                save_player(user)
                inventory_message = 'Dropped the '+item_data[str(item)]['name']+'\n'

        if command[:13] == 'equip weapon ':
            item = str(command[13:])
            if item_data[item]['type'] == 'Weapon':
                if int(item) in player_data[user]['inventory']:
                    if player_data[user]['class'] in item_data[item]['class']:
                        if player_data[user]['level'] >= item_data[item]['level']:
                            player_data[user]['strength'] = player_data[user]['strength']-item_data[str(player_data[user]['equipped_weapon'])]['attack']
                            player_data[user]['strength'] = player_data[user]['strength']+item_data[item]['attack']
                            player_data[user]['equipped_weapon'] = item
                            save_player(user)
                            inventory_message = 'Equipped the '+item_data[item]['name']+'\n'
                        else:
                            inventory_message = 'You need to be at least level '+str(item_data[item]['level'])+' to use this\n'
                    else:
                        inventory_message = 'A '+player_class[user]['class']+' can\'t use this\n'
                else:
                    inventory_message = 'You don\'t own a '+item_data[item]['name']+'\n'
            else:
                inventory_message = 'No Patrick, a '+item_data[item]['name']+' is not a weapon\n'

        if command == 'unequip weapon':
            item = str(player_data[user]['equipped_weapon'])
            player_data[user]['strength'] = player_data[user]['strength']-item_data[str(player_data[user]['equipped_weapon'])]['attack']
            player_data[user]['equipped_weapon'] = 0
            save_player(user)
            inventory_message = 'Unequipped the '+item_data[item]['name']+'\n'

        if command[:13] == 'equip shield ':
            item = str(command[13:])
            if item_data[item]['type'] == 'Shield':
                if int(item) in player_data[user]['inventory']:
                    if player_data[user]['class'] in item_data[item]['class']:
                        if player_data[user]['level'] >= item_data[item]['level']:
                            player_data[user]['defense'] = player_data[user]['defense']-item_data[str(player_data[user]['equipped_shield'])]['defense']
                            player_data[user]['defense'] = player_data[user]['defense']+item_data[item]['defense']
                            player_data[user]['equipped_shield'] = item
                            save_player(user)
                            inventory_message = 'Equipped the '+item_data[item]['name']+'\n'
                        else:
                            inventory_message = 'You need to be at least level '+str(item_data[item]['level'])+' to use this\n'
                    else:
                        inventory_message = 'A '+player_class[user]['class']+' can\'t use this\n'
                else:
                    inventory_message = 'You don\'t own a '+item_data[item]['name']+'\n'
            else:
                inventory_message = 'No patrick, a '+item_data[item]['name']+' is not a shield\n'

        if command == 'unequip shield':
            item = str(player_data[user]['equipped_shield'])
            player_data[user]['defense'] = player_data[user]['defense']-item_data[str(player_data[user]['equipped_shield'])]['defense']
            player_data[user]['equipped_shield'] = 0
            save_player(user)
            inventory_message = 'Unequipped the '+item_data[item]['name']+'\n'

        if command[:4] == 'use ':
            item = str(command[4:])
            if item_data[item]['type'] == 'Item':
                if int(item) in player_data[user]['inventory']:
                    player_data[user]['health'] = player_data[user]['health']+item_data[item]['health']
                    if player_data[user]['health'] > player_data[user]['max_health']:
                        player_data[user]['health'] = player_data[user]['max_health']
                    player_data[user]['mana'] = player_data[user]['mana']+item_data[item]['mana']
                    if player_data[user]['mana'] > player_data[user]['max_mana']:
                        player_data[user]['mana'] = player_data[user]['max_mana']
                    save_player(user)
                    inventory_message = 'Used the '+item_data[item]['name']+'\n'
                else:
                    inventory_message = 'You don\'t have a '+item_data[item]['name']+'\n'
            else:
                inventory_message = 'You can\'t "use" a '+item[item]['type']+'\n'

        if command[:5] == 'view ':
            item = str(command[5:])
            if int(item) in player_data[user]['inventory']:
                if str(item) in item_data:
                    view_item(conn,item)
                else:
                    inventory_message = 'This item does not exist\n'
            else:
                inventory_message = 'You don\'t have this item\n'

        if command[:5] == 'give ':
            item = command[5:]
            if int(item) in player_data[user]['inventory']:
                if str(item) in item_data:
                    conn.sendall('Give the '+item_data[item]['name']+' to which player?\nPlayer name >')
                    target_player = receive(conn)
                    if target_player in player_data:
                        player_data[user]['inventory'].remove(int(item))
                        player_data[target_player]['inventory'].append(int(item))
                        inventory_message = 'Gave the '+item_data[item]['name']+' to '+target_player+'\n'
                    else:
                        inventory_message = target_player+' is not a registered username\n'
                else:
                    inventory_message = 'This item does not exist\n'
            else:
                inventory_message = 'You don\'t have this item\n'
#
#
#
#
#
#Send Stats Function
def send_stats(conn,user):
    clear_player_screen(conn)
    conn.sendall('------------ Info ------------\n')
    conn.sendall('Name: '+user+'\n')
    conn.sendall('Health: ('+str(player_data[user]['health'])+'/'+str(player_data[user]['max_health'])+')\n')
    conn.sendall('Mana: ('+str(player_data[user]['mana'])+'/'+str(player_data[user]['max_mana'])+')\n')
    conn.sendall('\n')
    conn.sendall('Strength: '+str(player_data[user]['strength'])+'\n')
    conn.sendall('Agility: '+str(player_data[user]['agility'])+'\n')
    conn.sendall('Defense: '+str(player_data[user]['defense'])+'\n')
    conn.sendall('------------------------------\n')
    conn.sendall('Press <RETURN> to exit')
    receive(conn)
    clear_player_screen(conn)
#
#
#
#
#
#Generate Enemy Function
def generate_enemy(min_level,max_level,player_level):
    global player_data
    global enemy_data
    global enemy_index
    candidates = []

    for i in range(0,len(enemy_index)-1):
        enemy = enemy_data[enemy_index[i]]
        if enemy['level'] <= player_level+3 and enemy['level'] >= player_level-3:
            candidates.append(enemy['name'])
    for i in range(0,len(candidates)-1):
        enemy = enemy_data[candidates[i]]
        if enemy['level'] > max_level or enemy['level'] < min_level:
            candidates.remove(enemy['name'])

    if len(candidates) == 0:
        return None
    num = randint(0,len(candidates)-1)
    return candidates[num]
#
#
#
#
#
#Generate Player Attack Function
def generate_player_attack(player,enemy):
    power = player['strength']-(enemy['attack']/2)-randint(0,2)
    if power <= 0:
        power = randint(0,3)
    return power
#
#
#
#
#
#Generate Enemy Attack Function
def generate_enemy_attack(player,enemy):
    power = enemy['attack']-(player['defense']/2)
    if power <= 0:
        power = randint(0,3)
    return power
#
#
#
#
#
#Drop Item Function
def drop_item():
    return
#
#
#
#
#
#Start Battle Function
def start_battle(user,room,conn):
    global room_data
    global player_data
    global enemy_data
    global item_data
    room = str(room)
    player_moved = False
    min_enemy = room_data[room]['min_enemy']
    max_enemy = room_data[room]['max_enemy']
    player_level = int(player_data[user]['level'])
    enemy_id = None
    try:
        enemy_id = generate_enemy(min_enemy,max_enemy,player_level)
        enemy = deepcopy(enemy_data[enemy_id])
    except Exception,e:
        print 'Battle init for '+user+' with CAND '+str(enemy_id)+' failed - '+str(e)
        return
    else:
        print 'Battle init for '+user+' with CAND '+enemy['name']+' - Currently in progress'
    battle_message = 'You are attacked by a '+enemy['name']+'!'
    clear_player_screen(conn)

    if int(player_data[user]['equipped_weapon']) == 0:
        conn.sendall('You have no weapons equipped, and are quickly\nslaughtered by the '+enemy['name']+'.\n')
        conn.sendall('Press <RETURN> to revive in the main hallway')
        receive(conn)
        return False

    while True:
        clear_player_screen(conn)
        conn.sendall('---------------------------------------------\n')
        conn.sendall(enemy['name']+' | '+str(enemy['health'])+'\n')
        conn.sendall('---------------------------------------------\n')
        conn.sendall('\n'+battle_message+'\n')
        conn.sendall('---------------------------------------------\n')
        conn.sendall(user+' | ('+str(player_data[user]['health'])+'/'+str(player_data[user]['max_health'])+') | ('+str(player_data[user]['mana'])+'/'+str(player_data[user]['max_mana'])+')\n')
        conn.sendall('---------------------------------------------\n')
        conn.sendall('Command >')
        command = str(receive(conn))

        if command == 'attack':
            power = generate_player_attack(player_data[user],enemy)
            enemy['health'] = enemy['health']-power
            clear_player_screen(conn)
            conn.sendall('\n'+item_data[str(player_data[user]['equipped_weapon'])]['phrase']+'\n')
            time.sleep(0.5)
            conn.sendall('It did '+str(power)+' damage to the '+enemy['name']+'!\n')
            time.sleep(1)
            if enemy['health'] < 0:
                enemy['health'] = 0
            player_moved = True

        if command == 'run':
            escape_chance = randint(player_data[user]['agility'],50)
            if escape_chance == 50:
                conn.sendall('Escaped the fight!\n')
                conn.sendall('Press <RETURN> to exit')
                return True
            else:
                conn.sendall('You were unable to escape!\n')
                time.sleep(1)
                player_moved = True

        if enemy['health'] == 0:
            gold_gained = (enemy['level']*2)*10
            conn.sendall('You defeated the '+enemy['name']+'!\n')
            conn.sendall('You received '+str(gold_gained)+' gold!\n')
            conn.sendall('\nPress <RETURN> to exit')
            for i in range(0,gold_gained):
                player_data[user]['inventory'].append(3)
            receive(conn)
            save_player(user)
            clear_player_screen(conn)
            return True

        if player_moved:
            power = generate_enemy_attack(player_data[user],enemy)
            player_data[user]['health'] = player_data[user]['health']-power
            battle_message = enemy['attack_phrases'][randint(0,len(enemy['attack_phrases'])-1)]+'\nIt does '+str(power)+' damage!'
            if player_data[user]['health'] <= 0:
                conn.sendall('\nYou were slain by the '+enemy['name']+'!\n')
                conn.sendall('Press <RETURN> to revive in the main hall')
                receive(conn)
                return False
#
#
#
#
#
#Send Message Function
def send_message(conn,user):
    global player_data
    message_full = {
        'to':'',
        'from':'',
        'subject':'',
        'message':''
        }
    
    clear_player_screen(conn)
    conn.sendall('------------ Message ------------\n')
    conn.sendall('From: '+user+'\n')
    message_full['from'] = user
    conn.sendall('To: ')
    message_full['to'] = receive(conn)
    
    if not message_full['to'] in player_data:
        conn.sendall('This player does not exist\n')
        time.sleep(1)
        clear_player_screen(conn)
        return
    conn.sendall('Subject: ')
    message_full['subject'] = receive(conn)
    conn.sendall('---------------------------------\n')
    conn.sendall('Please type your message below. When\n')
    conn.sendall('you are done, send a blank line.\n')
    conn.sendall('---------------------------------\n')

    while True:
        message = receive(conn)
        if message == '':
            break
        message_full['message'] = message_full['message']+message+'\n'
    conn.sendall('---------------------------------\n')
    player_data[message_full['to']]['messages'].append(message_full)
    save_player(message_full['to'])
    conn.sendall('Thank you, your message has been delivered\n')
    time.sleep(1)
    clear_player_screen(conn)
    return
#
#
#
#
#
#View Message Function
def view_message(conn,user,message_id):
    global player_data
    
    clear_player_screen(conn)
    conn.sendall('------------------------------------\n')
    conn.sendall('From: '+player_data[user]['messages'][message_id]['from']+'\n')
    conn.sendall('Subject: '+player_data[user]['messages'][message_id]['subject']+'\n')
    conn.sendall('------------------------------------\n')
    conn.sendall(player_data[user]['messages'][message_id]['message'])
    conn.sendall('------------------------------------\n')
    conn.sendall('Press <RETURN> to exit')
    receive(conn)
#
#
#
#
#
#View Messages Function
def list_messages(conn,user):
    global player_data
    messages_help = '''
--------------------------------------------
View <message ID> - View a messages contents

Delete <messaage ID> - Delete a message

Exit - Exit the messages menu

Help - Display this menu
--------------------------------------------
'''
    
    interface_message = 'Type "exit" to quit this menu\n'

    while True:
        clear_player_screen(conn)
        conn.sendall('------------ '+user+'\'s Messages ------------\n')
        if len(player_data[user]['messages']) > 0:
            for i in range(0,len(player_data[user]['messages'])):
                conn.sendall(str(i)+' | '+player_data[user]['messages'][i]['from']+' | '+player_data[user]['messages'][i]['subject']+'\n')
        else:
            conn.sendall('No new messages\n')
        conn.sendall('--------------------------------------------------\n')
        conn.sendall(interface_message)
        conn.sendall('--------------------------------------------------\n')
        conn.sendall('>')
        command = receive(conn)

        if command == 'exit':
            clear_player_screen(conn)
            return

        if command[:5] == 'view ':
            try:
                view_message(conn,user,int(command[5:]))
            except:
                interface_message = 'No message with ID '+command[5:]+'\n'
            else:
                interface_message = 'Type "exit" to quit this menu\n'

        if command[:7] == 'delete ':
            message_id = int(command[7:])
            try:
                player_data[user]['messages'][message_id] = 'REMOVE'
                player_data[user]['messages'].remove('REMOVE')
                save_player(user)
            except:
                interface_message = 'Failed to delete the message\n'
            else:
                interface_message = 'Deleted the message\n'

        if command == 'help':
            clear_player_screen(conn)
            conn.sendall(messages_help+'\n')
            conn.sendall('Press <RETURN> to exit')
            receive(conn)
def revive_player(user):
    player_data[user]['health'] = player_data[user]['max_health']
    player_data[user]['mana'] = player_data[user]['max_mana']
#
#
#
#
#
#Move Player Function
def move_player(conn,current,direction):
    global room_data
    current = str(current)
    direction = string.lower(direction)

    if direction == 'north':
        if room_data[current]['north'] == '1':
            return room_data[current]['north_id']
        else:
            return current
    elif direction == 'south':
        if room_data[current]['south'] == '1':
            return room_data[current]['south_id']
        else:
            return current
    elif direction == 'east':
        if room_data[current]['east'] == '1':
            return room_data[current]['east_id']
        else:
            return current
    elif direction == 'west':
        if room_data[current]['west'] == '1':
            return room_data[current]['west_id']
        else:
            return current
    else:
        return current
#
#
#
#
#
#Player Handling Function
def player_handler(conn,addr):
    global name
    global version
    global kicklist
    global banlist
    current_room = str(0)
    username = str()
    status = 0

    clear_player_screen(conn)
    conn.sendall(name+' Server v'+version+'\n')
    conn.sendall('------------------------------------\n')
    username = player_login(conn,addr)

    if username in banlist:
        conn.sendall('You are currently banned from this server\n')
        conn.sendall('If you believe this to be a mistake, feel\n')
        conn.sendall('free to email martianmellow12@gmail.com\n')
        conn.close()
    
    send_room(conn,0,username)

    while True:
        conn.sendall('Command >')
        command = string.lower(receive(conn))

        if username in kicklist:
            kicklist.remove(username)
            conn.sendall('\n You have been kicked from the server\n')
            conn.sendall('You may rejoin, but please try to be respectful\n')
            conn.sendall('to other players.\n')
            conn.close()

        if command == 'help':
            send_help(conn)
            send_room(conn,current_room,username)

        if command == 'exit' or command == 'quit':
            clear_player_screen(conn)
            conn.sendall('Farewell, '+username+'...')
            time.sleep(2)
            clear_player_screen(conn)
            conn.close()
            break

        if command[:3] == 'go ':
            direction = command[3:]
            current_room = move_player(conn,current_room, direction)
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command == 'inventory':
            send_inventory(conn,username)
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command == 'stats':
            send_stats(conn,username)
            send_room(conn,current_room,username)

        if command == 'send message':
            send_message(conn,username)
            send_room(conn,current_room,username)

        if command == 'messages' or command == 'view messages':
            list_messages(conn,username)
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command == 'refresh':
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command == 'fight':
            clear_player_screen(conn)
            sucess = start_battle(username,current_room,conn)
            if not sucess:
                current_room = 0
                revive_player(username)
                print 'Battle with '+username+' ended - WIN'
            else:
                print 'Battle with '+username+' ended - LOSS'
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command[:8] == 'elevate:' and command[8:] == 'yeetothemax':
            status = 2
            print 'User '+username+' was elevated to level 2'
            conn.sendall('You were elevated to level 2\nPress <RETURN> to accept')
            receive(conn)
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command[:5] == 'kick ':
            player = command[5:]
            kicklist.append(player)
            print username+' kicked '+player+' from the server'
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command[:7] == 'addban:':
            player = command[7:]
            banlist.append(player)
            print username+' banned '+player+' from the server'
            clear_player_screen(conn)
            send_room(conn,current_room,username)

        if command[:10] == 'removeban:':
            player = command[10:]
            banlist.remove(player)
            print username+' unbanned '+player+' from the server'
            clear_player_screen(conn)
            send_room(conn,current_room,username)
#
#
#
#
#
#Setup
print name+' Server Framework v'+version
print 'Written By MM12 And ObsidiousD'
print ''
print '---------- Server Setup ----------'

print 'Checking file structure...'
#Check For Resources Folder
print 'Resources Folder',
if os.path.isdir(resource_dir):
    print '[ OK ]'
else:
    print '[FAIL]'
    print 'Creating Resources folder...',
    try:
        os.mkdir(resource_dir)
    except:
        print '[FAIL]'
        sys.exit(0)
        print 'ERROR: Server setup has failed'
    else:
        print '[ OK ]'
#Check For Room Folder
print 'Room Data Folder',
if os.path.isdir(room_dir):
    print '[ OK ]'
else:
    print '[FAIL]'
    print 'Creating Room Data folder...',
    try:
        os.mkdir(room_dir)
    except:
        print '[FAIL]'
        sys.exit(0)
        print 'ERROR: Server setup has failed'
    else:
        print '[ OK ]'
#Check For Player Folder
print 'Player Data Folder',
if os.path.isdir(player_dir):
    print '[ OK ]'
else:
    print '[FAIL]'
    print 'Creating Player Data folder...',
    try:
        os.mkdir(player_dir)
    except:
        print '[FAIL]'
        sys.exit(0)
        print 'ERROR: Server setup has failed'
    else:
        print '[ OK ]'
#Check For Enemy Data
print 'Enemy Data Folder',
if os.path.isdir(enemy_dir):
    print '[ OK ]'
else:
    print '[FAIL]'
    print 'Creating Enemy Data folder...',
    try:
        os.mkdir(enemy_dir)
    except:
        print '[FAIL]'
        sys.exit(0)
        print 'ERROR: Server setup has failed'
    else:
        print '[ OK ]'
#Check For Item Data
print 'Item Data',
if os.path.isdir(item_dir):
    print ' [ OK ]'
else:
    print ' [FAIL]'
    print 'Creating item data folder...',
    try:
        os.mkdir(item_dir)
    except:
        print ' [FAIL]'
        sys.exit(0)
    print ' [ OK ]'
#Load Player Data
print 'Loading player data...'
players = os.listdir(player_dir)
print 'Preparing to load '+str(len(players))+' players...'
time.sleep(2)
for i in range(0,len(players)):
    if not '.' in players[i]:
        success = load_player(players[i])
        if success:
            print players[i]+' [ OK ]'
        else:
            print players[i]+' [FAIL]'
#Load Room Data
print 'Loading room data'
rooms = os.listdir(room_dir)
print 'Preparing to load '+str(len(rooms))+' rooms...'
time.sleep(2)
if not rooms[i][:1] == '.':
    for i in range(0,len(rooms)):
        success = load_room(i)
        if success:
            print 'ID '+str(i)+' [ OK ]'
        else:
            print 'ID '+str(i)+' [FAIL]'
#Load Items
print 'Loading item data'
files = os.listdir(item_dir)
for i in range(0,len(files)):
    if not files[i][:1] == '.':
        try:
            filein = open(item_dir+str(files[i]),'r')
            item_data[str(files[i])] = json.loads(filein.read())
            filein.close()
        except:
            print 'ID '+str(files[i])+' [FAIL]'
        else:
            print 'ID '+str(files[i])+' [ OK ]'
#Load Enemies
print 'Loading enemies'
enemies = os.listdir(enemy_dir)
for i in range(0,len(enemies)):
    if not enemies[i][:1] == '.':
        try:
            filein = open(enemy_dir+enemies[i])
            enemy_data[str(enemies[i])] = json.loads(filein.read())
            filein.close()
        except:
            print enemies[i]+' [FAIL]'
        else:
            print enemies[i]+' [ OK ]'
            enemy_index.append(enemies[i])
#
#
#
#
#
#Server Setup
print 'Setting up the socket',
try:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
except:
    print ' [FAIL]'
    sys.exit(0)
else:
    print ' [ OK ]'

print 'Binding the socket to host port 8080'
try:
    s.bind((host,port))
except:
    print ' [FAIL]'
    sys.exit(0)
else:
    print ' [ OK ]'

try:
    s.listen(5)
except Exception,e:
    print 'Failed to put the server into listening mode'
    print str(e)
    sys.exit(0)

print 'The server will now listen for new connections'
print ''
print 'System Log'
print '-----------------------------------------------'
#
#
#
#
#
#Main Listen Loop
while True:
    conn,addr = s.accept()

    print 'New connection: '+str(addr)+' - Pushing to player handler'
    thread.start_new_thread(player_handler,(conn,addr))
