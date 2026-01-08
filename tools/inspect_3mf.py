import zipfile, sys
p = sys.argv[1]
with zipfile.ZipFile(p,'r') as z:
    print('\n'.join(z.namelist()))
    data = z.read('3D/3dmodel.model')
    print('\n--- model start ---\n')
    print(data.decode('utf-8')[:2000])
