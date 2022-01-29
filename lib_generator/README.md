# Automatic generation for Altium SchLib

The tip is to export a schematic lib in .lia format, corresponding to a P-CAD library, which has the good taste to be a text format. 
Once the lib has been created, use Jinja2 magic to create a template file.

Then it is possible to re-import a modified .lia using the Import Wizard.
Just open the generated .lia files and click "Next" several times, until the Wizard generates you a proper SchLib.

Be careful, Altium is very sensitive to encoding and line feeds: modified file must be \\r\\n line breaks and ISO-8859-1 encoding.

## Post-treatment
Some data is lost during the import/export process.

* Use the SCHLIB List panel to display all parameters, and set them all to the right color and font.
* Use SHIFT-F to select all "PartNumber" parameters, modify the display boolean, color, font and position
Alternativery, use SCHLIB Filter panel and request: "(ObjectKind = 'Parameter') And (ParameterName = 'PartNumber')"
* Also use SHIFT-F to select all designators, change them to R? instead of U?, and modify display options
SCHLIB Filter request: "ObjectKind = 'Designator'"
* Select all parameters and toggle PartNumber and Designator visibility.
SCHLIB Filter request: "ObjectKind = 'Part'"

### To be fixed
* Description fields are empty
* Bug with designator display

## Notes on .lia file structure
.lia are kind of hierarchical files based on parenthesis.

Nodes "symbolDef" represents a package, with the graphical elements
coordinates (pins, lines, text...).

Nodes "compDef" represents a component and has a link to its package.

```
(library
	(symbolDef "mysymbol_N"
		(pin
			...
		)
		(line
			...
		)
	)
	(compDef
		(compPin "mycomponent"
			...
		)
		(attachedSymbol (symbolName "mysymbol_N")
			...
		)
```
