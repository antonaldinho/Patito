#!/bin/bash
# File name must be the same as program ID

name=("$1.txt")
echo "$name"
dout=("$1.dout")
echo "$dout"

python3 PatitoSyntax.py __tests__/$name > log.txt
python3 vm.py $dout > vm-log.txt