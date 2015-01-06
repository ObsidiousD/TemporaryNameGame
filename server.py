#Server Framework
#
#Written By MartianMellow12 (MM12) And ObsidiousD
import threading
import socket
import os
import time
import json

name = 'Game Thing'
version = '0.1'
local_dir = os.getcwd()+'/'
resource_dir = local_dir+'Resources/'
player_dir = local_dir+'Resources/player_data/'
room_dir = local_dir+'Resources/room_data/'
enemy_dir = local_dir+'Resources/enemy_data/'

player_data = {}
room_data = {}
enemy_data = {}
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
        player_data[player_name] = filein.read()
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
def create_player(player_name,player_class):
    global player_dir
    global player_data

    if os.path.isdir(player_dir+player_name):
        return 2 #Code for a name that's already taken
    
    try:
        os.mkdir(player_dir+player_name)
        fileout = open(player_dir+player_name+'/info.dat','w')
    except:
        return 0 #Code for failure

    info = {
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
#Load Player Data
print 'Loading player data...'
players = os.listdir(player_dir)
print 'Preparing to load '+str(len(players))+' players...'
time.sleep(2)
for i in range(0,len(players)):
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
for i in range(1,len(rooms)):
    success = load_room(i)
    if success:
        print 'ID '+str(i)+' [ OK ]'
    else:
        print 'ID '+str(i)+' [FAIL]'
