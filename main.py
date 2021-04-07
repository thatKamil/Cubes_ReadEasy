import pydicom
import datetime

dicom_info = pydicom.dcmread('C:\\Users\\tksokolo1\\Desktop\\thisisdicom.dcm')

# Reads Voxel Size
voxelSize = ''
if dicom_info.SliceThickness == 0.2:
    voxelSize = '200um'
elif dicom_info.SliceThickness == 0.1:
    voxelSize == '100um'
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

print('{:%d %B %Y ~ %I:%M%p}'.format(date_time_obj))


print('Modality : ' + dicom_info.Modality)
print('Acquisition type : ' + dicom_info.SharedFunctionalGroupsSequence[0].CTAcquisitionTypeSequence[0].AcquisitionType)
print('Reconstruction algorithm : ' + dicom_info.SharedFunctionalGroupsSequence[0].CTReconstructionSequence[0].ReconstructionAlgorithm)
print('Exposure time : ' + (str(dicom_info.SharedFunctionalGroupsSequence[0].CTExposureSequence[0][0x18,0x9332].value)[0:2]) + 'ms')
print('Voxel Size = ' + voxelSize)
print('kV : ' + str(dicom_info.SharedFunctionalGroupsSequence[0].CTXRayDetailsSequence[0].KVP))