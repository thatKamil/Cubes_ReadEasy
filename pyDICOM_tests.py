import pydicom
from pydicom.data import get_testdata_file
filename = get_testdata_file('rtplan.dcm')
ds = pydicom.dcmread(filename)


# print(ds.PatientName)
print(ds)

print(ds.BeamSequence[0].BeamLimitingDeviceSequence[0].RTBeamLimitingDeviceType)

print(ds[0x300a,0xb0][0][0x300a,0xc2].value)

