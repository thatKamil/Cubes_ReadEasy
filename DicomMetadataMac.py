import os
import pydicom

consoleSize = 'mode 40,6'
os.system(consoleSize)

# Drag drop functionality in Windows
importedFile = sys.argv[1]

# Open Dicom with python dicom package
dicomInfo = pydicom.dcmread(importedFile)

# Create text file output naming structure
dicomDateTime = dicomInfo.AcquisitionDateTime
outputName = 'Dicom_Metadata_'
dateTimeOutput = dicomDateTime[0:4] + '-' + dicomDateTime[4:6] + '-' + dicomDateTime[6:8] + '_' + dicomDateTime[8:12]

# Initial Pydicom output not a string
info = str(dicomInfo)

# Writes text file
with open("{0}{1}.txt".format(outputName, dateTimeOutput), 'w') as f:
    for i in info:
        f.write(i)

print('\nDICOM metadata output created for: \n' + str(dicomInfo.PatientName) + '\n')

input('Press enter key to close program')