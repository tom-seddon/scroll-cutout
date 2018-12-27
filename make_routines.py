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
        
    #
    screen_addrs=[]
    for index in range(256):
        angle=index/255.0*16*math.pi
        dx=math.sin(angle)*0.5
        dy=math.cos(angle)*0.5

        # not quite centred!
        if dx<0: x=dx*28
        else: x=dx*34

        if dy<0: y=dy*14
        else: y=dy*8

        addr=0x3000+int(x)*8+int(y)*640
        if addr<0x3000: addr+=0x5000
        screen_addrs.append(addr>>3)

    print 'screen_addrs_l:'
    for a in screen_addrs: print '    .byte <$%04x'%a
    print 'screen_addrs_h:'
    for a in screen_addrs: print '    .byte >$%04x'%a
        

if __name__=='__main__': main()
