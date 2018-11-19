import socket
import sys
import os
import termios
import tty
import fcntl
import signal
import struct
import select
now_channel = None


def interactive_shell(chan):
    posix_shell(chan)


def ioctl_GWINSZ(fd):
    try:
        cr = struct.unpack('hh', fcntl.ioctl(fd, termios.TIOCGWINSZ, 'aaaa'))
    except:
        return
    return cr


def getTerminalSize():
    cr = ioctl_GWINSZ(0) or ioctl_GWINSZ(1) or ioctl_GWINSZ(2)
    return int(cr[1]), int(cr[0])


def resize_pty(signum=0, frame=0):
    width, height = getTerminalSize()
    if now_channel is not None:
        now_channel.resize_pty(width=width, height=height)


def posix_shell(chan):
    global now_channel
    now_channel = chan
    resize_pty()
    signal.signal(signal.SIGWINCH, resize_pty) 
    stdin = os.fdopen(sys.stdin.fileno(), 'r', 0)
    fd = stdin.fileno()
    oldtty = termios.tcgetattr(fd)
    newtty = termios.tcgetattr(fd)
    newtty[3] = newtty[3] | termios.ICANON
    try:
        termios.tcsetattr(fd, termios.TCSANOW, newtty)
        tty.setraw(fd)
        tty.setcbreak(fd)
        chan.settimeout(0.0)
        while True:
            try:
                r, w, e = select.select([chan, stdin], [], [])
            except:
                continue
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print 'rn*** EOFrn',
                        break
                    sys.stdout.write(x)
                    sys.stdout.flush()
                except socket.timeout:
                    pass
            if stdin in r:
                x = stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)
