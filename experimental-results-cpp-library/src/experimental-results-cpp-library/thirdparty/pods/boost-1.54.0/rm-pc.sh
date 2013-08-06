#!/bin/bash

bn=$(basename $1)
echo $1 $2/$3$bn
rm $1 $2/$3$bn
