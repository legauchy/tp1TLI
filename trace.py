#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from math import *

		
def trace(function, xmin, xmax, nstep, output):
	#output.write("x, %s\n" % function)
	output.write("%!\n")
	
	func_save = function
	function = eval("lambda x:" + function)
	
	x_values = []
	y_values = []
	ymin = sys.maxint
	ymax = -sys.maxint
	
	step = 1.*(xmax-xmin)/nstep
	for i in range(nstep+1):
		x = xmin + i*step
		try:
			y = function(x)
			x_values.append(x)
			y_values.append(y)
			if ymin > y:
				ymin = y
			if ymax < y:
				ymax = y
		except:
			sys.stderr.write("%s is not a valid function for x=%s\n" % (func_save, x) )
			continue
	
	### Traits gris clair ###
	output.write("gsave\n")
	output.write("/Times-Roman findfont\n")
	output.write("18 scalefont\n")
	output.write("setfont\n")
	output.write("newpath\n")
	output.write("0.5 setgray\n")
	output.write("[2] 1 setdash\n")
	
	
	step = (ymax - ymin) / 6.0
	for i in range(0, 7):
		x = 106
		y = 196 + 400 * ((ymin+i*step) - ymin) / (ymax - ymin)
		output.write("%s %s moveto\n" % (x, y))
		output.write("%s %s lineto\n" % (x+400, y))
		output.write("%s %s moveto\n" % (x-40, y-4))
		output.write("(%s) show\n" % str(int((ymin+i*step)*100)/100.0))
	
	step = (xmax - xmin) / 6.0
	for i in range(0, 7):
		x = 106 + 400 * ((xmin+i*step) - xmin) / (xmax - xmin)
		y = 196
		output.write("%s %s moveto\n" % (x, y))
		output.write("%s %s lineto\n" % (x, y+400))
		output.write("%s %s moveto\n" % (x-20, y-16))
		output.write("(%s) show\n" % str(int((xmin+i*step)*100)/100.0))
		
	output.write("stroke\n")
	output.write("grestore\n")
	
	### Contours ###
	output.write("newpath\n")
	output.write("%s %s moveto\n" % (306, 396))
	output.write("%s %s moveto\n" % (306-200, 396))
	output.write("%s %s lineto\n" % (306+200, 396))
	output.write("%s %s moveto\n" % (306, 396-200))
	output.write("%s %s lineto\n" % (306, 396+200))
	output.write("%s %s lineto\n" % (106, 396+200))
	output.write("%s %s lineto\n" % (106, 396-200))
	output.write("%s %s lineto\n" % (506, 396-200))
	output.write("%s %s lineto\n" % (506, 396+200))
	output.write("%s %s lineto\n" % (306, 396+200))
	output.write("stroke\n")
	
	### Fonction ###
	if len(x_values) > 0:
		x = 106 + 400 * (x_values[0] - xmin) / (xmax - xmin)
		y = 196 + 400 * (y_values[0] - ymin) / (ymax - ymin)
		output.write("newpath\n")
		output.write("%s %s moveto\n" % (x, y))
	
		for i in range(len(x_values)):
			x = 106 + 400 * (x_values[i] - xmin) / (xmax - xmin)
			y = 196 + 400 * (y_values[i] - ymin) / (ymax - ymin)
			output.write("%s %s lineto\n" % (x, y))
	
	output.write("stroke\n")	
	output.write("showpage\n")
	


def main(argv=None):
	if argv is None:
		argv = sys.argv
	
	import getopt
	try:
		options, argv = getopt.getopt(argv[1:], "o:hm:M:", ["output=","help","xmin=","xmax="])
	except getopt.GetoptError as message:
		sys.stderr.write("%s\n" % message)
		sys.exit(1)
	
	# Affiche le message d'aide
	for option, value in options:
		if option in ["-h", "--help"]:
			sys.stderr.write("Usage : ./trace.py ([output=]) (o:) \"func(x)\" \n")
			sys.stderr.write("-o, --output : specifier un fichier pour la sortie \n")
			sys.stderr.write("-m, --xmin : borne inférieure de l'interval de définition \n")
			sys.stderr.write("-M, --xmax : borne supérieure de l'interval de définition \n")
			sys.stderr.write("func(x) définition de la fonction à tracer en fontion de 'x' \n")
			sys.exit(1)
	
	if len(argv) != 1:
		sys.stderr.write("Usage : ./trace.py ([output=]) (o:) \"func(x)\" \n")
		sys.stderr.write("-o, --output : specifier un fichier pour la sortie \n")
		sys.stderr.write("-m, --xmin : borne inférieure de l'interval de définition \n")
		sys.stderr.write("-M, --xmax : borne supérieure de l'interval de définition \n")
		sys.stderr.write("func(x) définition de la fonction à tracer en fontion de 'x' \n")
		sys.exit(1)
	function = argv[0]
	
	if len(function) == 0:
		sys.stderr.write("function is empty \n")
		sys.exit(1)
	
	output = sys.stdout
	xmin, xmax = 0.0, 1.0
	for option, value in options:
		if option in ["-o", "--output"]:
			output = file(value, "w")
		elif option in ["-m", "--xmin"]:
			xmin = float(value)
		elif option in ["-M", "--xmax"]:
			xmax = float(value)
		else:
			assert False, "option " + option + "non définie"
	
	if xmax < xmin:
		sys.stderr.write("xmax : %s ne doit pas être plus petit que xmin  : %s\n" %(xmax, xmin) )
		sys.exit(1)
	
	trace(function, xmin, xmax, 100, output)


if __name__ == "__main__":
	sys.exit(main())

