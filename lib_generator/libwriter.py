#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to generate an Altium lib with repetitive components.
First, export altium SCHLIB as PCAD V16 (.lia file)
Create Jinja template file with said SCHLIB and put it in template folder.
Template has to be UTF-8 encoded.

@author: Eve Redero
@license: GPL
"""

import os
import jinja2 as jj2
import codecs
import numpy as np
import decimal

SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "output")
if not os.path.exists(OUTPUT_DIR):
    os.mkdir(OUTPUT_DIR)

# Configure template engine
template_env = jj2.Environment(
        extensions=['jinja2.ext.loopcontrols'],
        loader=jj2.FileSystemLoader('templates'))

template_env.globals['target'] = 'libc'

template_name = 'resistors.lia'

# Configure the E96 series values
e96_series = np.array([1, 1.02, 1.05, 1.07, 1.10, 1.13, 1.15, 1.18, 1.21, 1.24,
                       1.27, 1.30, 1.33, 1.37, 1.40, 1.43, 1.47, 1.50, 1.54,
                       1.58, 1.62, 1.65, 1.69, 1.74, 1.78, 1.82, 1.87, 1.91,
                       1.96, 2.00, 2.05, 2.10, 2.15, 2.21, 2.26, 2.32, 2.37,
                       2.43, 2.49, 2.55, 2.61, 2.67, 2.74, 2.80, 2.87, 2.94,
                       3.01, 3.09, 3.16, 3.24, 3.32, 3.40, 3.48, 3.57, 3.65,
                       3.74, 3.83, 3.92, 4.02, 4.12, 4.22, 4.32, 4.42, 4.53,
                       4.64, 4.75, 4.87, 4.99, 5.11, 5.23, 5.36, 5.49, 5.62,
                       5.76, 5.90, 6.04, 6.19, 6.34, 6.49, 6.65, 6.81, 6.98,
                       7.15, 7.32, 7.50, 7.68, 7.87, 8.06, 8.25, 8.45, 8.66,
                       8.87, 9.09, 9.31, 9.53, 9.76], dtype=decimal.Decimal)

n_octaves = 6
# Select our footprints
footprint_series = ["0201", "0402", "0603", "0805"]
e96_all = np.concatenate([e96_series * 10**i for i in range(n_octaves)])

def human_format(num, unit='R', suffix=''):
    '''
    Returns values in a standard electronician format.
    For instance:
        - 1100 => "1.1K"
        - 8.06e6 => "8.06M"
        - 1 => "1R" with parameter 'unit' set to R
    Use 'suffix' to add a unit after the value (e.g, F for capacitors)
    '''
    num = float('{:.3g}'.format(num))
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num /= 1000.0
    return '{}{}{}'.format('{:f}'.format(num).rstrip('0').rstrip('.'),
            [unit, 'k', 'M', 'B', 'T'][magnitude],
            suffix)

e96_formatted = [human_format(num, unit='R') for num in e96_all]

json = {"resistor_values": e96_formatted, "footprint_series": footprint_series}

template = template_env.get_template(template_name + '.in')

with open(os.path.join(OUTPUT_DIR, template_name + '.tmp'), 'w+') as fd:
    fd.write(template.render(json))

# Change text file formating from UTF-8, \n line ending to ISO-8859-1, \r\n
# line ending. Would make Altium loop infinitely otherwise.
with open(os.path.join(OUTPUT_DIR, template_name + '.tmp'), 'r') as outfile:
    copytext = outfile.read()

copytext = copytext.replace(os.linesep, '\r\n')
with codecs.open(os.path.join(OUTPUT_DIR, template_name),
                 'w', "ISO-8859-1") as myfile:
    myfile.write(copytext)

os.remove(os.path.join(OUTPUT_DIR, template_name + '.tmp'))
