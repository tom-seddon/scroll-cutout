#!/usr/bin/python
import math

def lerp(a,b,t): return a+t*(b-a)

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

    print 'row_routines_list:'
    for index in range(128):
        print '    .word row_routine_%02x'%(index<<1)


    #

    min_delay=92
    max_delay=min_delay+46
    
    print 'delays_list:'
    for index in range(128):
        angle=index/32.0*2.0*math.pi
        delay=int(lerp(min_delay,max_delay,math.sin(angle)*0.5+0.5))
        print '    .word draw_delay_%d'%delay
        
    # 
    for delay in range(max_delay,min_delay,-1):
        print 'draw_delay_%d:'%delay
        print '    .nop1'

    print 'draw_delay_%d:'%min_delay
    print '    .nops %d'%(min_delay-3)
    print '    jmp fx_draw_function.after_delay'

if __name__=='__main__': main()
