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
	python make_routines.py > $(TMP)/routines.s65
	$(MAKE) assemble STEM=$(NAME)
	echo '@.$(NAME) e00 e00' > $(DEST)/@.$(NAME).inf
	ssd_create -o $(NAME).ssd $(DEST)/@.$(NAME) $(DEST)/$$.!BOOT

##########################################################################
##########################################################################

.PHONY:assemble
assemble:
	mkdir -p $(DEST) $(TMP)
	$(TASS) $(STEM).s65 -L$(TMP)/$(STEM).lst -l$(TMP)/$(STEM).sym -o$(DEST)/@.$(STEM)
	touch $(DEST)/@.$(STEM).inf

##########################################################################
##########################################################################
