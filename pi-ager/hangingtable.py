#!/usr/bin/python
# -*- coding: iso-8859-1 -*-

######################################################### Importieren der Module
import sys
import os
import json
import glob
import time
import datetime
import csv
import gettext
from datetime import timedelta
######################################################### Definieren von Funktionen
#---------------------------------------------------------------------------------- Function Lesen der tables.json
def read_tables_json():
    global tables_json_file
    current_data = None
    with open(tables_json_file, 'r') as tablesjsonfile:
        table_data = tablesjsonfile.read();
    data_tablesjsonfile = json.loads(table_data);
    return data_tablesjsonfile
#---------------------------------------------------------------------------------- Function Lesen der settings.json
def read_settings_json():
    global settings_json_file
    settings_data = None
    with open(settings_json_file, 'r') as settingsjsonfile:
        settings_data = settingsjsonfile.read()
    data_settingsjsonfile = json.loads(settings_data)
    return data_settingsjsonfile
#---------------------------------------------------------------------------------- Function Lesen der config.json
def read_config_json():
    global config_json_file
    config_data = None
    with open(config_json_file, 'r') as configjsonfile:
        config_data = configjsonfile.read()
    data_configjsonfile = json.loads(config_data)
    return data_configjsonfile
#---------------------------------------------------------------------------------- Function Schreiben der settings.json
def write_settings_json(modus, setpoint_temperature, setpoint_humidity, circulation_air_period, circulation_air_duration, exhaust_air_period, exhaust_air_duration):
    global settings_json_file

    setting_data = json.dumps({"modus":modus, "setpoint_temperature":setpoint_temperature, "setpoint_humidity":setpoint_humidity, "circulation_air_period":circulation_air_period, "circulation_air_duration":circulation_air_duration, "exhaust_air_period":exhaust_air_period, "exhaust_air_duration":exhaust_air_duration, "switch_on_cooling_compressor":switch_on_cooling_compressor, "switch_off_cooling_compressor":switch_off_cooling_compressor, "switch_on_humidifier":switch_on_humidifier, "switch_off_humidifier":switch_off_humidifier, "delay_humidify":delay_humidify, 'date':int(time.time()), 'sensortype':sensortype})
    with open(settings_json_file, 'w') as settingsjsonfile:
        settingsjsonfile.write(setting_data)
#---------------------------------------------------------------------------------- Function Schreiben der current.json
def write_current_json(sensor_temperature, sensor_humidity):
    global current_json_file

    current_data = json.dumps({"sensor_temperature":sensor_temperature, "status_heater":gpio.input(gpio_heater), "status_exhaust_air":gpio.input(gpio_exhaust_fan), "status_cooling_compressor":gpio.input(gpio_cooling_compressor), "status_circulating_air":gpio.input(gpio_circulation_fan),"sensor_humidity":sensor_humidity, 'last_change':int(time.time())})
    with open(current_json_file, 'w') as currentjsonfile:
        currentjsonfile.write(current_data)
#---------------------------------------------------------------------------------- Funktion zur Übersetzung von z.B. Listenobjekten z.B. animals = [N_('mollusk'), N_('albatross'), N_('rat')]
def N_(message):
    return message
#---------------------------------------------------------------------------------- Funktion zur schreiben in das Logfile
def write_verbose(logstring):
    logfile_txt = open(logfile_txt_file, 'a')           # Variable target = logfile.txt öffnen
    logfile_txt.write(logstring)
    logfile_txt.close
    print logstring
#---------------------------------------------------------------------------------- Function write verbose
def write_verbose(logstring, newLine=False, print_in_logfile=False):
    global verbose
    
    if(verbose):
        print(logstring)
        if(newLine is True):
            print('')
    if (print_in_logfile is True):
        logfile_txt = open(logfile_txt_file, 'a')           # Variable target = logfile.txt öffnen
        logfile_txt.write(logstring)
        logfile_txt.close
#---------------------------------------------------------------------------------- Funktion zum Lesen des Dictionarys und setzen der Werte
def read_dictionary(dictionary):
    # print 'DEBUG read_dictionary()'
    # Variablen aus Dictionary setzen
    for key, value in dictionary.iteritems():
        if value == '':                      # wenn ein Wert leer ist muss er aus der letzten settings.json ausgelesen  werden
            data_settings_json = read_settings_json()
            value = data_settings_json['' + key + '']
            exec('%s = %d') % (key,value)    # füllt die jeweilige Variable mit altem Wert (value = columname)
        else:
            value = int(value)
            exec('%s = %d') % (key,value)
        
    duration = int (days)
    global duration_sleep
    duration_sleep = int(duration) * day_in_seconds    # Anzahl der Tage von "column" mit 86400 (Sekunden) multipliziert für wartezeit bis zur nächsten Periode
#---------------------------------------------------------------------------------- Aufbereitung für die Lesbarkeit im Logfile und Füllen der Variablen
    modus = int(modus + 0.5)                # Rundet auf Ganzzahl, Integer da der Modus immer Integer sein sollte 
    if modus == 0:
        operating_mode = "\n" + _('Betriebsart: Kühlen')
    elif modus == 1:
        operating_mode = "\n" + _('Betriebsart: Kühlen mit Befeuchtung')
    elif modus == 2:
        operating_mode = "\n" + _('Betriebsart: Heizen mit Befeuchtung')
    elif modus == 3:
        operating_mode = "\n" + _('Betriebsart: Automatik mit Befeuchtung')
    elif modus == 4:
        operating_mode = "\n" + _('Betriebsart: Automatik mit Be- und Entfeuchtung')
    else:
        operating_mode = "\n" + _('Betriebsart falsch oder nicht gesetzt')
    setpoint_temperature_logstring = "\n" + _('Soll-Temperatur:') + " \t \t" + str(setpoint_temperature) + "°C"
    switch_on_cooling_compressor_logstring = "\n" + _('Einschaltwert Temperatur:') + " \t" + str(switch_on_cooling_compressor) + "°C"
    switch_off_cooling_compressor_logstring = "\n" + _('Ausschaltwert Temperatur:') + " \t" + str(switch_off_cooling_compressor) + "°C"
    sollfeuchtigkeit_logstring = "\n" + _('Soll-Feuchtigkeit:') + " \t \t" + str(setpoint_humidity) + "%"
    switch_on_humidifier_logstring = "\n" + _('Einschaltwert Feuchte:') + " \t \t" + str(switch_on_humidifier) + "%"
    switch_off_humidifier_logstring = "\n" + _('Ausschaltwert Feuchte:') + " \t \t" + str(switch_off_humidifier) + "%"
    delay_humidify_logstring = "\n" + _('Befeuchtungsverzögerung:') + " \t" + str(delay_humidify) + "min"
    circulation_air_period_format = int(circulation_air_period)/60
    circulation_air_period_logstring = "\n" + _('Timer Umluftperiode alle:') + " \t" + str(circulation_air_period_format) + "min"
    circulation_air_duration_format = int(circulation_air_duration)/60
    circulation_air_duration_logstring = "\n" + _('Timer Umluftdauer:') + " \t  \t" + str(circulation_air_duration_format) + "min"
    exhaust_air_period_format = int(exhaust_air_period)/60
    exhaust_air_period_logstring = "\n" + _('Timer Abluftperiode alle:') + " \t" + str(exhaust_air_period_format) + "min"
    exhaust_air_duration_format = int(exhaust_air_duration)/60
    exhaust_air_duration_logstring = "\n" + _('Timer Abluftdauer:') + " \t \t" + str(exhaust_air_duration_format) + "min"
    period_days_logstring="\n" + _('Dauer:') + " \t \t \t \t" + str(days) + _(' Tage')
    sensor_logstring = _('Sensortyp: ') + " \t \t \t" + sensorname + ' Value: ' + str(sensortype)
    
    
    # print 'DEBUG schreibe settings.json in if'
    write_settings_json (modus, setpoint_temperature, setpoint_humidity, circulation_air_period, circulation_air_duration, exhaust_air_period, exhaust_air_duration)
    global period_endtime
    period_endtime = datetime.datetime.now() + timedelta(days = duration) # days = parameter von timedelta
    logstring = operating_mode + setpoint_temperature_logstring + switch_on_cooling_compressor_logstring + switch_off_cooling_compressor_logstring + "\n" + sollfeuchtigkeit_logstring + switch_on_humidifier_logstring + switch_off_humidifier_logstring + delay_humidify_logstring + "\n" + circulation_air_period_logstring + circulation_air_duration_logstring + "\n" + exhaust_air_period_logstring + exhaust_air_duration_logstring + "\n" + period_days_logstring + "\n" + sensor_logstring + "\n" '---------------------------------------'
    write_verbose(logstring, False, True)
    
    
######################################################### Definition von Variablen
#---------------------------------------------------------------------------------- Pfade zu den Dateien
website_path = '/var/www'
csv_path = website_path + '/csv/'
settings_json_file = website_path+'/settings.json'
tables_json_file = website_path + '/tables.json'
config_json_file = website_path + '/config.json'
current_json_file = website_path + '/current.json'
logfile_txt_file = website_path + '/logfile.txt'
verbose = True                # Dokumentiert interne Vorgänge wortreich
#---------------------------------------------------------------------------------- Allgemeingültige Werte aus config.json
data_config_json = read_config_json()
sensortype = data_config_json ['sensortype']                                        # Sensortyp
language = data_config_json ['language']                                            # Sprache der Textausgabe
switch_on_cooling_compressor = data_config_json ['switch_on_cooling_compressor']    # Einschalttemperatur
switch_off_cooling_compressor = data_config_json ['switch_off_cooling_compressor']  # Ausschalttemperatur
switch_on_humidifier = data_config_json ['switch_on_humidifier']                    # Einschaltfeuchte
switch_off_humidifier = data_config_json ['switch_off_humidifier']                  # Ausschaltfeuchte
delay_humidify = data_config_json ['delay_humidify']                                # Luftbefeuchtungsverzögerung

#---------------------------------------------------------------------------------- Tabelle aus tables.json
data_tables_json = read_tables_json()                   # Function-Aufruf
hangingtable = data_tables_json['hangingtable']    # Variable reifetablename = Name der Reifetabelle

#---------------------------------------------------------------------------------- bedingte Werte aus Variablen
#---------------------------------------------------------------------------------------------------------------- csv-datei
csv_file = hangingtable + '.csv'                       # Variable csv_file = kompletter Dateiname
#---------------------------------------------------------------------------------------------------------------- Sensor
if sensortype == 1 :
    sensortype_txt = '1'
    sensorname = 'DHT11'
elif sensortype == 2 :
    sensortype_txt = '2'
    sensorname = 'DHT22'
elif sensortype == 3 :
    sensortype_txt = '3'
    sensorname = 'SHT'
#---------------------------------------------------------------------------------------------------------------- Sprache
####   Set up message catalog access
# translation = gettext.translation('pi_ager', '/var/www/locale', fallback=True)
# _ = translation.ugettext
if language == 'de':
    translation = gettext.translation('pi_ager', '/var/www/locale', languages=['en'], fallback=True)
elif language == 'en':
    translation = gettext.translation('pi_ager', '/var/www/locale', languages=['de'], fallback=True)
# else:
    
translation.install()

f= [N_('mollusk'), N_('albatross'), N_('rat'), N_('undefined')]
print _('mollusk') +  ' normal print'
e = _('albatross') +  ' Variable e'
print e
for a in f:
    print _(a) + str(' for a in f')

#---------------------------------------------------------------------------------- Variablen
#day_in_seconds = 86400  #Anzahl der Sek. in einem Tag
day_in_seconds = 1  #zum testen ein Tag vergeht in einer Sekunde
logspacer = "\n"+ "***********************************************"

######################################################### Hauptprogramm
########################################################################################################################
write_verbose(logspacer, False, True)
logstring = "\n" + _('Die Klima-Werte werden nun vom automatischen Programm "%s" gesteuert') % (hangingtable)
write_verbose(logstring, False, True)

#---------------------------------------------------------------------------------- Auslesen der gesammten csv-Datei
csv_file = open(csv_path + csv_file,"rb")   # Variable csv_file = csv-Datei oeffnen
csv_file_reader = csv.DictReader(csv_file)  # reader-Objekt liest csv in Dictionary ein
row_number = 0                              # Setzt Variable row_number auf 0
total_duration = 0                          # Setzt Variable duration auf 0

for row in csv_file_reader:
    # print 'DEBUG' + str(row)
    total_duration += int(row["days"])                           # errechnet die Gesamtdauer
    build_dictionary = "dictionary%d = %s"%  (row_number,row)   # baut pro Zeile ein Dictionary
    exec(build_dictionary)                                      # baut pro Zeile das jeweilige Dictionary
    
    row_number += 1                                             # Zeilenanzahl wird hochgezählt (für Dictionary Nummer und total_periods)
    # print 'DEBUG ' + str(total_duration)

total_periods = row_number - 1                                    # Variable total_periods = Anzahl der Perioden (0 basiert!), der Reifephasen (entspricht der Anzahl an Reihen)
# print 'DEBUG ' + str(total_periods)
csv_file.close()
#---------------------------------------------------------------------------------- Lesen der Werte aus der CSV-Datei & Schreiben der Werte in die Konsole und das Logfile
period = 0              # setzt periodenzähler zurück
actual_dictionary = ""  # setzt aktuelles Dictionary zurück

while period <= total_periods:
    # print 'DEBUG period : ' + str(period)
    # print 'DEBUG total_periods : ' + str(total_periods)
    exec('%s = %s') % ("actual_dictionary", "dictionary" + str(period))
    # print 'DEBUG actual_dictionary : ' + str(actual_dictionary)
    if period == 0:
        logstring = time.strftime('%d.%m.%Y - %H:%M Uhr') + _(': Startwerte Periode 1 von %s') % (str(total_periods + 1)) + '\n'  
        write_verbose(logstring, False, True)
        finaltime = datetime.datetime.now() + timedelta(days = total_duration)  # days = parameter von timedelta
        read_dictionary(actual_dictionary)
        logstring = _("Nächste Änderung der Werte: %s") % (period_endtime.strftime('%d.%m.%Y  %H:%M'))
        write_verbose(logstring, False, True)
        logstring = _("Programmende: %s") % (finaltime.strftime('%d.%m.%Y  %H:%M'))
        write_verbose(logstring, False, True)
        
    elif period == total_periods:
        logstring = time.strftime('%d.%m.%Y - %H:%M') + _(' Uhr: Neue Werte für Periode %s von %s') % (str(period + 1), str(total_periods + 1))
        write_verbose(logstring, False, True)
        read_dictionary(actual_dictionary)
        logstring = '\n' + _('Programm "%s " beendet die Kontrolle.') % (hangingtable) + '\n' + _('Der Reifeschrank funktioniert weiter mit den letzten Werten.')
        write_verbose(logstring, False, True)
        
    else:
        logstring = time.strftime('%d.%m.%Y - %H:%M') + _(' Uhr: Neue Werte für Periode %s von %s') % (str(period + 1), str(total_periods + 1))
        write_verbose(logstring, False, True)
        read_dictionary(actual_dictionary)
        logstring = _("Nächste Änderung der Werte: %s") % (period_endtime.strftime('%d.%m.%Y  %H:%M'))
        write_verbose(logstring, False, True)
        logstring = _("Programmende: %s") % (finaltime.strftime('%d.%m.%Y  %H:%M'))
        write_verbose(logstring, False, True)
    period += 1
    write_verbose(logspacer, False, True)
    if period <= total_periods:
        time.sleep(duration_sleep)       # Wartezeit bis zur nächsten Periode
sys.exit(0)