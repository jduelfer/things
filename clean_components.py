import csv

e = [] 	#edition 
i = [] 	#idioma
pbe = [] #pricebookentry
opp = [] #opportunities
ti = [] #title of components

luc17 = [] 

############## create dictionaries #################

#set the edition dictionary
with open('SIM2SF-Maestro-Edicion.csv', 'rb') as fe:
	reader = csv.reader(fe)
	e = dict(reader)

#set the idioma dictionary
with open('SIM2SF-Maestro-Idioma.csv', 'rb') as fi:
	reader = csv.reader(fi)
	i = dict(reader)

#set the pbe dict
with open('MaestroPBE.csv', 'rb') as fpbe:
	reader = csv.reader(fpbe)
	pbe = dict(reader)

#set the opp dict
with open('MaestroOportunidades.csv', 'rb') as fopp:
	reader = csv.reader(fopp)
	opp = dict(reader)

#set the title of components dict
with open('MaestroLUPadre.csv', 'rb') as fti:
	reader = csv.reader(fti)
	ti = dict(reader)

############ end dictionary creation ##############

#open our file into a list to process
with open('LibroUsadoComponente_P17.csv', 'rb') as s:
	reader = csv.reader(s)
	luc17 = list(reader)

for line in luc17[1:]:
	if(line[3] != None and line[3] != ''):
		line[3] = e[line[3]]
	if(line[4] != None and line[4] != ''):
		line[4] = i[line[4]]
	#add pbe column
	if(line[1] != None and line[1] != ''):
		line += [pbe[line[1]]]
	#add opp column
	if(line[0] != None and line[0] != ''):
		line += [opp[line[0]]]
		line += [ti[line[0]]]

#write to the new csv
with open('LibroUsadoComponenteAfter_P17.csv', 'wb') as w:
	writer = csv.writer(w)
	for new_line in luc17:
		writer.writerow(new_line)