#!/usr/bin/python
import png,argparse,os,os.path,sys

##########################################################################
##########################################################################

g_verbose=False

def v(msg):
    if g_verbose:
        sys.stdout.write(msg)
        sys.stdout.flush()

def fatal(msg):
    sys.stderr.write('FATAL: %s\n'%msg)
    sys.exit(1)

##########################################################################
##########################################################################

def main(options):
    global g_verbose;g_verbose=options.verbose

    glyph_width=8
    glyph_height=8
    width_limit=472
    
    png_width,png_height,png_pixels,png_metadata=png.Reader(options.input_path).read()
    png_width=min(png_width,width_limit)
    if png_width%glyph_width!=0:
        fatal('width is %d - not a multiple of %d'%(png_width,
                                                    glyph_width))
    if 'palette' not in png_metadata: fatal('not palettized')
    png_palette=png_metadata['palette']

    for ch in range(png_width//glyph_width):
        for y in range(glyph_height):
            pass
            

##########################################################################
##########################################################################

if __name__=='__main__':
    parser=argparse.ArgumentParser()

    parser.add_argument('-v','--verbose',action='store_true',help='be verbose')

    parser.add_argument('-d',dest='output_data_path',metavar='FILE',help='write font data to %(metavar)s (- for stdout)')
    
    parser.add_argument('-o',dest='output_asm_path',metavar='FILE',help='write asm to %(metavar)s (- for stdout)')
    
    parser.add_argument('input_path',metavar='PNG-FILE',help='load front from %(metavar)s')
    
    main(parser.parse_args())
    
