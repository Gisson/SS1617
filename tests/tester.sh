#!/bin/bash

python=python2

if [[ ! -d ../../phply ]];then
	git clone --depth 1 https://github.com/viraptor/phply.git
fi

if [[ -z $(echo $PYTHONPATH | grep phply) ]];then
	export PYTHONPATH="$PYTHONPATH:$(pwd)/../../phply"
fi

mkdir -p output

if [[ ! -n $(pip -V | grep "python 2") ]];then
	python=python3
fi

echo "`tput bold`-------STARTING TESTS------`tput sgr0`"
for i in $(find . -name "*.php");do
	echo "`tput bold`-------STARTING TEST $i ----------`tput sgr0`"
	$python ../src/analyzer.py $i | tee output/$(sed "s/\.php/\.out/" <<< "$i")
done

