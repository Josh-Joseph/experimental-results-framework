#!/bin/bash

bn=$(basename $1)
echo $1 $2/$3$bn
cp $1 $2/$3$bn
