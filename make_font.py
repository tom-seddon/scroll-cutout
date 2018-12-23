#!/usr/bin/python
import png,argparse,os,os.path,sys

##########################################################################
##########################################################################

def fatal(msg):
    sys.stderr.write('FATAL: %s\n'%msg)
    sys.exit(1)

##########################################################################
##########################################################################

def main():
    glyph_width=8
    glyph_height=8
    width_limit=472

    png_width,png_height,png_pixels,png_metadata=png.Reader('verifier_font_8x8.png').read()
    png_width=min(png_width,width_limit)
    if png_width%glyph_width!=0:
        fatal('width is %d - not a multiple of %d'%(png_width,
                                                    glyph_width))
    if 'palette' not in png_metadata: fatal('not palettized')
    png_palette=png_metadata['palette']

    print 'font_data:'
    for ch in range(png_width//glyph_width):
        all=0
        print '; \'%s\' - %d, $%02x'%(chr(32+ch),32+ch,32+ch)
        for y in range(glyph_height):
            row=0
            for x in range(glyph_width):
                colour=png_palette[png_pixels[y][ch*glyph_width+x]]
                if colour[3]!=0: row|=1
                row<<=1
            bin_str=('00000000'+bin(row)[2:])[-8:]
            print '    .byte %%%s'%bin_str
            if row&1: fatal('glyph %d row %d has bit 0 set'%(ch,y))

##########################################################################
##########################################################################

if __name__=='__main__': main()
    
