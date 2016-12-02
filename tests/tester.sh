#!/bin/bash

python=python2

if [[ ! -d ../../phply ]];then
	git clone --depth 1 https://github.com/viraptor/phply.git
fi

if [[ ! -n $(echo $PYTHONPATH | grep phply) ]];then
	export PYTHONPATH="$PYTHONPATH:$(pwd)../../phply"
fi

mkdir -p output

if [[ ! -n $(pip -V | grep "python 2") ]];then
	python=python3
fi

for i in $(find . -name "*.php");do
	$python ../src/analyzer.py $i | tee output/$(sed "s/\.php/\.out/" <<< "$i")
done

