#!/bin/bash
rm -f out.txt
echo Please enter the KeyWord:
read varkw
echo processing webscrape
python arxivscrape.py $varkw >> out.txt
echo processing wordcloud_generator
python wordcloud_generator.py
