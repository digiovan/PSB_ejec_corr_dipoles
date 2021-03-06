#! /usr/bin/python

"""

Simple script to create a madx file for the study of the extraction matrix,
based on the template, psb_orbit_TEMPLATE.madx

EXAMPLE: python createMadxFile.py -r 3 -f ../psb.seq -k DHZ4L1 -v 0.001 

OUTPUT: a madx file called psb_orbit_kBE3DHZ4L1at0p001rad_l2014.madx

"""


import sys
import os
import commands

# for the options
import optparse
parser = optparse.OptionParser()

# define the options
parser.add_option('-r', '--ring',
                  help='specify which ring of the PSB',
                  dest='RING',
                  action='store')

parser.add_option('-f', '--seq_file',
                  help='specify the MADX sequence',
                  dest='SEQFILE',
                  action='store')

parser.add_option('-k', '--kicker',
                  help='specify the kicker name',
                  dest='KICKER_NAME',
                  action='store')

parser.add_option('-v', '--kicker_value',
                  help='specify the kicker value in rad',
                  dest='KICKER_VALUE',
                  action='store')

parser.add_option('-t', '--tunes',
                  help='specify the tunes values separated by comma -t 4.17,4.23',
                  dest='TUNES',
                  action='store')


# get the options
(opts, args) = parser.parse_args()


# Sanity check: Making sure all mandatory options appeared
mandatories = ['RING','SEQFILE','KICKER_NAME','KICKER_VALUE']
for m in mandatories:
    if not opts.__dict__[m]:
        print "at least the mandatory option %s is missing\n" % m
        parser.print_help()
        exit(-1)

# default tunes
tunes_h = '4.172'
tunes_v = '5.230'

if opts.__dict__['TUNES']:
    new_tunes = opts.TUNES.split(",")
    tunes_h = new_tunes[0]
    tunes_v = new_tunes[1]

# print "The Tunes are Qh=%s, Qv=%s" % (tunes_h, tunes_v)

# standard variables
outfolder = '../output/'

# know your current directory
PWD = os.getcwd()


var_to_change = {}

var_to_change['TUNES_H'] = tunes_h
var_to_change['TUNES_V'] = tunes_v
var_to_change['RING'] = opts.RING
var_to_change['PSBSEQ'] = 'psb' + var_to_change['RING']
var_to_change['SEQFILE'] = opts.SEQFILE
var_to_change['KICKER_NAME'] = 'BE' + opts.RING + '.' + opts.KICKER_NAME
var_to_change['KICKER_VALUE'] = opts.KICKER_VALUE
var_to_change['KICKER_STRENGTH'] = 'k' + var_to_change['KICKER_NAME'].replace(".","")

ext = var_to_change['KICKER_STRENGTH'] + 'at' + var_to_change['KICKER_VALUE'].replace(".","p") + 'rad'
ext2 = 'l2014'

if ('2009' in var_to_change['SEQFILE']):
    ext2 = 'l2009'
if ('expfromnote' in var_to_change['SEQFILE']):
    ext2 = 'lexpfromnote' # layout as expected from PS/OP/Note 99-xx, never published...

if ('geode' in var_to_change['SEQFILE']):
    ext2 += 'geodeSMH15L1'

if ('tobias' in var_to_change['SEQFILE']):
    ext2 += 'tobias'

var_to_change['MATCH_ORBIT_FILENAME'] = outfolder + 'match_orbit_MUX4p172_MUY5p230_' +  ext + '_' + ext2 + '.prt'
var_to_change['OUTPUT_TWISS'] = outfolder + 'twiss/psb_orbit_' +  ext + '_' + ext2 + '.twiss'
var_to_change['OUTPUT_PLOT']  = outfolder +    'ps/psb_orbit_' +  ext + '_' + ext2 
var_to_change['OUTPUT_GEOM']  = outfolder +  'geom/geom_rel_'  +  ext + '_' + ext2 + '.txt'
                                                                                                                              
# debug
# for item in var_to_change.keys():
#     print item, var_to_change[item]



# modify the template script
infile_name = ''
if ('DHZ' in var_to_change['KICKER_NAME']):
    infile_name = '%s/templates/psb_orbit_DHZ_TEMPLATE.madx' % PWD
if ('DVT' in var_to_change['KICKER_NAME']):
    infile_name = '%s/templates/psb_orbit_DVT_TEMPLATE.madx' % PWD

infile  = open('%s' % infile_name)


madx_filename = 'psb_orbit_%s_%s_tunes_%s_%s.madx' % (ext, ext2, tunes_h, tunes_v) 
outfile = open('%s/%s' % (PWD, madx_filename), 'w')


print ' echo \'madx32 < %s >& log/log_%s\'' % (madx_filename, madx_filename)
print ' madx32 < %s >& log/log_%s\n' % (madx_filename, madx_filename)


for line in infile:
    
    newline = line
    for item in var_to_change.keys():
        # print item, var_to_change[item]
        newline = newline.replace( item, var_to_change[item] )

    # print 'newline:  %s' % newline      
    outfile.write(newline)

infile.close()
outfile.close()

