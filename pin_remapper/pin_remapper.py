#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to batch change pin names in a component.
First, create an Altium SCHLIB with only one component.
Export it as PCAD V16 (.lia file)
Export a pin csv thanks to this script, copy this csv with a
pinNameRemapped column with new pin names.

@license: GPL
@author: Eve Redero
"""

import re
import io
import csv
import codecs
import os
import logging

lia_filename = "soc.lia"
output_filename = "soc_remapped.lia"
remap_pin_col_name = "compPinRemapped"
remap_name_col_name = "pinNameRemapped"
original_name_col_name = "pinName"
original_pin_col_name = "compPin"

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

filename = os.path.join(SCRIPT_DIR, lia_filename)

def lia_to_text(filename):
    '''
    Opens file and returns text
    '''
    mytext = ""
    for line in io.open(filename, encoding="ISO-8859-1", newline="\r\n"):
        mytext = mytext + line
    return(mytext)

def export_pin_list(lia_text):
    '''
    Exports a list of pin in CSV from the string returned by lia_to_text.
    '''
    # Parse pins
    myreg = re.compile("""\(compPin "(\S+)" \(pinName "(\S+)"\) \(partNum (\d+)\) \(symPinNum (\d+)\) \(gateEq (\d+)\) \(pinEq (\d+)\) \(pinType (\S+)\) \)""")
    parsed_pin_header = ["compPin", "pinName", "partNum", "symPinNum", "gateEq", "pinEq", "pinType"]
    parsed_pin_list = myreg.findall(lia_text)
    
    # Export csv with pin list
    with open(filename + ".csv", 'w') as myfile:
        writer = csv.writer(myfile)
        writer.writerow(parsed_pin_header)
        writer.writerows(parsed_pin_list)
    
def remap_pins(filename, remap_csv_file):
    '''
    Renames pins from .lia filename, with a look up table in remap_csv_file.
    To create remap_csv_file, copy the csv returned by export_pin_list
    and add a column pinNameRemapped.
    Columns "pinName" and "compPin" from .lia are taken from reference.
    Name the modification you want: "pinNameRemapped".
    '''
    # Remap file
    with open(remap_csv_file, "r") as myfile:
        reader = csv.reader(myfile, delimiter=";")
        remap = []
        for line in reader:
            remap.append(line)
    
    remap_header = remap.pop(0)
            
    remap_name_col = remap_header.index(remap_name_col_name)
    remap_original_name_col = remap_header.index(original_name_col_name)
    
    mytext = lia_to_text(filename)
    
    # This regexp gives back the list of pins in fields compPin in 
    # compDef part, the pin description section
    myreg = re.compile("""\(compPin "(\S+)" \(pinName "(\S+)"\) \(partNum (\d+)\) \(symPinNum (\d+)\) \(gateEq (\d+)\) \(pinEq (\d+)\) \(pinType (\S+)\) \)""")

    # Replace in pin description section
    copytext = mytext
    for pin_found in myreg.finditer(mytext):
        groups = pin_found.groups()
        original = pin_found.group()
        pinName = groups[1]
        rep = ""
        for remap_line in remap:
            if remap_line[remap_original_name_col] == pinName:
                rep = re.sub(pinName, remap_line[remap_name_col], original)
                logging.debug("Remapped old: {} with new: {}".format(original, rep))
        if rep != "":
            copytext = copytext.replace(original, rep)
    
    # Replace in pinmap section
    myreg_pinmap = re.compile("""\(padNum  (\d+)\) \(compPinRef "(\S+)"\)""")
    
    for pin_found in myreg_pinmap.finditer(mytext):
        groups = pin_found.groups()
        original = pin_found.group()
        pinName = groups[1]
        rep = ""
        for remap_line in remap:
            if remap_line[remap_original_name_col] == pinName:
                rep = re.sub(pinName, remap_line[remap_name_col], original)
                logging.debug("Remapped old: {} with new: {}".format(original, rep))
        if rep != "":
            copytext = copytext.replace(original, rep)
               
    # Replace in pin name section
    myreg_pindesc = re.compile("""\s+\(pin \(pinNum (\d+)\).*$""" +\
                               """\s+\(pinDisplay.*$""" +\
                               """\s+\(pinDes\s+\(text\s+\(pt \S+ \S+\) "(\S+)" .*$""" +\
                               """\s+\)$""" +\
                               """\s+\(pinName\s+\(text\s+\(pt \S+ \S+\) "(\S+)"\s*""", re.MULTILINE)
    for pin_found in myreg_pindesc.finditer(mytext):
        groups = pin_found.groups()
        original = pin_found.group()
        pinName = groups[1]
        rep = ""
        for remap_line in remap:
            if remap_line[remap_original_name_col] == pinName:
                rep = re.sub(pinName, remap_line[remap_name_col], original)
                logging.debug("Remapped old: {} with new: {}".format(original, rep))
        if rep != "":
            copytext = copytext.replace(original, rep)
        
    # Exporting remapped file
    filename_out = re.sub(".lia", ".remap.lia", filename)

    with codecs.open(filename_out, 'w', "ISO-8859-1") as myfile:
        myfile.write(copytext)

if __name__ == '__main__': 
    lia_text = lia_to_text(lia_filename)
    export_pin_list(lia_text)
    remap_csv_file = "remap.csv"
    remap_pins(lia_filename, remap_csv_file)