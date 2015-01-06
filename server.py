#Server Framework
#
#Written By MartianMellow12 (MM12) And ObsidiousD
import thread
import socket
import os

name = 'Game Thing'
version = '0.1'
local_dir = os.getcwd()+'/'
resource_dir = local_dir+'Resources/'
player_dir = local_dir+'Resources/player_data/'
room_dir = local_dir+'Resources/room_data/'

player_data = {}
room_data = {}
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
#Resources Folder
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
#Room Folder
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
#Player Folder
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

print 'Loading player data...'
filein = open(player_dir+'
