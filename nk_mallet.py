#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
@author: nkodkani

Description: Remove the stop words in brief summary and detailed description using the mallet and generate new xml file
"""

import glob
import xml.etree.ElementTree as ET
import commands
import os

def extract_data_xml():
       """
       This function is used to extract the desired data from the input xml files.
       """
       
       #Provide the path to the input xml files
       list_of_files = glob.glob('/home/nikita/Documents/mallet-2.0.8/clinicaltrials_xml/*/*' + '/*.xml')
       #Counter variable to count each processed file
       ctr = 0
       
       #Print the progress as we process each file
       print '\nProgress:'
       
       #This for loop iterates over each input file. Within each try-except block we try to extract the data from one particular xml field. This extracted data is stored in an ordered dictionary with key as the field name and value as the extracted data.
       #Currently the following fields are extracted: brief_summary, detailed_description
       #Not all the files contain all the fields we desire, hence the multiple try-except blocks.
       for input_file in list_of_files:
              tree = ET.parse(input_file)
              root = tree.getroot()
              
              #brief_summary
              try:
                     brief_summary = root.find('brief_summary').find('textblock').text
                     stemp_file = 'summary_temp_file'
                     f=open(stemp_file,'w')
                     print >>f,brief_summary
                     f.close()

                     # Invoke the mallet command from the python 
                     smallet="bin/mallet import-file --input summary_temp_file --print-output --remove-stopwords --keep-sequence | awk -F ' ' '{if($2 ==\"0:\") {print $3} else {print $2}}' | tr -s '\n' ' '"
                     smallet_output = commands.getoutput(smallet)
                     os.remove(stemp_file)

                     print smallet_output
                     root.find('brief_summary').find('textblock').text = smallet_output

              except:
                     mallet = None

              #detailed_description
              try:
                     detailed_description = root.find('detailed_description').find('textblock').text
                     dtemp_file = 'desc_temp_file'
                     f=open(dtemp_file,'w')
                     print >>f,detailed_description
                     f.close()

                     # Invoke the mallet command from the python 
                     dmallet="bin/mallet import-file --input desc_temp_file --print-output --remove-stopwords --keep-sequence | awk -F ' ' '{if($2 ==\"0:\") {print $3} else {print $2}}' | tr -s '\n' ' '"
                     dmallet_output = commands.getoutput(dmallet)
                     os.remove(dtemp_file)

                     print dmallet_output
                     root.find('detailed_description').find('textblock').text = dmallet_output

              except:
                     mallet = None

              # Update the input file  
              tree.write(input_file)

              #Increment the counter and print the progress in the following format: current counter value/total number of input files.
              ctr+=1
              print ctr,'/',len(list_of_files)



if __name__ == '__main__':
       #Call the function to start extracting the data
       extract_data_xml()

