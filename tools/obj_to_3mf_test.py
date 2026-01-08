import sys, zipfile, re
from collections import defaultdict
import xml.etree.ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: python obj_to_3mf_test.py in.obj out.3mf")
    sys.exit(2)

infile = sys.argv[1]
outfile = sys.argv[2]

# Parse OBJ: collect global vertices and per-object faces
vertices = []
obj_faces = defaultdict(list)  # name -> list of faces (each face as tuple of global vertex indices)
current = None
with open(infile, 'r', encoding='utf-8', errors='ignore') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        if line.startswith('v '):
            parts = line.split()
            x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
            vertices.append((x, y, z))
        elif line.startswith('o ') or line.startswith('g '):
            current = line[2:].strip()
        elif line.startswith('f '):
            if current is None:
                current = 'default'
            parts = line[2:].split()
            idxs = []
            for p in parts:
                a = p.split('/')
                idx = int(a[0])
                if idx < 0:
                    idx = len(vertices) + 1 + idx
                idxs.append(idx-1)
            obj_faces[current].append(tuple(idxs))

print('Found', len(vertices), 'vertices and', len(obj_faces), 'objects')

# Build per-object vertex lists and remap faces
objects = []  # list of (name, verts, faces_local)
for name, faces in obj_faces.items():
    used = {}
    verts = []
    faces_local = []
    for face in faces:
        local = []
        for gi in face:
            if gi not in used:
                used[gi] = len(verts)
                verts.append(vertices[gi])
            local.append(used[gi])
        faces_local.append(tuple(local))
    objects.append((name, verts, faces_local))

# Write minimal 3MF
NS = 'http://schemas.microsoft.com/3dmanufacturing/2013/01'
model = ET.Element('model', {'unit':'millimeter','xmlns':NS})
resources = ET.SubElement(model, 'resources')
for idx, (name, verts, faces) in enumerate(objects, start=1):
    obj = ET.SubElement(resources, 'object', {'id':str(idx), 'type':'model', 'name':re.sub(r'[^0-9A-Za-z_\-]','_',name)})
    mesh_el = ET.SubElement(obj, 'mesh')
    verts_el = ET.SubElement(mesh_el, 'vertices')
    for x,y,z in verts:
        v = ET.SubElement(verts_el, 'vertex')
        v.set('x', repr(x)); v.set('y', repr(y)); v.set('z', repr(z))
    tris_el = ET.SubElement(mesh_el, 'triangles')
    for a,b,c in faces:
        t = ET.SubElement(tris_el, 'triangle')
        t.set('v1', str(a)); t.set('v2', str(b)); t.set('v3', str(c))

build = ET.SubElement(model, 'build')
for idx in range(1, len(objects)+1):
    ET.SubElement(build, 'item', {'objectid':str(idx)})

model_xml = ET.tostring(model, encoding='utf-8', method='xml')
content_types = b'<?xml version="1.0" encoding="utf-8"?>\n<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">\n  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>\n  <Default Extension="model" ContentType="application/vnd.ms-package.3dmanufacturing-3dmodel+xml"/>\n</Types>'
rels_xml = b'<?xml version="1.0" encoding="utf-8"?>\n<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">\n  <Relationship Id="rId1" Type="http://schemas.microsoft.com/3dmanufacturing/2013/01/3dmodel" Target="/3D/3dmodel.model"/>\n</Relationships>'

with zipfile.ZipFile(outfile, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', content_types)
    z.writestr('_rels/.rels', rels_xml)
    z.writestr('3D/3dmodel.model', model_xml)

print('Wrote', outfile)
print('Archive contains:', zipfile.ZipFile(outfile).namelist())
