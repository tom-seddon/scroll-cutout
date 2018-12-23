#!/usr/bin/python

def main():
    for value in range(256):
        cycles=6
        print 'row_routine_%02x:'%value
        for bit in range(8):
            if value&(1<<(7-bit))!=0: ins='trb'
            else: ins='tsb'

            cycles+=4
            print '    %s acccon ; 4 %d'%(ins,cycles)

        cycles+=6
        print '    rts ; 6 %d'%cycles
        print

if __name__=='__main__': main()
