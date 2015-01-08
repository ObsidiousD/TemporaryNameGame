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

name = 'Game Thing'
version = '0.1'
local_dir = os.getcwd()+'/'
resource_dir = local_dir+'Resources/'
player_dir = local_dir+'Resources/player_data/'
room_dir = local_dir+'Resources/room_data/'
enemy_dir = local_dir+'Resources/enemy_data/'

host = ''
port = 8080
newline = [chr(13)+chr(10),chr(13),chr(10)]

player_data = {}
player_passwords = {}
room_data = {}
enemy_data = {}
item_data = {}

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
        'bosses_killed':0
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
    current_room = str(0)
    username = str()

    clear_player_screen(conn)
    conn.sendall(name+' Server v'+version+'\n')
    conn.sendall('------------------------------------\n')
    username = player_login(conn,addr)
    send_room(conn,0,username)

    while True:
        conn.sendall('Command >')
        command = string.lower(receive(conn))

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
if os.path.isfile(resource_dir+'item_list.dat'):
    print ' [ OK ]'
else:
    print ' [FAIL]'
    print 'Creating item list...',
    try:
        fileout = open(resource_dir+'item_list.dat','w')
        fileout.close()
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
for i in range(0,len(rooms)):
    success = load_room(i)
    if success:
        print 'ID '+str(i)+' [ OK ]'
    else:
        print 'ID '+str(i)+' [FAIL]'
#
#
#
#
#
#Server Setup
print 'Setting up the socket',
try:
    s = socket.socket()
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
