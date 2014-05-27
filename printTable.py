#! /usr/bin/python

import sys
import os
import commands
import re


# for the options
import optparse
parser = optparse.OptionParser()

# define the options
parser.add_option('-t', '--tunes',
                  help='specify the tunes values separated by comma -t 4.17,4.23',
                  dest='TUNES',
                  action='store')


# get the options
(opts, args) = parser.parse_args()


# Sanity check: Making sure all mandatory options appeared
mandatories = ['TUNES']
for m in mandatories:
    if not opts.__dict__[m]:
        print "at least the mandatory option %s is missing\n" % m
        parser.print_help()
        exit(-1)

# tunes
tunes = opts.TUNES.split(",")
tunes_h = tunes[0]
tunes_v = tunes[1]


configuration = []
kicker_corr = []

def print_kicker(table,coord_type,pos):
    header = "\n\nCorr. Type"
    for l in reversed(configuration):
        header += " & %s" % l
    header += " \\\\ \\hline"

    print header

    for k in kicker_corr:

        #print k
        table_line = '%s & %s_%s' % (k,coord_type,pos)
        #print table_line
        
        for l in reversed(configuration):
            for v in table[l][k].keys():

                a_match = re.match( r'(%s_%s)'%(coord_type,pos), v)
                if (a_match != None):

                    value = float( table[l][k][v] )/0.001
                    #print k,l,v,table[l][k][v],value
                    table_line += ' & %4.3f' % value

        table_line += '\\\\ \\hline'

        #print table_line
        # match_any_digit = re.match( r'.*&.*[\d].*.&.*', table_line)
        match_any_digit = re.match( r'.*&.*[\d].*', table_line)
        
        if (match_any_digit):
            print table_line



def print_matrix(table,coord_type,pos):

    scale_defl_over_curr = 0.113
    
    header = "\n\nCorr. Type"
    for l in reversed(configuration):
        header += " & %s" % l
    header += " \\\\ \\hline"

    print header

    for k in kicker_corr:

        #print k
        table_line = '%s & %s_%s' % (k,coord_type,pos)
        #print table_line
        
        for l in reversed(configuration):
            for v in table[l][k].keys():

                a_match = re.match( r'(%s_%s)'%(coord_type,pos), v)
                if (a_match != None):

                    value = float( table[l][k][v] )/0.001
                    value *= scale_defl_over_curr
                    #print k,l,v,table[l][k][v],value
                    table_line += ' & %4.4f' % value

        table_line += '\\\\ \\hline'

        #print table_line
        # match_any_digit = re.match( r'.*&.*[\d].*.&.*', table_line)
        match_any_digit = re.match( r'.*&.*[\d].*', table_line)
        
        if (match_any_digit):
            print table_line



list_of_logfiles = commands.getoutput('ls madx/log | grep %s | grep %s' %(tunes_h,tunes_v) ).split()

if (len(list_of_logfiles) == 0):
    print "no logfile found, exiting..."
    sys.exit()


for logfile in list_of_logfiles:

    # print logfile.split("_")
    layout = logfile.split("_")[4].split(".")[0]
    kicker = logfile.split("_")[3].split("at")[0].replace('k','')
    
    if layout not in configuration:
        configuration.append(layout)

    if kicker not in kicker_corr:
        kicker_corr.append(kicker)

# print configuration
# print kicker_corr


table ={}

for logfile in list_of_logfiles:

    filename = 'madx/log/'+logfile
    # print logfile

    layout = logfile.split("_")[4].split(".")[0]
    kicker = logfile.split("_")[3].split("at")[0].replace('k','')

    # print layout, kicker
    
    if layout not in table.keys():
        table[layout] = {}

    if kicker not in table[layout].keys():
        table[layout][kicker] = {}


    infile = open(filename)
    for line in infile:

        # print line
        a_match = re.match( r'(.*sept_.*)([?\- ][\d]\.[\d]+)',line)
        if (a_match != None):
            var= a_match.group(1).replace(" =","").replace(' ','')
            value=a_match.group(2).replace(' ','') 

            
            #print logfile
            #print layout
            #print kicker
            
            #print a_match.group()
            #print var
            #print value
                
            table[layout][kicker][var] = value



#print table
#print_kicker(table,'xsept','center')
# print_kicker(table,'pxsept','center')
# print_kicker(table,'ysept','center')
# print_kicker(table,'pysept','center')

print '\n\n-----------------------------------------------------\n'

print ('TUNES: Qh=%s, Qv=%s' % (tunes_h, tunes_v) )
print_kicker(table,'xsept','start')
print_kicker(table,'pxsept','start')
print_kicker(table,'ysept','start')
print_kicker(table,'pysept','start')


print ('\n\nMATRIX CONVERSION: Qh=%s, Qv=%s' % (tunes_h, tunes_v) )
print_matrix(table,'xsept','start')
print_matrix(table,'pxsept','start')
print_matrix(table,'ysept','start')
print_matrix(table,'pysept','start')


