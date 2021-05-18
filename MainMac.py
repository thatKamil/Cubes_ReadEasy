import pydicom
import datetime
from tkinter import *
from tkinter import filedialog

# Main windows setup
mainWindow = Tk()  # Links main window to the interpreter
mainWindow.title("Molecubes_ReadEasy by Kamil_Sokolowski")
mainWindow.geometry("400x400+300+200")  # Window size and initial position
mainWindow['bg'] = 'gray98'  # Background colour

# Main text area
textArea = Text(mainWindow, width=46, height=17, borderwidth=2, bg='old lace')
textArea.place(x=10, y=50)


# Log file path output text area
logPath = Text(mainWindow, width=39, height=1, bg='old lace')
logPath.place(x=68, y=332)

# Labels
Label(mainWindow, text="Log path:", bg='gray98').place(x=8, y=330)
Label(mainWindow, text="Ready to read easy?", bg='gray98', font='Helvetica').place(x=170, y=10)

def openLogFileAndProcess():
    '''Main program that runs with an open GUI'''

    textArea.delete("1.0", "end")
    logPath.delete("1.0", "end")

    # Select log file
    dicomFilePath = filedialog.askopenfilename(
        initialdir="/",
        title="Open Log file",
        filetypes=(("Dicom File", "*.dcm"),)
    )

    logPath.insert(END, dicomFilePath)  # Writes path address to text box in GUI


    dicom_info = pydicom.dcmread(dicomFilePath)

    # Reads Voxel Size
    voxelSize = ''
    if dicom_info.SliceThickness == 0.2:
        voxelSize = '200um'
    elif dicom_info.SliceThickness == 0.1:
        voxelSize = '100um'
    else:
        voxelSize = '50um'


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

    textArea.insert(END, '{:%d %B %Y ~ %I:%M%p}'.format(date_time_obj) + '\n')
    textArea.insert(END, 'Study Info: ' + str(dicom_info.PatientName) + ' / ' + str(dicom_info.PatientID)+ '\n')
    textArea.insert(END, 'Modality : ' + dicom_info.Modality+ '\n')
    textArea.insert(END, 'Acquisition type : ' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTAcquisitionTypeSequence[0].AcquisitionType).capitalize() + '\n')
    textArea.insert(END, 'Reconstruction algorithm : ' + (
        dicom_info.SharedFunctionalGroupsSequence[0].CTReconstructionSequence[
            0].ReconstructionAlgorithm).capitalize() + '\n')
    textArea.insert(END, 'Voltage : ' + str(
        dicom_info.SharedFunctionalGroupsSequence[0].CTXRayDetailsSequence[0].KVP) + 'kV' + '\n')
    textArea.insert(END, 'Voxel Size = ' + voxelSize + '\n')


# Main buttons
Button(mainWindow, text="Open Dicom", command=openLogFileAndProcess, height=1, width=10,
       bg='snow').place(x=2, y=2)

mainWindow.mainloop()