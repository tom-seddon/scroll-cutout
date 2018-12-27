# -*- mode:makefile-gmake; -*-
##########################################################################
##########################################################################

TASS:=64tass --m65c02 --nostart -Wall -C --line-numbers

VOLUME:=beeb/scroll-cutout
DEST:=$(VOLUME)/0
TMP:=.tmp
NAME:=cutout

##########################################################################
##########################################################################

.PHONY:build
build:
	mkdir -p $(VOLUME)/0
#	python font_conv.py -o $(TMP)/font.s65 anuvverbubbla_8x8.png
	python make_pics.py --striped '$(DEST)/$$.PIC' --masked '$(DEST)/$$.PIC2' --dithered '$(DEST)/$$.PIC3' '$(VOLUME)/1/2.SMILEY'
	python make_routines.py > $(TMP)/routines.s65
	python make_font.py > $(TMP)/font.s65
	$(MAKE) assemble STEM=$(NAME)
	echo '@.$(NAME) e00 e00' > $(DEST)/@.$(NAME).inf
	ssd_create -4 3 -o $(NAME).ssd '$(DEST)/@.$(NAME)' '$(DEST)/$$.!BOOT' '$(DEST)/$$.PIC' '$(DEST)/$$.PIC2' '$(DEST)/$$.PIC3'
	$(MAKE) test_b2

##########################################################################
##########################################################################

.PHONY:assemble
assemble:
	mkdir -p $(DEST) $(TMP)
	$(TASS) $(STEM).s65 -L$(TMP)/$(STEM).lst -l$(TMP)/$(STEM).sym -o$(DEST)/@.$(STEM)
	touch $(DEST)/@.$(STEM).inf

##########################################################################
##########################################################################

.PHONY:test_b2
test_b2:
	curl -G 'http://localhost:48075/reset/b2' --data-urlencode "config=Master 128 (MOS 3.20)"
	curl -H 'Content-Type:application/binary' --upload-file '$(NAME).ssd' 'http://localhost:48075/run/b2?name=$(NAME).ssd'
