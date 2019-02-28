#!/bin/bash

echo 'Please enter whichever Python interpreter provides you with Python 3:'
echo '[ python ] OR [ python3 ]'
read py

echo 'Enter a recipe url please':
read url

#echo 'Do you want to modify this recipe in any way?'
#read way

$py query.py $url

echo 'Done!'
