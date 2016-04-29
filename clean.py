import csv

a = [] 	#asignatura external id key : salesforce id value
c = [] 	#centro external id key : salesforce id value
n = []	#nivel external id key : salesforce id value
cn = [] #caracnivel external id key : text in second column of csv
ch = [] #clasehora external id key : texto in third column of csv
pb = [] #pbe external id key : salesforce id value
op = [] #sim integration external id key : salesforce id value
pbcopy = [] 	#pbe external id key : salesforce product2id value
pbprod = []

lu16 = []
#lu17 = []

################# create dictionaries #################
#set the asig dict
with open('MaestroAsignatura.csv', 'rb') as fa:
	reader = csv.reader(fa)
	a = dict(reader)

#set the centro dict
with open('MaestroCentros.csv', 'rb') as fc:
	reader = csv.reader(fc)
	c = dict(reader)

#set the nivel dict
with open('MaestroNiveles.csv', 'rb') as fn:
	reader = csv.reader(fn)
	n = dict(reader)

#set the caracnivel dict
with open('SIM2SF-Maestro-CaracNivel.csv', 'rb') as fcn:
	reader = csv.reader(fcn)
	cn = dict(reader)

#set the clasehora dict
with open('SIM2SF-Maestro-ClaseHora.csv', 'rb') as fch:
	reader = csv.reader(fch)
	ch = dict(reader)

#set the opportunityid dict
with open('MaestroOp2016.csv', 'rb') as fop:
	reader = csv.reader(fop)
	op = dict(reader)

#set the pbe dict
with open('MaestroPBE.csv', 'rb') as fpb:
	reader = csv.reader(fpb)
	pb = dict(reader)

#set the pbe copy dict
with open('MaestroPBEcopy.csv', 'rb') as fpbcopy:
	reader = csv.reader(fpbcopy)
	pbcopy = dict(reader)

with open('MaestroPBEcopyProd.csv', 'rb') as fpbprod:
	reader = csv.reader(fpbprod)
	pbprod = dict(reader)

################ end dictionaries #####################

#
with open('LibroUsado_P17_chunk5.csv', 'rb') as s:
	reader = csv.reader(s)
	lu16 = list(reader)

#_______________________
#|  field	| csv index	|
#|__________|___________|
#|  nivel 	| 	1		|
#|  centro  | 	3		|
#|  asig  	| 	4		|
#|ti_es_adop|	6		|
#|caracnivel|	22		|
#|c_titulo 	|	24		|
#|tit_es_est|	35		|
#|clasehora	|	44		|
#|edi_adop	|	45		|
#| idi_adop |	47		|
#|__________|___________|

#for line in origina csv
for line in lu16[1:]:		#don't include the headers
	if(line[1] != None and line[1] != ''):
		line[1] = n[line[1]]	#replace the Nivel with salesforce id
	if(line[3] != None and line[3] != ''):
		line += [op[line[3]]]		#add the opportunity id to the end of the list, now at index -1
		line[3] = c[line[3]]	#replace the Center with salesforce id
	if(line[4] != None and line[4] != ''):
		line[4] = a[line[4]] 	#replace the Asignatura with salesforce id	
	if(line[22] != None and line[22] != ''):
		line[22] = cn[line[22]]	#replace the CaracteristicaNivel with salesforceid
	if(line[44] != None and line[44] != ''):
		line[44] = ch[line[44]]	#replace the ClaseHora with third column of csv

	##################################### NEW LINES ########################################
	#ORDER:
	#1. OpportunityId (set above) 
	#2. PriceBookEntryId 
	#3. CurrentTitle__c 
	#4. EstimatedTitle__c
	#5. ProductId
	#6. ExternalId

	#########################
	#INDICES: oppid at [-1]
	#########################

	#2. PriceBookEntry
	if(line[24] != None and line[24] != ''):	#if the line at 24 is not blank 
		line += [pb[line[24]]] 	#create a new column by the id from pb by C_TITULO
	else:	#if the line at 24 is blank
		if(line[6] != None and line[6] != ''):
			line += [pb[line[6]]]	#create a new column by the id from pb by C_TITULO_ES_ADOPTADO 
		else:
			print('pricebookentry fail')
			line += ['']	#just add an empty one

	######################################
	#INDICES: oppid at [-2], pbeid at [-1]
	######################################

	#3.CurrentTitle__c
	if(line[6] != None and line[6] != ''):
		line+=[pb[line[6]]]
	else:
		print('currentitle fail')
		line += ['']	#just add an empty value

	############################################################
	#INDICES: oppid at [-3], pbeid at [-2], currenttitle at [-1]
	############################################################	

	#4.EstimatedTitle
	if(line[35] != None and line[35] != ''):
		line+=[pbprod[line[35]]]
	else:
		line+=['']	#just add an empty value

	###################################################################################
	#INDICES: oppid at [-4], pbeid at [-3], currentitle at [-2], estimatedtitle at [-1]
	###################################################################################

	#5. ProductId
	if(line[-2] != None and line[-2] != ''):
		line+=[pbcopy[line[-2]]]
	else:
		print('product id fail')
		line+=['']

	######################################################################################################
	#INDICES: oppid at [-5], pbeid at [-4], currentitle at [-3], estimatedtitle at [-2], productid at [-1]
	######################################################################################################

	#6. External ID
	line+=[line[3]+'-'+line[-5]+'-'+line[4]+'-'+line[1]+'-'+line[-1]+'-'+line[47]+'-'+line[45]+'-'+line[22]]

	#################################### END NEW LINES ######################################

#now we have lu16 as the correct thing and lets write to file
with open('LibroUsadoAfter_P17_chunk5.csv', 'wb') as lu:
	writer = csv.writer(lu)
	for new_line in lu16:
		writer.writerow(new_line)