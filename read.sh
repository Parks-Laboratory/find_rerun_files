#!/bin/bash

while IFS= read -r line;
do
	rm epistasis_BF_*	
	mv $line 123.txt
	mv 123.txt $(pwd)/data/
	rm epistasis_BF_*
	python epistasis_submit_DAGman_v2.py BF_PERCENT_GROWTH_0to2wks_MALE -g 600 -m 2 --rerun 123.txt
	sleep 180	
	rm epistasis_BF_*	
	 
done < "list.txt"



