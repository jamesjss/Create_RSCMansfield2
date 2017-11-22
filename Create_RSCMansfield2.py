#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import cookielib, urllib2, requests, json, sys, getopt
from urllib2 import urlopen
from datetime import datetime, timedelta
from lxml import html

ofile="RSCMansfield2.txt"

today = datetime.today()  # Asigna fecha actual
hace52Sem = today - timedelta(days=364)  # Resta a fecha actual 52 semanas (52*7)

end_date=datetime.now().strftime ("%m/%d/%Y")
init_date=hace52Sem.strftime ("%m/%d/%Y")

payload = {
	"loginFormUser_email": "jaisan79@hotmail.com", 
	"loginForm_password": "2wU11ugLLxY2", 
	"logintoken": "6ae362b798f7904efec5e927e02dc626"
}

#site = "https://es.investing.com/instruments/DownloadHistoricalData?curr_id=166&smlID=2030167&header=Datos+históricos+S%26amp%3BP+500&st_date=" + init_date + "&end_date=" + end_date + "&interval_sec=Weekly&sort_col=date&sort_ord=DESC"
site = "http://quotes.wsj.com/index/SPX/historical-prices/download?MOD_VIEW=page&num_rows=365&range_days=365&startDate=" + init_date + "&endDate=" + end_date
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

req = urllib2.Request(site, headers=hdr)

try:
    page = urllib2.urlopen(req)
except urllib2.HTTPError, e:
    print e.fp.read()

content = page.read()

data = []
rownum = 0
for line in content.split('\n'):
	if rownum == 0:
		header = line
	else:
		data_detail = []
		for field in line.split(','):
			data_detail.append(field)
		data.append(data_detail)
	rownum += 1


# Recorremos el array.
# Si la primera fecha es un viernes se recorren los primeros 52 viernes (dia 4 de weekday)
# Si la primera fecha no es un viernes se recorre la primera fecha + los 51 viernes restantes (día 4 de weekday)
priceWeeks=[]
rownum = 1
#dayOfWeek y lastWeekdayOfWeek serviran para determinar el último dia de la semana en que el SP500 estuvo operativo,
#siempre que se encuentre un dia superior o igual al anterior tratado se supondrá que es una semana nueva
dayOfWeek = 0
lastWeekdayOfWeek = 0
for line in data:
	oneWeek=[]
	date=datetime.strptime(line[0], "%m/%d/%y").date()
	dayOfWeek=date.weekday()
	if rownum == 1:
		oneWeek.append(date)
		oneWeek.append(line[4])
		priceWeeks.append(oneWeek)
		rownum += 1
	else:
		if dayOfWeek>=lastWeekdayOfWeek:
			oneWeek.append(date)
			oneWeek.append(line[4])
			priceWeeks.append(oneWeek)
			rownum += 1
	lastWeekdayOfWeek = dayOfWeek
	if rownum == 53:
		break
	
text_file = open(ofile, "w")


text_file.write("REM Indicador realizado por Javier Alfayate\n")
text_file.write("REM administrador de Aguila Roja Sistemas de\n")
text_file.write("REM trading y autor de accionesdebolsa.com\n")
text_file.write("REM si vas a utilizar este código, no lo difundas\n")
text_file.write("REM sin autorización expresa de mi parte.\n")
text_file.write("REM este indicador está diseñado para los foreros\n")
text_file.write("REM y no es un código definitivo. Es necesaria la\n")
text_file.write("REM actualización de ciertos valores para su\n")
text_file.write("REM correcto funcionamiento.\n")
text_file.write("REM Indicador generado automáticamente por script Create_RSCMansfield2.py (Jaume Sanchez)\n")
text_file.write("\n")
text_file.write("CountR=0\n")
text_file.write("i=51\n")
text_file.write("\n")
rownum=1
for line in reversed(priceWeeks):
	text_file.write("R= Close[i]/" + line[1] + "\n")
	text_file.write("CountR=CountR+R\n")
	if rownum != 52:
		text_file.write("i=i-1\n")
	text_file.write("\n")
	rownum+=1

text_file.write("BasePrice = CountR / 52\n")
text_file.write("FR = ((R / BasePrice) – 1) * 10\n")
text_file.write("\n")
text_file.write("CERO = 0\n")
text_file.write("SENYAL = FR\n")
text_file.write("RETURN CERO AS “CERO”, SENYAL AS “FR”\n")

text_file.close()

print ""
print "Archivo RSCMansfield2.txt creado correctamente"
print ""
print "Puedes realizar un donativo accediendo a esta página:"
print "https://www.paypal.me/jamesjss\n"

