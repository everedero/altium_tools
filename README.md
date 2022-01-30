# Altium lib tools

A collection of scripts to process Altium files and libraries.

## Lib generator
Allows to generate automatically a repetitive component library, 
for instance with every E96 resistor values, or multiple capacitor values.

## Pin remapper
Allows to remap pins on a symbol, typically, change SoC GPIO names to add
or remove the alternate names, or change pin number from different SoM
implementation on the same SoC.

## HTML report parser
Altium allows to export HTML reports on libraries. This script parses it
to get statistics on pin numbers by components, which Altium weirdly
cannot do.
