#!/bin/sh
STARTPAGE=1 # set to pagenumber of the first page of PDF you wish to convert
ENDPAGE=1000 # set to pagenumber of the last page of PDF you wish to convert
SOURCE=le_fpkl0190 # set to the file name of the PDF
PDF="$SOURCE.pdf"
TXT="$SOURCE.txt"

RESOLUTION=600 # set to the resolution the scanner used (the higher, the better)

touch $TXT
for i in `seq $STARTPAGE $ENDPAGE`; do
    convert  -density $RESOLUTION $PDF\[$(($i - 1 ))\] -depth 8 page.tif
    echo processing page $i
    tesseract page.tif tempoutput

    echo "\nPage $i \n" | cat - tempoutput.txt > temp && mv temp tempoutput.txt
    cat tempoutput.txt >> $TXT

done
