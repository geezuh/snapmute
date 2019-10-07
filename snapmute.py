#!/usr/bin/env python3
import asyncio
import snapcast.control
import curses
from curses import wrapper
#init curses stuff
stdscr=curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

def getserver():
    loop = asyncio.get_event_loop()
    server = loop.run_until_complete(snapcast.control.create_server(loop, 'nosuch'))
    return(server)

def mutetoggle(server,index):
    loop = asyncio.get_event_loop()
    client=server.clients[index]
    loop.run_until_complete(server.client_volume(client.identifier, {'muted': not client.muted}))

def main(stdscr):
    index=0
    while True:
        stdscr.clear()
        server=getserver()
        clients=server.clients
        names=[]
        y=0
        for client in clients:
            if y==index:
                at=curses.A_REVERSE
            elif client.muted:
                at=curses.A_DIM
            else:
                at=curses.A_BOLD
            stdscr.addstr(y+1,1,client.friendly_name,at)   
            y+=1
        key=stdscr.getkey()
        if key=="KEY_DOWN":
            index+=1
        elif key=="KEY_UP":
            index-=1
        elif key=="\n":
            mutetoggle(server,index)
        elif key=="q":
            break
        #stdscr.addstr(y+1,1,key)
        stdscr.refresh()
    return;

wrapper(main)

#end curses stuff 
curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()
