#!/usr/bin/python
import argparse

##########################################################################
##########################################################################

def fatal(msg):
    sys.stderr.write('FATAL: %s\n'%msg)
    sys.exit(1)

##########################################################################
##########################################################################

def index(x,y):
    assert x>=0 and x<160
    assert y>=0 and y<256
    return ((x>>1)<<3)+(y>>3)*640+(y&7)

def tap(x):
    v=0
    if (x&0x80)!=0: v|=0x08
    if (x&0x20)!=0: v|=0x04
    if (x&0x08)!=0: v|=0x02
    if (x&0x02)!=0: v|=0x01
    return v

def split(x):
    assert (x&~0xf)==0
    v=0
    if (x&0x08)!=0: v|=0x80
    if (x&0x04)!=0: v|=0x20
    if (x&0x02)!=0: v|=0x08
    if (x&0x01)!=0: v|=0x02
    return v

def getpixel(s,x,y):
    v=s[index(x,y)]
    if (x&1)==0: return tap(v)
    else: return tap(v<<1)

def putpixel(s,x,y,c):
    i=index(x,y)
    v=s[i]
    if (x&1)==0: s[i]=(s[i]&0x55)|split(c)
    else: s[i]=(s[i]&0xaa)|(split(c)>>1)
    
##########################################################################
##########################################################################

def find_smiley_pixels(s):
    flags=[]

    for y in range(256):
        lx=0
        while lx<160 and getpixel(s,lx,y)==0: lx+=1
        rx=160
        while rx>lx and getpixel(s,rx-1,y)==0: rx-=1

        row=[]

        x=0
        while x<lx:
            row.append(False)
            x+=1

        while x<rx:
            row.append(True)
            x+=1

        while x<160:
            row.append(False)
            x+=1

        flags.append(row)

    return flags

def save_pic(path,data):
    if path is not None:
        with open(path,'wb') as f: f.write("".join([chr(x) for x in data]))

def main(options):
    with open(options.input_path,'rb') as f: data=[ord(x) for x in f.read()]
    if len(data)!=20480: fatal('not 20K: %s'%options.input_path)

    # remove the bitshifters url
    for y in range(220,256):
        for x in range(0,160):
            putpixel(data,x,y,0)

    smiley=find_smiley_pixels(data)

    striped=data[:]
    for y in range(256):
        for x in range(160):
            if not smiley[y][x]: putpixel(striped,x,y,11 if (x&15)<8 else 12)
    save_pic(options.striped,striped)

    masked=data[:]
    for y in range(256):
        for x in range(160):
            if not smiley[y][x]: putpixel(masked,x,y,5)
    save_pic(options.masked,masked)

    dithered=data[:]
    for y in range(256):
        for x in range(160):
            if (not smiley[y][x] or
                ((x^y)&1)!=0):
                putpixel(dithered,x,y,5)
    save_pic(options.dithered,dithered)

##########################################################################
##########################################################################

if __name__=='__main__':
    parser=argparse.ArgumentParser()

    parser.add_argument('--striped',
                        metavar='FILE',
                        help='write striped pic to %(metavar)s')

    parser.add_argument('--dithered',
                        metavar='FILE',
                        help='write dithered pic to %(metavar)s')
    
    parser.add_argument('--masked',
                        metavar='FILE',
                        help='write masked pic to %(metavar)s')
    
    parser.add_argument('input_path',
                        metavar='FILE',
                        help='read Mode 2 smiley pic from %(metavar)s')

    main(parser.parse_args())
