import pydicom
import datetime
from tkinter import *
import tkinter.messagebox
from tkinter import filedialog


# Main windows setup
mainWindow = Tk()  # Links main window to the interpreter
mainWindow.title("Cubes_ReadEasy by Kamil_Sokolowski")
mainWindow.geometry("505x285+100+100")  # Window size and initial position
mainWindow['bg'] = 'gray98'  # Background colour

# Main text area
textArea = Text(mainWindow, width=59, height=14, borderwidth=2, bg='old lace', font='Menlo')
textArea.place(x=10, y=55)

# Displays ASCII art in the text window
textArea.insert(END, '\n\n\n\t\t   +------+         +------+  \n\t\t  /|     /|        /|     /|\n\t\t'
                         ' +-+----+ |       +-+----+ |\n\t\t | |    | |       | |    | |\n\t\t | +----+-+       '
                         '| +----+-+\n\t\t |/     |/        |/     |/\n\t\t +------+         +------+  ')

Label(mainWindow, text="Open Molecubes dicom \nor reconparams file", bg='gray98', font='Menlo').place(x=180, y=7)

def openLogFileAndProcess():
    '''Main program that runs with an open GUI'''

    textArea.delete("1.0", "end")

    # Select log file
    importedFile = filedialog.askopenfilename(initialdir="~/Desktop",title="Open Log file")

    # Determines filetype and passes it onto appropriate function.
    if importedFile.endswith('.txt'):
        determineLog(importedFile)
    elif importedFile.endswith('.dcm'):
        determineDicom(importedFile)
    else:
        textArea.insert(END, 'Not a valid file format')


def determineDicom(importedFile):
    """ Determines whether the Dicom file is PET, CT or invalid"""

    dicom_info = pydicom.dcmread(importedFile)

    # Different file types passes to one of two functions.
    if dicom_info.Modality == 'CT':
        textArea.insert(END, 'CT Dicom file:\n')
        CTdicom(importedFile)
    elif dicom_info.Modality == 'PT':
        textArea.insert(END, 'PET Dicom file:\n')
        PETdicom(importedFile)
    else:
        textArea.insert(END, 'Not a Dicom or reconstruction parameter log file\n')


def determineLog(importedFile):
    """Determines whether the Log file is PET, CT or invalid"""

    parametersDict = {}  # New dictionary holding data from log file.

    # Opens and parses the data from log file
    with open(importedFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    # Different file types passed to one of two functions.
    if 'Acquisition/isotope ' in parametersDict:
        textArea.insert(END, 'PET reconstruction parameter file:\n')
        PETlog(importedFile)
    elif parametersDict.get('Acquisition/modality ') == 'CT':
        textArea.insert(END, 'CT reconstruction parameter file:\n')
        CTlog(importedFile)
    else:
        textArea.insert(END, 'Not a Dicom or reconstruction parameter log file\n')


def CTlog(importedFile):
    """Processes CT Log file and outputs data in text window. """

    parametersDict = {}  # New dictionary holding data from log file.
    studyInfo = []  # List for creation of file name.

    # Opens and parses the data from log file
    with open(importedFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    # Parses information from log file to generate a filename.
    studyInfo.append(parametersDict.get('General/principalinvestigator '))
    studyInfo.append(parametersDict.get('General/study '))
    studyInfo.append(parametersDict.get('General/series '))
    studyInfo.append(parametersDict.get('General/patient '))
    textArea.insert(END, '\nStudy Info: \t\t\t' + str("/".join(studyInfo)))

    # Outputs voxel size in human readable format.
    if parametersDict.get('Reconstruction/voxelsizeX ') == '0.2':
        textArea.insert(END, '\nVoxel Size: \t\t\t200um')
    elif parametersDict.get('Reconstruction/voxelsizeX ') == '0.1':
        textArea.insert(END, '\nVoxel Size: \t\t\t100um')
    elif parametersDict.get('Reconstruction/voxelsizeX ') == '0.05':
        textArea.insert(END, '\nVoxel Size: \t\t\t50um')
    else:
        textArea.insert(END, '\nINVALID VOXEL SIZE')

    # Parses important information from log file and outputs in text window.
    textArea.insert(END, '\nVoltage: \t\t\t' + parametersDict.get('Acquisition/kVp ') + 'kV')
    textArea.insert(END, '\nCurrent: \t\t\t' + parametersDict.get('Acquisition/muA ') + 'uA')
    textArea.insert(END, '\nExposure: \t\t\t' + parametersDict.get('Acquisition/exposure ') + 'ms')
    textArea.insert(END, '\nModality: \t\t\t' + parametersDict.get('Acquisition/modality '))
    textArea.insert(END, '\nProtocol: \t\t\t' + parametersDict.get('General/protocol ').capitalize())
    textArea.insert(END, '\nNoise Reduction: \t\t\t' + parametersDict.get('NoiseRegularization/factor '))
    textArea.insert(END, "\nExposures #'s: \t\t\t" + parametersDict.get('Acquisition/nr_exposures '))
    textArea.insert(END, '\nAcquisition Type: \t\t\t' + (parametersDict.get('Acquisition/scan_type ')).capitalize())
    textArea.insert(END, '\nRecon. Algorithm: \t\t\t' + parametersDict.get('Reconstruction/algorithm '))
    textArea.insert(END, '\nSoftware Ver: \t\t\t' + parametersDict.get('Acquisition/version '))


def CTdicom(importedFile):
    """Processes CT dicom file and outputs data in text window. """

    dicom_info = pydicom.dcmread(importedFile)

    # Outputs voxel size in human readable format.
    if dicom_info.SliceThickness == 0.2:
        voxelSize = '200um'
    elif dicom_info.SliceThickness == 0.1:
        voxelSize = '100um'
    elif dicom_info.SliceThickness == 0.05:
        voxelSize = '50um'
    else:
        voxelSize = 'INVALID VOXEL SIZE'


    # Parse concatenated dicom date/time information and output in human readable format
    newDate = ['']
    dateTimeInfo = dicom_info.AcquisitionDateTime
    newDate.append(dateTimeInfo[0:4])
    newDate.append(dateTimeInfo[4:6])
    newDate.append(dateTimeInfo[6:8])
    newDate.append(dateTimeInfo[8:10])
    newDate.append(dateTimeInfo[10:12])
    newDate.append(dateTimeInfo[12:14])
    newDate.remove('')
    finalDate = "-".join(newDate)
    date_time_obj = datetime.datetime.strptime(finalDate, '%Y-%m-%d-%H-%M-%S')

    # Parses important information from log file and outputs in text window.
    textArea.insert(END, '\nDate & Time: \t\t' + '{:%d %B %Y @ %I:%M%p}'.format(date_time_obj))
    textArea.insert(END, '\nStudy Info: \t\t' + str(dicom_info.PatientName) + '/' + str(dicom_info.PatientID))
    textArea.insert(END, '\nVoxel Size:  \t\t' + voxelSize)
    textArea.insert(END, '\nVoltage: \t\t' + str(dicom_info.SharedFunctionalGroupsSequence[0].CTXRayDetailsSequence[0].KVP) + 'kV')
    textArea.insert(END, '\nModality: \t\t' + dicom_info.Modality)
    textArea.insert(END, '\nAcq. Type: \t\t' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTAcquisitionTypeSequence[0].AcquisitionType).capitalize())
    textArea.insert(END, '\nRecon. Alg.: \t\t' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTReconstructionSequence[0].ReconstructionAlgorithm).capitalize())
    textArea.insert(END, '\nSoftware Ver: \t\t' + dicom_info.SoftwareVersions)


def PETlog(importedFile):
    """Processes PET log file and outputs data in text window. """

    parametersDict = {}  # New dictionary holding data from log file.
    studyInfo = []  # List for combining scan information into one output.

    # Opens and parses the data from log file into a searchable dictionary.
    with open(importedFile, 'r') as textInput:
        for line in textInput:
            for i in line:
                position = line.find('=')
                parametersDict[line[:position]] = (line[position + 1:]).strip()

    # Parses information from log file to generate a filename.
    studyInfo.append(parametersDict.get('General/principalinvestigator '))
    studyInfo.append(parametersDict.get('General/study '))
    studyInfo.append(parametersDict.get('General/series '))
    studyInfo.append(parametersDict.get('General/patient '))
    textArea.insert(END, '\nStudy Info: \t\t\t' + str("/".join(studyInfo)))

    # Outputs voxel size in human readable format.
    textArea.insert(END, '\nModality: \t\t\tPET')
    textArea.insert(END, '\nIsotope: \t\t\t' + parametersDict.get('Acquisition/isotope '))
    if (parametersDict.get('Reconstruction/voxel_size ')) == '0.400000':
        textArea.insert(END, '\nVoxel size: \t\t\t400um')
    elif (parametersDict.get('Reconstruction/voxel_size ')) == '0.800000':
        textArea.insert(END, '\nVoxel size: \t\t\t800um')
    else:
        print()
        textArea.insert(END, '\nINVALID VOXEL SIZE')

    # Parses important information from log file and outputs in text window.
    textArea.insert(END, '\nScan Duration: \t\t\t' + str(int(int(parametersDict.get('Acquisition/duration ')) / 60)) + 'min')
    textArea.insert(END, '\nProtocol: \t\t\t' + (parametersDict.get('General/protocol ')).capitalize())
    textArea.insert(END, '\nNoise Reduction: \t\t\t' + parametersDict.get('NoiseRegularization/factor '))
    textArea.insert(END, '\nSoftware Ver: \t\t\t' + parametersDict.get('Acquisition/version '))


def PETdicom(importedFile):
    """Processes PET dicom file and outputs data in text window. """

    dicom_info = pydicom.dcmread(importedFile)

    # Reads Voxel Size
    voxelSize = ''
    if dicom_info.SliceThickness == 0.4:
        voxelSize = '400um'
    elif dicom_info.SliceThickness == 0.8:
        voxelSize = '800um'
    else:
        voxelSize = 'Voxel size not valid'

    # Parse concatenated dicom date/time information and output in human readable format
    newDate = ['']
    dateTimeInfo = dicom_info.AcquisitionDateTime
    newDate.append(dateTimeInfo[0:4])
    newDate.append(dateTimeInfo[4:6])
    newDate.append(dateTimeInfo[6:8])
    newDate.append(dateTimeInfo[8:10])
    newDate.append(dateTimeInfo[10:12])
    newDate.append(dateTimeInfo[12:14])
    newDate.remove('')
    finalDate = "-".join(newDate)
    date_time_obj = datetime.datetime.strptime(finalDate, '%Y-%m-%d-%H-%M-%S')

    # Parses important information from log file and outputs in text window.
    textArea.insert(END, '\nDate & Time: \t\t' + '{:%d %B %Y @ %I:%M%p}'.format(date_time_obj))
    textArea.insert(END, '\nStudy Info: \t\t' + str(dicom_info.PatientName) + '/' + str(dicom_info.PatientID))
    textArea.insert(END, '\nVoxel Size:  \t\t' + voxelSize)
    textArea.insert(END, '\nModality: \t\t' + dicom_info.Modality)
    textArea.insert(END, '\nAtt. Correct: \t\t' + (dicom_info.AttenuationCorrected).capitalize())
    textArea.insert(END, '\nAcq. Duration: \t' + str(int((dicom_info.AcquisitionDuration)/60)) + ' minutes')
    (dicom_info.RadiopharmaceuticalInformationSequence[0].RadionuclideCodeSequence[0].CodeMeaning).replace('^', '')
    textArea.insert(END,'\nIsotope: \t\t' + str(
        (dicom_info.RadiopharmaceuticalInformationSequence[0].RadionuclideCodeSequence[0].CodeMeaning).replace('^',
                                                                                                              '')))
    textArea.insert(END, '\nSoftware Ver: \t\t' + dicom_info.SoftwareVersions)

def aboutInformation():
    """Displays information about the program in a pop up box"""

    tkinter.messagebox.showinfo('Information', 'Cubes_ReadEasy\n\nVersion 1.0\n\n20th May 2021\n\n'
                                               'Cubes_ReadEasy parses useful information from Molecubes dicom '
                                               'and reconstruction parameter files.\n\nCopyright (c) 2021 Kamil '
                                               'Sokolowski\n\n'
                                               'Any suggestion or features you would like added?\nEmail me :'
                                               'thatKamil@pm.me\n\nSource code & license (MIT) available at:\n'
                                               'https://github.com/thatKamil/Cubes_ReadEasy')

def useInformation():
    """Display information on how to use the program in a pop-up box"""

    tkinter.messagebox.showinfo('Use Guide', "-=Use Guide=-\n\n"
                                             "The program can process any Molecubes PET or CT dicom file, as well as the "
                                             "'reconparams' file located in the original reconstruction folder.\n\n"
                                             "Start the Cubes_ReadEasy program and click 'Open File'.\n"
                                             "Select file to be opened."
                                             "\n\nInfo in the text area can be copied to a seperate file.")

# GUI buttons
Button(mainWindow, text="Open File", command=openLogFileAndProcess, height=2, width=12,
       bg='snow', font='menlo').place(x=12, y=4)
Button(mainWindow, text="About", command=aboutInformation, height=1, width=10,
       bg='snow', font='menlo').place(x=387, y=0)
Button(mainWindow, text="Use Guide", command=useInformation, height=1, width=10,
       bg='snow', font='menlo').place(x=387, y=26)

mainWindow.mainloop()