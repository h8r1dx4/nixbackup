#!/usr/bin/python3
import sys
import os
import datetime

precode = './precode'
postcode = './postcode'
directory = './directory'
date = datetime.datetime.now()
fdate = date.strftime('%d-%m-%Y')
backupdir = ' /tmp/backups/workdir/'
serverip = './serverip'

def runcode(file):
    with open(file) as f:
        for line in f:
            os.system(line)

def copyfile(dir):
    os.system('mkdir /tmp/backups/')
    os.system('mkdir' + backupdir)
    with open(dir) as f:
        for line in f:
            os.system('cp -R ' + line + backupdir)

def compress(dir):
    os.system('tar -zcvf /tmp/backups/backup-' + fdate + '.tar.gz' + dir)

def remotecopy(ip):
    with open(ip) as f:
        for line in f:
            os.system('scp /tmp/backups/backup-' + fdate + '.tar.gz' ' root@' + line + ':/var/backups/')

def removefiles(dir):
    os.system('rm -Rf ' + dir)

def addtofile(file, userdata):
    x = open(file, "a")
    if os.stat(file).st_size == 0:
        x.write(userdata)
        x.close()
    else:
        x.write('\n')
        x.write(userdata)
        x.close()

def clearfile(file):
        x = open(file, "w+")
        x.truncate()
        x.close()

def menu():
    active = 1
    while active ==1:
        usr = input('''NixBackup
        1. Add Server address
        2. Clear Server list
        3. Add directory
        4. Clear directory list
        5. Run backup
        q. Quit
        ''')
        if usr == '1':
            userdata = input('Please provide server ip to apend to list:')
            addtofile(serverip, userdata)
        elif usr == '2':
            clearfile(serverip)
        elif  usr == '3':
            userdata = input('Please provide directory for backup:')
            addtofile(directory, userdata)
        elif usr == '4':
            clearfile(directory)
        elif usr == '5':
            runcode(precode)
            copyfile(directory)
            runcode(postcode)
            compress(backupdir)
            remotecopy(serverip)
            removefiles('/tmp/backups/')


if len(sys.argv) > 1:
    if sys.argv[1] == '-m':
        menu()
    elif sys.argv[1] == '-b':
        runcode(precode)
        copyfile(directory)
        runcode(postcode)
        compress(backupdir)
        remotecopy(serverip)
        removefiles('/tmp/backups/')
    elif sys.argv[1] == '-h':
        print('-m for Menu')
        print('-b for background')
    else:
        print('-h for Help')
else:
    print('-h for Help')

