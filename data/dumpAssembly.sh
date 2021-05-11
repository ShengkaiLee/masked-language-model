#!/bin/bash
for d1 in */ ; do
    for d2 in $d1*/ ; do
	for d3 in $d2*; do
		if [[ "$d3" != *".asm"* ]]; then
		#[ ! -d ${d2}assembly ] && mkdir ${d2}assembly
		[ ! -d $d3 ] && objdump -j .text -d $d3 > ${d3}.asm
		[ ! -d $d3 ] && rm $d3
		#[ ! -d $d3 ] && python3 assemblyParsing.py $d3 $d2
		#mv ${d2}*.assembly $d2/assembly/
		fi
	done
    done
done