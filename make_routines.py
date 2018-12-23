#!/usr/bin/python

def main():
    for index in range(128):
        value=index<<1
        
        cycles=0
        print 'row_routine_%02x:'%value
        mask=128
        while mask!=1:
            if value&mask!=0: ins='tsb'
            else: ins='trb'

            cycles+=6
            print '    %s acccon ; ($%02x) 6 %d'%(ins,mask,cycles)
            mask>>=1

        cycles+=3
        print '    jmp fx_draw_function.char_done ; 3 %d'%cycles
        print

    print 'routines_list:'
    for index in range(128):
        print '    .word row_routine_%02x'%(index<<1)

if __name__=='__main__': main()
