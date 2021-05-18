from tkinter import *
import pydicom
import datetime

importedLogFile = sys.argv[1]

def CTlog(importedLogFile):
    parametersDict = {}  # New dictionary holding data from log file.
    studyInfo = []

    # Opens and parses the data from log file
    with open(importedLogFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    studyInfo.append(parametersDict.get('General/principalinvestigator '))
    studyInfo.append(parametersDict.get('General/study '))
    studyInfo.append(parametersDict.get('General/series '))
    studyInfo.append(parametersDict.get('General/patient '))
    print('\nStudy Info: \t\t' + str("/".join(studyInfo)))

    if parametersDict.get('Reconstruction/voxelsizeX ') == '0.2':
        print('Voxel Size: \t\t200um')
    elif parametersDict.get('Reconstruction/voxelsizeX ') == '0.1':
        print('Voxel Size: \t\t100um')
    elif parametersDict.get('Reconstruction/voxelsizeX ') == '0.05':
        print('Voxel Size: \t\t50um')
    else:
        print('INVALID VOXEL SIZE')

    print('Voltage: \t\t' + parametersDict.get('Acquisition/kVp ') + 'kV')
    print('Current: \t\t' + parametersDict.get('Acquisition/muA ') + 'uA')
    print('Exposure: \t\t' + parametersDict.get('Acquisition/exposure ') + 'ms')
    print('Modality: \t\t' + parametersDict.get('Acquisition/modality '))
    print('Protocol: \t\t' + parametersDict.get('General/protocol ').capitalize())
    print('Noise Reduction: \t' + parametersDict.get('NoiseRegularization/factor '))
    print("Exposures #'s: \t\t" + parametersDict.get('Acquisition/nr_exposures '))
    print('Acquisition Type: \t' + (parametersDict.get('Acquisition/scan_type ')).capitalize())
    print('Recon. Algorithm: \t' + parametersDict.get('Reconstruction/algorithm '))
    print('Software Ver: \t\t' + parametersDict.get('Acquisition/version '))

def CTdicom(importedLogFile):
    dicom_info = pydicom.dcmread(importedLogFile)
    # Reads Voxel Size
    voxelSize = ''
    if dicom_info.SliceThickness == 0.2:
        voxelSize = '200um'
    elif dicom_info.SliceThickness == 0.1:
        voxelSize = '100um'
    elif dicom_info.SliceThickness == 0.05:
        voxelSize = '50um'
    else:
        voxelSize = 'INVALID VOXEL SIZE'


    # Parse concatenated dicom date/time information and output in human readable format
    dateTimeInfo = dicom_info.AcquisitionDateTime

    newDate = ['']
    newDate.append(dateTimeInfo[0:4])
    newDate.append(dateTimeInfo[4:6])
    newDate.append(dateTimeInfo[6:8])
    newDate.append(dateTimeInfo[8:10])
    newDate.append(dateTimeInfo[10:12])
    newDate.append(dateTimeInfo[12:14])
    newDate.remove('')

    finalDate = "-".join(newDate)

    date_time_obj = datetime.datetime.strptime(finalDate, '%Y-%m-%d-%H-%M-%S')

    print('\nDate & Time: \t\t' + '{:%d %B %Y @ %I:%M%p}'.format(date_time_obj))
    print('Study Info: \t\t' + str(dicom_info.PatientName) + ' / ' + str(dicom_info.PatientID))
    print('Voxel Size:  \t\t' + voxelSize)
    print('Voltage: \t\t' + str(dicom_info.SharedFunctionalGroupsSequence[0].CTXRayDetailsSequence[0].KVP) + 'kV')
    print('Modality: \t\t' + dicom_info.Modality)
    print('Acq. Type: \t\t' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTAcquisitionTypeSequence[0].AcquisitionType).capitalize())
    print('Recon. Algorithm: \t' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTReconstructionSequence[0].ReconstructionAlgorithm).capitalize())
    print('Software Ver: \t\t' + dicom_info.SoftwareVersions)

def PETlog(importedLogFile):
    parametersDict = {}  # New dictionary holding data from log file.
    studyInfo = []  # List for combining scan information into one output.

    # Opens and parses the data from log file into a searchable dictionary.
    with open(importedLogFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    studyInfo.append(parametersDict.get('General/principalinvestigator '))
    studyInfo.append(parametersDict.get('General/study '))
    studyInfo.append(parametersDict.get('General/series '))
    studyInfo.append(parametersDict.get('General/patient '))
    print('\nStudy Info: \t\t' + str("/".join(studyInfo)))

    print('Modality: \t\tPET')
    print('Isotope: \t\t' + parametersDict.get('Acquisition/isotope '))
    if (parametersDict.get('Reconstruction/voxel_size ')) == '0.400000':
        print('Voxel size: \t\t400um')
    elif (parametersDict.get('Reconstruction/voxel_size ')) == '0.800000':
        print('Voxel size: \t\t800um')
    else:
        print('INVALID VOXEL SIZE')
    print('Scan Duration: \t\t' + str(int(int(parametersDict.get('Acquisition/duration ')) / 60)) + 'min')
    print('Protocol: \t\t' + (parametersDict.get('General/protocol ')).capitalize())
    print('Noise Reduction: \t' + parametersDict.get('NoiseRegularization/factor '))
    print('Software Ver: \t\t' + parametersDict.get('Acquisition/version '))

def PETdicom(importedLogFile):
    dicom_info = pydicom.dcmread(importedLogFile)

    # Reads Voxel Size
    voxelSize = ''
    if dicom_info.SliceThickness == 0.4:
        voxelSize = '400um'
    elif dicom_info.SliceThickness == 0.8:
        voxelSize = '800um'
    else:
        voxelSize = 'Voxel size not valid'

    # Parse concatenated dicom date/time information and output in human readable format
    dateTimeInfo = dicom_info.AcquisitionDateTime

    newDate = ['']
    newDate.append(dateTimeInfo[0:4])
    newDate.append(dateTimeInfo[4:6])
    newDate.append(dateTimeInfo[6:8])
    newDate.append(dateTimeInfo[8:10])
    newDate.append(dateTimeInfo[10:12])
    newDate.append(dateTimeInfo[12:14])
    newDate.remove('')

    finalDate = "-".join(newDate)

    date_time_obj = datetime.datetime.strptime(finalDate, '%Y-%m-%d-%H-%M-%S')

    print('\nDate & Time: \t\t' + '{:%d %B %Y @ %I:%M%p}'.format(date_time_obj))
    print('Study Info: \t\t' + str(dicom_info.PatientName) + ' / ' + str(dicom_info.PatientID))
    print('Voxel Size:  \t\t' + voxelSize)
    print('Modality: \t\t' + dicom_info.Modality)
    print('Software Ver: \t\t' + dicom_info.SoftwareVersions)
    print('Acq. Duration: \t\t' + str(int((dicom_info.AcquisitionDuration)/60)) + ' minutes')
    print('Att. Corrected: \t' + (dicom_info.AttenuationCorrected).capitalize())

    (dicom_info.RadiopharmaceuticalInformationSequence[0].RadionuclideCodeSequence[0].CodeMeaning).replace('^', '')

    print('Isotope: \t\t' + str(
        (dicom_info.RadiopharmaceuticalInformationSequence[0].RadionuclideCodeSequence[0].CodeMeaning).replace('^',
                                                                                                               '')))

def determineDicom(importedLogFile):
    dicom_info = pydicom.dcmread(importedLogFile)

    if dicom_info.Modality == 'CT':
        print('Reading CT Dicom file:')
        CTdicom(importedLogFile)
    elif dicom_info.Modality == 'PT':
        print('Reading PET Dicom file:')
        PETdicom(importedLogFile)
    else:
        print('Not a Dicom or reconstruction parameter log file')

def determineLog(importedLogFile):
    parametersDict = {}  # New dictionary holding data from log file.

    # Opens and parses the data from log file
    with open(importedLogFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    if 'Acquisition/isotope ' in parametersDict:
        print('Reading PET reconstruction parameter file:')
        PETlog(importedLogFile)
    elif parametersDict.get('Acquisition/modality ') == 'CT':
        print('Reading CT reconstruction parameter file:')
        CTlog(importedLogFile)
    else:
        print('Not a Dicom or reconstruction parameter log file')


if importedLogFile.endswith('.txt'):
    determineLog(importedLogFile)
elif importedLogFile.endswith('.dcm'):
    determineDicom(importedLogFile)
else:
    print('Not a valid file format')

input('\nPress enter key to close program')