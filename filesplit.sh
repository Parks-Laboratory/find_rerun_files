#!/bin/bash


while IFS= read -r line;
do
	echo  "$line" > $line 

done < "list.txt"


