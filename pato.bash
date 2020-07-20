#!/bin/bash

name=("$1.txt")
echo "$name"
dout=("$1.dout")
echo "$dout"

python3 PatitoSyntax.py __tests__/$name 
python3 MaquinaVirtual.py __dout__/$dout