"""DXF -> DWFx (formato de Autodesk que exige EPM), sin AutoCAD.
DWFx = paquete OPC/ZIP con paginas XPS (FixedPage) + manifiesto DWF. Cada layout de papel del DXF es una hoja.
Todo se dibuja como vector (el texto como contornos rellenos, asi no se necesitan fuentes embebidas).
Uso:  python3 dxf_a_dwfx.py plano.dxf salida.dwfx ["Titulo"]
Estructura copiada de un DWFx real devuelto por EPM (Jardines de Guadalupe, 2025)."""
import sys, os, io, uuid, zipfile, math, datetime
import numpy as np
import ezdxf
from ezdxf.addons.drawing import RenderContext, Frontend, recorder
from ezdxf.addons.drawing.config import Configuration, BackgroundPolicy, TextPolicy
from ezdxf.path import Command

# Firma e imagenes sin marco: ezdxf dibuja siempre el borde del IMAGE; se suprime.
_orig_img = Frontend.draw_image_entity
def _img_sin_marco(self, entity, properties):
    self.pipeline.draw_solid_lines = lambda *a, **k: None
    try: _orig_img(self, entity, properties)
    finally: del self.pipeline.draw_solid_lines
Frontend.draw_image_entity = _img_sin_marco

K = 96.0 / 25.4          # mm -> unidad XPS (1/96 in)

def G(): return str(uuid.uuid4()).upper()
def color_xps(c):
    c = c.lstrip("#")
    if len(c) == 8: return "#" + c[6:8].upper() + c[0:6].upper()      # RRGGBBAA -> AARRGGBB
    return "#" + c.upper()
def fmt(v): return f"{v:.2f}".rstrip("0").rstrip(".")

class Pagina:
    def __init__(self, w_mm, h_mm, lw_scale=0.6):
        self.w, self.h, self.s = w_mm, h_mm, lw_scale; self.items = []; self.imgs = []
    def P(self, x, y): return (x*K, (self.h - y)*K)
    def pt(self, x, y): X, Y = self.P(x, y); return f"{fmt(X)},{fmt(Y)}"
    def grosor(self, lw): return fmt(max(lw, 0.10) * self.s * K)
    def linea(self, pts, props, cerrar=False):
        if len(pts) < 2: return
        d = "M" + self.pt(*pts[0]) + "L" + " ".join(self.pt(*p) for p in pts[1:]) + ("Z" if cerrar else "")
        self.items.append(f'<Path Stroke="{color_xps(props.color)}" StrokeThickness="{self.grosor(props.lineweight)}" StrokeStartLineCap="Round" StrokeEndLineCap="Round" StrokeLineJoin="Round" Data="{d}"/>')
    def segmentos(self, arr, props):
        parts = []
        for i in range(0, len(arr) - 1, 2):
            parts.append("M" + self.pt(*arr[i]) + "L" + self.pt(*arr[i+1]))
        if parts:
            self.items.append(f'<Path Stroke="{color_xps(props.color)}" StrokeThickness="{self.grosor(props.lineweight)}" StrokeStartLineCap="Round" StrokeEndLineCap="Round" Data="{"".join(parts)}"/>')
    def _path_d(self, p, cerrar):
        pa = p.to_path() if hasattr(p, "to_path") else p
        d = ["M" + self.pt(pa.start.x, pa.start.y)]
        for c in pa.commands():
            t = c.type
            if t == Command.LINE_TO: d.append("L" + self.pt(c.end.x, c.end.y))
            elif t == Command.MOVE_TO: d.append("M" + self.pt(c.end.x, c.end.y))
            elif t == Command.CURVE3_TO: d.append("Q" + self.pt(c.ctrl.x, c.ctrl.y) + " " + self.pt(c.end.x, c.end.y))
            elif t == Command.CURVE4_TO: d.append("C" + self.pt(c.ctrl1.x, c.ctrl1.y) + " " + self.pt(c.ctrl2.x, c.ctrl2.y) + " " + self.pt(c.end.x, c.end.y))
        if cerrar: d.append("Z")
        return "".join(d)
    def trazo(self, p, props):
        self.items.append(f'<Path Stroke="{color_xps(props.color)}" StrokeThickness="{self.grosor(props.lineweight)}" StrokeStartLineCap="Round" StrokeEndLineCap="Round" StrokeLineJoin="Round" Data="{self._path_d(p, False)}"/>')
    def relleno(self, paths, props):
        d = "".join(self._path_d(p, True) for p in paths if len(p))
        if d: self.items.append(f'<Path Fill="{color_xps(props.color)}" Data="F0 {d}"/>')
    def poligono(self, pts, props):
        d = "M" + self.pt(*pts[0]) + "L" + " ".join(self.pt(*p) for p in pts[1:]) + "Z"
        self.items.append(f'<Path Fill="{color_xps(props.color)}" Data="{d}"/>')
    def imagen(self, rec, nombre):
        from PIL import Image
        img = rec.image_data.image; hpx, wpx = img.shape[0], img.shape[1]
        m = rec.image_data.transform
        def T(u, v): q = m.transform((u, v, 0)); return self.P(q.x, q.y)
        o, ex, ey = T(0, 0), T(wpx, 0), T(0, hpx)
        a, b = (ex[0]-o[0])/wpx, (ex[1]-o[1])/wpx; c, d = (ey[0]-o[0])/hpx, (ey[1]-o[1])/hpx
        buf = io.BytesIO(); Image.fromarray(np.ascontiguousarray(np.flip(img, axis=0))).save(buf, "PNG"); self.imgs.append((nombre, buf.getvalue()))
        # ezdxf: fila v=0 abajo; en XPS la fila 0 va arriba -> se voltea la imagen
        bd = rec.boundary.vertices() if hasattr(rec.boundary, "vertices") else list(rec.boundary)
        dd = "M" + self.pt(bd[0].x, bd[0].y) + "L" + " ".join(self.pt(p.x, p.y) for p in bd[1:]) + "Z"
        self.items.append(f'<Path Data="{dd}"><Path.Fill><ImageBrush ImageSource="{nombre}" Viewbox="0,0,{wpx},{hpx}" ViewboxUnits="Absolute" Viewport="0,0,{wpx},{hpx}" ViewportUnits="Absolute" TileMode="None" Transform="{fmt(a)},{fmt(b)},{fmt(c)},{fmt(d)},{fmt(o[0])},{fmt(o[1])}"/></Path.Fill></Path>')
    def xml(self):
        W, H = self.w*K, self.h*K
        return ('<?xml version="1.0" encoding="utf-8"?>'
                f'<FixedPage xmlns="http://schemas.microsoft.com/xps/2005/06" Width="{fmt(W)}" Height="{fmt(H)}" xml:lang="es-CO">'
                f'<Path Fill="#FFFFFF" Data="M0,0H{fmt(W)}V{fmt(H)}H0Z"/>'
                f'<Canvas Name="dwfresource_1">' + "".join(self.items) + '</Canvas></FixedPage>')

def pagina_de_layout(doc, lay, w, h):
    rec = recorder.Recorder()
    cfg = Configuration(background_policy=BackgroundPolicy.WHITE, text_policy=TextPolicy.FILLING, lineweight_scaling=1.0)
    Frontend(RenderContext(doc), rec, config=cfg).draw_layout(lay, finalize=True)
    pg = Pagina(w, h); n_img = 0
    for r, props in rec.player().recordings():
        if isinstance(r, recorder.PointsRecord):
            v = [(p.x, p.y) for p in r.points.vertices()]
            if len(v) == 2: pg.linea(v, props)
            elif len(v) > 2: pg.poligono(v, props)
        elif isinstance(r, recorder.SolidLinesRecord):
            pg.segmentos([(p.x, p.y) for p in r.lines.vertices()], props)
        elif isinstance(r, recorder.PathRecord):
            pg.trazo(r.path, props)
        elif isinstance(r, recorder.FilledPathsRecord):
            pg.relleno(r.paths, props)
        elif isinstance(r, recorder.ImageRecord):
            n_img += 1
            try: pg.imagen(r, f"img{n_img}.png")
            except Exception as e: print("imagen omitida:", e)
    return pg

def escribir_dwfx(dxf_path, out_path, titulo=None, lw_scale=0.6, solo=None):
    """solo = lista de nombres de layout; EPM recibe UN plano por archivo."""
    doc = ezdxf.readfile(dxf_path)
    lays = [l for l in doc.layouts if l.name != "Model" and len(l) > 1 and (solo is None or l.name in solo)]
    lays.sort(key=lambda l: l.dxf.taborder)
    titulo = titulo or os.path.splitext(os.path.basename(dxf_path))[0]
    DOC = G(); base = f"/dwf/documents/{DOC}"
    ahora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    files = {}; secciones = []; fdoc = []
    for i, lay in enumerate(lays, 1):
        w = lay.dxf.paper_width or 841.0; h = lay.dxf.paper_height or 594.0
        pg = pagina_de_layout(doc, lay, w, h); pg.s = lw_scale
        SEC = G(); sd = f"{base}/sections/com.autodesk.dwf.ePlot_{SEC}"
        files[f"{sd}/FixedPage.fpage"] = pg.xml()
        rels = [f'<Relationship Target="{sd}/{n}" Id="R{j}" Type="http://schemas.microsoft.com/xps/2005/06/required-resource"/>' for j, (n, _) in enumerate(pg.imgs)]
        for n, data in pg.imgs: files[f"{sd}/{n}"] = data
        if rels: files[f"{sd}/_rels/FixedPage.fpage.rels"] = '<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' + "".join(rels) + '</Relationships>'
        nombre = f"{titulo} - {lay.name}"
        tr = f"{fmt(1/K)} 0 0 0 0 {fmt(1/K)} 0 0 0 0 1 0 0 0 0 1"
        files[f"{sd}/descriptor.xml"] = (f'<ePlot:Page xmlns:ePlot="DWF-ePlot:1.2" version="1.2" objectId="{G()}" name="{nombre}" plotOrder="{i}" color="255 255 255">'
            f'<ePlot:Paper units="mm" width="{fmt(w)}" height="{fmt(h)}" color="255 255 255" clip="0 0 {fmt(w)} {fmt(h)}"/>'
            f'<ePlot:Properties id="{G()}"><ePlot:Property name="Author" value="Ing. Marcos Ivan Ortiz Botero"/><ePlot:Property name="Creation Time" value="{ahora}"/>'
            f'<ePlot:Property name="Creator" value="Domotex - dxf_a_dwfx.py (ezdxf {ezdxf.__version__})" category="Drawing"/><ePlot:Property name="Layout Name" value="{lay.name}" category="Drawing"/></ePlot:Properties>'
            f'<ePlot:Resources><ePlot:GraphicResource role="2d streaming graphics" mime="application/vnd.adsk-package.dwfx-fixedpage+xml" href="{sd}/FixedPage.fpage?dwfresource_1" title="{nombre}" internalId="dwfresource_1" objectId="{G()}" clip="0 0 {fmt(w)} {fmt(h)}" transform="{tr}"/></ePlot:Resources></ePlot:Page>')
        files[f"{sd}/_rels/descriptor.xml.rels"] = ('<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            f'<Relationship Target="{sd}/FixedPage.fpage" Id="R1" Type="http://schemas.autodesk.com/dwfx/2007/relationships/requiredresource"/></Relationships>')
        secciones.append((SEC, sd, nombre))
        fdoc.append(f'<PageContent Source="{sd}/FixedPage.fpage" Width="{fmt(w*K)}" Height="{fmt(h*K)}"/>')
    files[f"{base}/FixedDocument.fdoc"] = '<?xml version="1.0" encoding="utf-8"?><FixedDocument xmlns="http://schemas.microsoft.com/xps/2005/06">' + "".join(fdoc) + '</FixedDocument>'
    man = [f'<dwf:Manifest xmlns:dwf="DWF-Manifest:6.0" version="6.0" objectId="{DOC}"><dwf:Interfaces><dwf:Interface objectId="715941D4-1AC2-4545-8185-BC40E053B551" name="ePlot" href="http://www.autodesk.com/viewers"/></dwf:Interfaces>'
           '<dwf:Properties><dwf:Property name="DWFFormatVersion" value="7.10"/></dwf:Properties><dwf:Sections>']
    for SEC, sd, nombre in secciones:
        man.append(f'<dwf:Section type="com.autodesk.dwf.ePlot" name="com.autodesk.dwf.ePlot_{SEC}" title="{nombre}"><dwf:Source provider="dxf_a_dwfx" href="{nombre}"/><dwf:Toc>'
                   f'<dwf:Resource role="descriptor" mime="text/xml" href="{sd}/descriptor.xml"/>'
                   f'<dwf:Resource role="2d streaming graphics" mime="application/vnd.adsk-package.dwfx-fixedpage+xml" href="{sd}/FixedPage.fpage?dwfresource_1"/></dwf:Toc></dwf:Section>')
    man.append('</dwf:Sections></dwf:Manifest>')
    files[f"{base}/manifest.xml"] = "".join(man)
    files[f"{base}/_rels/manifest.xml.rels"] = ('<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">' +
        "".join(f'<Relationship Target="{sd}/descriptor.xml" Id="S{k}" Type="http://schemas.autodesk.com/dwfx/2007/relationships/section"/>' for k, (_, sd, _) in enumerate(secciones)) + '</Relationships>')
    files["/FixedDocumentSequence.fdseq"] = f'<?xml version="1.0" encoding="utf-8"?><FixedDocumentSequence xmlns="http://schemas.microsoft.com/xps/2005/06"><DocumentReference Source="{base}/FixedDocument.fdoc"/></FixedDocumentSequence>'
    files["/DWFDocumentSequence.dwfseq"] = f'<?xml version="1.0" encoding="utf-8"?><DWFDocumentSequence xmlns="http://schemas.dwf.autodesk.com/dwfx/2006/11"><ManifestReference Source="{base}/manifest.xml"/></DWFDocumentSequence>'
    files["/_rels/DWFDocumentSequence.dwfseq.rels"] = f'<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships"><Relationship Target="{base}/manifest.xml" Id="D1" Type="http://schemas.autodesk.com/dwfx/2007/relationships/document"/></Relationships>'
    files["/CoreProperties.xml"] = '<?xml version="1.0" encoding="utf-8"?><coreProperties xmlns="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"/>'
    files["/_rels/.rels"] = ('<?xml version="1.0" encoding="utf-8"?><Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="/CoreProperties.xml" Id="C1"/>'
        '<Relationship Type="http://schemas.autodesk.com/dwfx/2007/relationships/documentsequence" Target="/DWFDocumentSequence.dwfseq" Id="C2"/>'
        '<Relationship Type="http://schemas.microsoft.com/xps/2005/06/fixedrepresentation" Target="/FixedDocumentSequence.fdseq" Id="C3"/></Relationships>')
    files["/[Content_Types].xml"] = ('<?xml version="1.0" encoding="utf-8"?><Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
        '<Default Extension="dwfseq" ContentType="application/vnd.adsk-package.dwfx-dwfdocumentsequence+xml"/>'
        '<Default Extension="fdoc" ContentType="application/vnd.ms-package.xps-fixeddocument+xml"/>'
        '<Default Extension="fdseq" ContentType="application/vnd.ms-package.xps-fixeddocumentsequence+xml"/>'
        '<Default Extension="fpage" ContentType="application/vnd.ms-package.xps-fixedpage+xml"/>'
        '<Default Extension="png" ContentType="image/png"/>'
        '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
        '<Default Extension="xml" ContentType="text/xml"/>'
        '<Override PartName="/CoreProperties.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/></Types>')
    orden = ["/[Content_Types].xml", "/_rels/.rels"] + [k for k in files if k not in ("/[Content_Types].xml", "/_rels/.rels")]
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for k in orden:
            v = files[k]; z.writestr(k.lstrip("/"), v.encode("utf-8") if isinstance(v, str) else v)
    return out_path, len(lays)

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    t = sys.argv[3] if len(sys.argv) > 3 else None
    p, n = escribir_dwfx(src, dst, t); print("OK", p, n, "hojas", os.path.getsize(p)//1024, "kB")
