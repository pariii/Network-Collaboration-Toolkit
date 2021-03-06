import socket
import threading
import time
import logging

HOST = ''
PORT = 12000
TIMEOUT = 5
BUF_SIZE = 1024

class WhatsUpServer(threading.Thread):
    global clients
    global messages
    global accounts
    global onlines
    global groups
    global group_name


    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.ip = self.addr[0]
        self.name = ''
        self.flag = 0
        self.log = 0

    def print_indicator(self, prompt):
        print 56
        self.conn.send('%s' % (prompt,))
        print 57

    def login(self):
        global ip_names
        logging.info('Connected from: %s:%s' %(self.addr[0], self.addr[1]))
        #msg = '\n## Welcome to WhatsUp\n## Enter `!q` to quit\n'

        # new user
        print accounts
        if self.ip not in accounts:
            #msg += '## Please enter your name:'
            #self.print_indicator(msg)
            self.print_indicator(self.log)
            accounts[self.ip] = {
                'name': '',
                'pass': '',
                'lastlogin': time.ctime()
            }

            while 1:
                name = self.conn.recv(BUF_SIZE).strip()
                if name in messages:
                    self.print_indicator(
                        'Username already exists, please try another!')
                else:
                    break
            accounts[self.ip]['name'] = name
            self.name = name
            logging.info('%s logged as %s' % (self.addr[0], self.name))
            messages[name] = []
            self.print_indicator('Username verified!')
            password = self.conn.recv(BUF_SIZE)
            accounts[self.ip]['pass'] = password.strip()
            self.flag=1
            self.log = 1
            print self.log
            self.print_indicator('##')
            clients.add((self.conn, self.addr,self.flag))
        else:
            self.name = accounts[self.ip]['name']
            print self.log
            n = self.name
            #msg += '## Hello %s, please enter your password:' % (self.name,)
            # print accounts
            #self.print_indicator('Purana User, Enter your password!')
            self.print_indicator(n)
            while 1:
                password = self.conn.recv(BUF_SIZE).strip()
                if password != accounts[self.ip]['pass']:
                    self.print_indicator('Incorrect password, please enter again')
                else:
                    self.print_indicator('Welcome back, last login: %s' %(accounts[self.ip]['lastlogin'],))
                    accounts[self.ip]['lastlogin'] = time.ctime()
                    break
            #self.conn.send(self.show_mentions(self.name))
        ip_names += self.ip+"::"+self.name+"$"
        print ip_names
        self.broadcast_online_users('`%s` is online now' % (ip_names,), clients, False)
        onlines[self.name] = self.conn

    def logoff(self):
        self.conn.send('## Bye!\n')
        print online
        msg=self.name+" is offline now!"
        print msg
#        del onlines[self.name]
        clients.remove((self.conn, self.addr, self.flag))
        #self.broadcast('## `%s` is offline now' %(self.name,), clients)
        for conn, addr, flag in clients:
            conn.send(msg)
        #self.broadcast(msg, clients,False)
        self.conn.close()
        exit()

    def check_keyword(self, buf):
        global onlines
        if buf.find('!q') == 0:
            self.logoff()
        print 11

        if buf.find('#') == 0:
            print 12
            group_keyword = buf.split(' ')[0][1:]
            print group_keyword
            print 13
            group_component = group_keyword.split(':')
            print group_component

            # to post in a group
            if len(group_component) == 1:
                print 14
                group_name = group_component[0] #ankit 
                try:
                    msg = '[%s]%s: %s' % (
                        group_name, self.name, buf.split(' ', 1)[1])
                    print 22
                    print msg
                    self.group_post(group_name, msg)
                except IndexError:
                    self.print_indicator('## What do you want to do with `#%s`?' % (group_name))

            # to join / leave a group
            elif len(group_component) == 2: #joining
                print 16
                group_name = group_component[0] #group_name=ankit
                if group_component[1] == 'join':
                    print 33
                    self.group_join(group_name) #function called group_join to add member
                elif group_component[1] == 'leave':
                    self.group_leave(group_name)
            return True

        if buf.find('@') == 0:
            to_user = buf.split(' ')[0][1:]
            from_user = self.name
            msg = buf.split(' ', 1)[1]

            # if user is online
            if to_user in onlines:
                onlines[to_user].send('@%s: %s\n>> ' % (from_user, msg))
                self.mention(from_user, to_user, msg, 1)
            # offline
            else:
                self.mention(from_user, to_user, msg)
            return True

    def group_post(self, group_name, msg):
        # if the group does not exist, create it
        groups.setdefault(group_name, set())

        # if current user is a member of the group
        if (self.conn, self.addr,self.flag) in groups[group_name]:
            print groups[group_name]
            self.broadcast(msg, groups[group_name])
        else:
            self.print_indicator(
                '## You are currently not a member of group `%s`' % (group_name,))

    def group_join(self, group_name):
        groups.setdefault(group_name, set())
        groups[group_name].add((self.conn, self.addr,self.flag))
        print 44
        #self.print_indicator('## You have joined the group `%s`' %(group_name,))
        print 55

    def group_leave(self, group_name):
        try:
            groups[group_name].remove((self.conn, self.addr,self.flag))
            self.print_indicator('## You have left the group `%s`' %
                                 (group_name,))
        except Exception, e:
            pass

    def mention(self, from_user, to_user, msg, read=0):
        if to_user in messages:
            messages[to_user].append([from_user, msg, read])
            self.print_indicator('## Message has sent to %s' % (to_user,))
        else:
            self.print_indicator('## No such user named `%s`' % (to_user,))

    def show_mentions(self, name):
        res = '## Here are your messages:\n'
        if not messages[name]:
            res += '   No messages available\n>> '
            return res
        for msg in messages[name]:
            if msg[2] == 0:
                res += '(NEW) %s: %s\n' % (msg[0], msg[1])
                msg[2] = 1
            else:
                res += '      %s: %s\n' % (msg[0], msg[1])
        res += '>> '
        return res

    def broadcast_online_users(self, msg, receivers, to_self=True):
        for conn, addr, flag in receivers:
            conn.send(msg + '\n>> ')

    def broadcast(self, msg, receivers, to_self=True):
        for conn, addr, flag in receivers:
            # if the client is not the current user
            if addr[0] != self.ip and flag==1:
                conn.send(msg + '>> ')
            # if current user
            else:
                self.conn.send('>> ') if to_self else self.conn.send('')

    def run(self):
        self.login()

        while 1:
            try:
                self.conn.settimeout(TIMEOUT)
                buf = self.conn.recv(BUF_SIZE).strip()
                logging.info('%s@%s: %s' % (self.name, self.addr[0], buf))
                # check features
                if not self.check_keyword(buf):
                    # client broadcasts message to all
                    self.broadcast('%s: %s' % (self.name, buf), clients)

            except Exception, e:
                # timed out
                pass

def main():
    global clients
    global messages
    global accounts
    global onlines
    global groups
    global ip_names

    # logging setup
    logging.basicConfig(level=logging.INFO,
                        format='[%(asctime)s] %(levelname)s: %(message)s',
                        datefmt='%d/%m/%Y %I:%M:%S %p')

    # initialize global vars
    clients = set()
    messages = {}
    accounts = {}
    onlines = {}
    groups = {}
    ip_names=""

    # set up socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((HOST, PORT))
    sock.listen(5)
    print '-= WhatsUp Server =-'
    print '>> Listening on:', PORT
    print '>> Author: Xin Wang'
    print ''

    while 1:
        try:
            conn, addr = sock.accept()
            server = WhatsUpServer(conn, addr)
            server.start()
        except Exception, e:
            print e

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print 'Quited'