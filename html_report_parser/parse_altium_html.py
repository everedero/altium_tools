#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Another regexp parser, to export pin number by components from Altium lib
HTML reports.
It allows to count the pin numbers in a library file.
Put all the html lib*.html in the same folder.
The script exports a pin_numbers csv file.

@author: Eve Redero
@license: GPL
"""
import os
import re
import csv
import io

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
directory = os.path.join(SCRIPT_DIR, "html")
base_filename = "DVLT_IC_{}.html"
output_filename = "pin_numbers.csv"
components = list()
pins = list()
descs = list()
idx = 1

while True:
    file = base_filename.format(idx)
    filename = os.path.join(directory, file)
    idx += 1
    if not os.path.exists(filename):
        print("Last file at index {}".format(idx-1))
        break
    
    with open(filename, "r") as myfile:
        html = ""
        for line in io.open(filename, encoding="ISO-8859-1", newline="\r\n"):
            html = html + line
    
    reg_name = re.compile("""<b>\s+Library Reference\s+</b>\s+</font>\s+""" +\
                       """</td>\s+<td valign="top">\s+<h2>\s+""" +\
                       """<font face="Arial" size="2">\s+([\S ]+)\s+</font>""", re.MULTILINE)
    
    
    reg_num = re.compile("""Number of Pins\s+</b>\s+</font>\s+""" +\
                       """</td>\s+<td valign="top">\s+<font face="Arial" size="2">\s+""" +\
                       """(\d+)""", re.MULTILINE)
    
    reg_desc = re.compile("""<b>\s+Description\s+</b>\s+</font>\s+""" +\
                """</td>\s+<td valign="top">\s+<font face="Arial" size="2">\s+""" +\
                """(.*)\r$""" +\
                """\s+</font>""", re.MULTILINE)
    reg_package = re.compile("""<font face="Arial" size="2">\s+""" +\
        """PackageReference\s+</font>\s+</td>\s+""" +\
        """<td valign="top">\s+<font face="Arial" size="2">\s+""" +\
        """(.*)\r$\s+</font>\s+</td>""", re.MULTILINE)
    regexpes = [reg_name, reg_num, reg_desc, reg_package]
    
    component_name = reg_name.findall(html)
    if len(component_name) < 1:
        print("No component found at idx {}".format(idx))
        continue
    else:
        component_name = component_name[0]
    component_pin_num = reg_num.findall(html)
    if len(component_pin_num) < 1:
        print("No pin number found for component {}".format(component_name))
        component_pin_num = 0
    else:
        component_pin_num = component_pin_num[0]
    component_desc = reg_desc.findall(html)
    if len(component_desc) < 1:
        print("No description found for component {}".format(component_name))
        component_desc = 0
    else:
        component_desc = component_desc[0]
    components.append(component_name)
    pins.append(int(component_pin_num))
    descs.append(component_desc)
    
output_file = output_filename
mylist = zip(components, pins, descs)
with open(output_file, 'w') as myfile:
    mycsv = csv.writer(myfile)
    mycsv.writerows(mylist)