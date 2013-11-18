#Debug test for memory usage

import debugMem

outFile = open('/home/pbeeson/objdump','w')
debugMem.dumpObjects(outFile)

