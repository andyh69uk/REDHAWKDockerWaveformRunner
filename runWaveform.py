#!/usr/bin/python

import sys, getopt
from ossie import parsers
from ossie.utils import sb
def main(argv):
   sadfile = ''
   inputfile = ''
   dataformat = ''
   samplerate = ''
   iscomplex = False
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hs:i:f:r:co:",["sadfile=","ifile=","dataformat=","samplerate=","complex","ofile="])
   except getopt.GetoptError:
      print 'runWaveform.py -s <sadfile> -i <inputfile> -f <dataFormat> -r <sampleRate> -c -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      #print 'evaluating opt - ',opt,' arg - ',arg
      if opt == '-h':
         print 'runWaveform.py -s <sadfile> -i <inputfile> -f <dataFormat> -r <sampleRate> -c o <outputfile>'
         sys.exit()
      elif opt in ("-s", "--sadfile"):
         sadfile = arg
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-f", "--dataformat"):
         dataformat = arg
      elif opt in ("-r", "--samplerate"):
         samplerate = arg
      elif opt in ("-c", "--complex"):
         iscomplex = True
      elif opt in ("-o", "--ofile"):
         outputfile = arg
         print 'setting outputfile',outputfile
   print 'Processing ', inputfile, " through waveform - ", sadfile
   sadFile = open(sadfile)
   sadFileString = sadFile.read()
   usesPort = ''
   usesComponent = ''
   providesPort = ''
   providesComponent = ''
   sadXML = parsers.sad.parseString(sadFileString)
   if sadXML.get_externalports():
      for port in sadXML.get_externalports().get_port():
         if port.get_usesidentifier():
            usesPort = port.get_usesidentifier()
            usesComponent = port.get_componentinstantiationref()
         elif port.get_providesidentifier():
            providesPort = port.get_providesidentifier()
            providesComponent = port.get_componentinstantiationref()
      if not usesPort and not providesPort:
         print 'Need uses and provides external ports'
         sys.exit()
   else:
      print 'No external ports'
      sys.exit()
   print usesPort,providesPort
   if not usesPort or not providesPort:
      print 'Require external uses & provides port'
      sys.exit()
   sb.loadSADFile(sadfile)
   fileSource = sb.FileSource(filename=inputfile,dataFormat=dataformat,sampleRate=samplerate)
   fileSink = sb.FileSink(filename=outputfile)
   #FIXME check file type matches external port
   fileSource.connect(sb.getComponent(providesComponent.get_refid()),providesPortName=providesPort)
   sb.getComponent(usesComponent.get_refid()).connect(fileSink,usesPortName=usesPort)
   sb.start()
   fileSink.waitForEOS()
   sb.stop()
   sb.release()

if __name__ == "__main__":
   main(sys.argv[1:])
