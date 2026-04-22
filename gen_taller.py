#!/usr/bin/env python3
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import cm, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable,
                                 KeepTogether, PageBreak, Image as RLImage)
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
import os

# ── Paleta ──────────────────────────────────────────────────────────────────
FOREST  = HexColor('#1E3D0A')
GREEN   = HexColor('#2D5016')
GREEN_M = HexColor('#3E6B20')
GREEN_L = HexColor('#5A8F32')
SAGE    = HexColor('#8BB060')
OCHRE   = HexColor('#B8741A')
GOLD    = HexColor('#D4922C')
SAND    = HexColor('#F2EAD8')
LINEN   = HexColor('#FAF6EE')
INK     = HexColor('#1A1A18')
INK_M   = HexColor('#3D3B34')
INK_L   = HexColor('#6B6555')
RED     = HexColor('#C0392B')
RED_BG  = HexColor('#FDF1EF')
WHITE   = colors.white

OUTPUT = os.path.join(os.path.dirname(__file__), 'taller-01-heno-motita.pdf')

# ── Página con encabezado/pie ────────────────────────────────────────────────
def make_page(canvas_obj, doc):
    W, H = letter
    # Banda superior
    canvas_obj.setFillColor(FOREST)
    canvas_obj.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    # Título en banda
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('Helvetica-Bold', 9)
    canvas_obj.drawString(2*cm, H - 12*mm, 'TALLER 1 · PRIMERA CAMPAÑA DE CONTROL DE HENO MOTITA')
    canvas_obj.setFont('Helvetica', 8)
    canvas_obj.setFillColor(HexColor('#A8C87A'))
    canvas_obj.drawRightString(W - 2*cm, H - 12*mm, 'Valle del Mezquital · Hidalgo · 2026')
    # Línea naranja decorativa
    canvas_obj.setFillColor(OCHRE)
    canvas_obj.rect(0, H - 31*mm, W, 3*mm, fill=1, stroke=0)
    # Pie de página
    canvas_obj.setFillColor(FOREST)
    canvas_obj.rect(0, 0, W, 12*mm, fill=1, stroke=0)
    canvas_obj.setFillColor(WHITE)
    canvas_obj.setFont('Helvetica-Bold', 7.5)
    canvas_obj.drawRightString(W - 2*cm, 4*mm, f'Pág. {doc.page}')

# ── Estilos ──────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def S(name, **kw):
    return ParagraphStyle(name, **kw)

sTitle = S('sTitle',
    fontName='Helvetica-Bold', fontSize=26, textColor=WHITE,
    leading=30, alignment=TA_CENTER)

sSubtitle = S('sSubtitle',
    fontName='Helvetica', fontSize=12, textColor=HexColor('#C8E8A0'),
    leading=16, alignment=TA_CENTER)

sMeta = S('sMeta',
    fontName='Helvetica', fontSize=9, textColor=HexColor('#A8C87A'),
    leading=13, alignment=TA_CENTER)

sModLabel = S('sModLabel',
    fontName='Helvetica-Bold', fontSize=7.5, textColor=OCHRE,
    leading=10, spaceBefore=4, spaceAfter=2,
    letterSpacing=1.5)

sModTitle = S('sModTitle',
    fontName='Helvetica-Bold', fontSize=14, textColor=WHITE,
    leading=17)

sModTime = S('sModTime',
    fontName='Helvetica', fontSize=8, textColor=HexColor('#C8E8A0'),
    leading=11)

sBody = S('sBody',
    fontName='Helvetica', fontSize=10, textColor=INK_M,
    leading=15, spaceAfter=3, alignment=TA_JUSTIFY)

sBullet = S('sBullet',
    fontName='Helvetica', fontSize=10, textColor=INK_M,
    leading=15, leftIndent=14, firstLineIndent=-10, spaceAfter=3)

sBulletB = S('sBulletB',
    fontName='Helvetica-Bold', fontSize=10, textColor=GREEN,
    leading=15, leftIndent=14, firstLineIndent=-10, spaceAfter=3)

sSub = S('sSub',
    fontName='Helvetica', fontSize=9, textColor=INK_L,
    leading=13, leftIndent=26, firstLineIndent=-10, spaceAfter=2)

sWarn = S('sWarn',
    fontName='Helvetica-Bold', fontSize=9.5, textColor=RED,
    leading=14, leftIndent=14, firstLineIndent=-10, spaceAfter=3)

sNote = S('sNote',
    fontName='Helvetica-Oblique', fontSize=8.5, textColor=INK_L,
    leading=12, leftIndent=8, spaceAfter=4)

sKey = S('sKey',
    fontName='Helvetica-Bold', fontSize=10, textColor=FOREST,
    leading=15, leftIndent=14, firstLineIndent=-10, spaceAfter=3)

sSectionTitle = S('sSectionTitle',
    fontName='Helvetica-Bold', fontSize=11, textColor=GREEN,
    leading=14, spaceBefore=10, spaceAfter=4)

sCover = S('sCover',
    fontName='Helvetica', fontSize=10, textColor=HexColor('#C8E8A0'),
    leading=16, alignment=TA_CENTER)

# ── Helpers ──────────────────────────────────────────────────────────────────
def rule(color=GREEN_L, thickness=0.6):
    return HRFlowable(width='100%', thickness=thickness, color=color,
                      spaceAfter=6, spaceBefore=2)

def spacer(h=0.3):
    return Spacer(1, h*cm)

def mod_header(num, label, title, time_str, color=GREEN):
    data = [[
        Paragraph(f'<b>{num}</b>', S('mn', fontName='Helvetica-Bold',
                  fontSize=22, textColor=WHITE, leading=26, alignment=TA_CENTER)),
        [Paragraph(f'MÓDULO {num} · {label}', sModLabel),
         Paragraph(title, sModTitle),
         Paragraph(f'⏱ {time_str}', sModTime)]
    ]]
    t = Table(data, colWidths=[1.6*cm, None])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), color),
        ('VALIGN',     (0,0), (-1,-1), 'MIDDLE'),
        ('LEFTPADDING',(0,0),(0,0), 10),
        ('RIGHTPADDING',(0,0),(0,0), 8),
        ('TOPPADDING', (0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('ROUNDEDCORNERS', [6,6,6,6]),
    ]))
    return t

def box(items, bg=SAND, border=GREEN_L, left_bar=None):
    content = []
    for it in items:
        content.append(it)
    data = [[content]]
    t = Table(data, colWidths=['100%'])
    style = [
        ('BACKGROUND', (0,0),(-1,-1), bg),
        ('BOX',        (0,0),(-1,-1), 0.8, border),
        ('LEFTPADDING', (0,0),(-1,-1), 12),
        ('RIGHTPADDING',(0,0),(-1,-1), 12),
        ('TOPPADDING',  (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]
    t.setStyle(TableStyle(style))
    return t

def warn_box(items):
    return box(items, bg=RED_BG, border=RED)

def key_box(items):
    return box(items, bg=HexColor('#EBF3E0'), border=GREEN_M)

def b(text): return f'<b>{text}</b>'
def em(text): return f'<i>{text}</i>'
def green(text): return f'<font color="#2D5016"><b>{text}</b></font>'
def ochre(text): return f'<font color="#B8741A"><b>{text}</b></font>'
def red(text): return f'<font color="#C0392B"><b>{text}</b></font>'

# ── Contenido ────────────────────────────────────────────────────────────────
def build():
    doc = SimpleDocTemplate(OUTPUT, pagesize=letter,
                            topMargin=3.5*cm, bottomMargin=2*cm,
                            leftMargin=2*cm, rightMargin=2*cm)
    story = []
    W = letter[0] - 4*cm  # ancho útil

    # ════════════════════════════════════════════════════════════
    # PORTADA
    # ════════════════════════════════════════════════════════════
    cover_items = [
        Paragraph('🌿', S('ico', fontName='Helvetica', fontSize=28,
                           alignment=TA_CENTER, leading=40)),
        Paragraph('TALLER 1', S('tw', fontName='Helvetica-Bold',
                    fontSize=9, textColor=GOLD, leading=12, alignment=TA_CENTER,
                    letterSpacing=3)),
        Paragraph('Primera Campaña de Control<br/>del Heno Motita', sTitle),
        Paragraph(em('Tillandsia recurvata') + ' · Valle del Mezquital, Hidalgo', sSubtitle),
        Spacer(1, 0.4*cm),
        Paragraph('Duración: 30 minutos · 5 módulos · Año 2026', sMeta),
        Spacer(1, 0.2*cm),
    ]
    cover_bg = Table([[cover_items]], colWidths=[W])
    cover_bg.setStyle(TableStyle([
        ('BACKGROUND',     (0,0),(-1,-1), FOREST),
        ('TOPPADDING',     (0,0),(-1,-1), 22),
        ('BOTTOMPADDING',  (0,0),(-1,-1), 22),
        ('LEFTPADDING',    (0,0),(-1,-1), 18),
        ('RIGHTPADDING',   (0,0),(-1,-1), 18),
        ('ROUNDEDCORNERS', [8,8,8,8]),
        ('VALIGN',         (0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(spacer(0.5))
    story.append(cover_bg)
    story.append(spacer(1.5))

    # Recuadro de objetivos de portada
    story.append(key_box([
        Paragraph(b('Objetivo del taller'), sSectionTitle),
        Paragraph('Al finalizar, los participantes podrán identificar árboles prioritarios, '
                  'aplicar el protocolo correcto de control mecánico-químico y evitar los '
                  'errores más comunes que hacen fracasar una campaña.', sBody),
    ]))
    story.append(spacer(0.5))

    # Tabla resumen de módulos
    mod_data = [
        [Paragraph(b('Módulo'), S('th', fontName='Helvetica-Bold', fontSize=9,
                   textColor=WHITE, leading=11)),
         Paragraph(b('Tema'), S('th', fontName='Helvetica-Bold', fontSize=9,
                   textColor=WHITE, leading=11)),
         Paragraph(b('Tiempo'), S('th', fontName='Helvetica-Bold', fontSize=9,
                   textColor=WHITE, leading=11))],
        ['1', Paragraph('El problema: qué es y cuándo es dañino', sBody), '5 min'],
        ['2', Paragraph('Evaluar la infestación: cómo priorizar', sBody), '5 min'],
        ['3', Paragraph('Métodos de control: protocolos paso a paso', sBody), '10 min'],
        ['4', Paragraph('Errores comunes y cómo evitarlos', sBody), '5 min'],
        ['5', Paragraph('Plan de acción: organizar la brigada', sBody), '5 min'],
    ]
    mt = Table(mod_data, colWidths=[1.5*cm, None, 2*cm])
    mt.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), FOREST),
        ('BACKGROUND', (0,1),(-1,1), HexColor('#EBF3E0')),
        ('BACKGROUND', (0,2),(-1,2), WHITE),
        ('BACKGROUND', (0,3),(-1,3), HexColor('#EBF3E0')),
        ('BACKGROUND', (0,4),(-1,4), WHITE),
        ('BACKGROUND', (0,5),(-1,5), HexColor('#EBF3E0')),
        ('ALIGN',      (0,0),(0,-1), 'CENTER'),
        ('ALIGN',      (2,0),(2,-1), 'CENTER'),
        ('VALIGN',     (0,0),(-1,-1),'MIDDLE'),
        ('FONTNAME',   (0,1),(0,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (0,1),(0,-1), 11),
        ('TEXTCOLOR',  (0,1),(0,-1), GREEN),
        ('FONTNAME',   (2,1),(2,-1), 'Helvetica-Bold'),
        ('FONTSIZE',   (2,1),(2,-1), 9),
        ('TEXTCOLOR',  (2,1),(2,-1), OCHRE),
        ('BOX',        (0,0),(-1,-1), 1, GREEN_L),
        ('INNERGRID',  (0,0),(-1,-1), 0.4, HexColor('#C5D8A0')),
        ('TOPPADDING', (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
    ]))
    story.append(mt)
    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # MÓDULO 1
    # ════════════════════════════════════════════════════════════
    story.append(mod_header('1', 'EL PROBLEMA', 'Qué es el heno motita y cuándo es dañino', '5 minutos', FOREST))
    story.append(spacer(0.4))

    story.append(Paragraph('¿Qué es?', sSectionTitle))
    story.append(Paragraph(
        f'{b("Tillandsia recurvata")} es una planta epífita (vive sobre otras plantas) de la familia '
        f'de las bromelias. Se fija a las ramas de mezquites, huizaches y otros árboles del Valle del Mezquital. '
        f'No tiene raíces en el suelo — obtiene agua y nutrientes del aire a través de sus {em("tricomas")} '
        f'(escamas plateadas en su superficie).', sBody))
    story.append(spacer(0.2))

    story.append(Paragraph('El rol dual: epífito vs. parásito estructural', sSectionTitle))
    dual_data = [
        [Paragraph(b('A BAJA DENSIDAD'), S('dh', fontName='Helvetica-Bold', fontSize=9,
            textColor=GREEN_M, leading=11, alignment=TA_CENTER)),
         Paragraph(b('A ALTA DENSIDAD (>50% de la rama)'), S('dh', fontName='Helvetica-Bold',
            fontSize=9, textColor=RED, leading=11, alignment=TA_CENTER))],
        [Paragraph('• Alberga +80 especies de artrópodos\n'
                   '• Intercepta humedad atmosférica\n'
                   '• Secuestra metales pesados del aire\n'
                   '• Daño al árbol: no significativo', sBullet),
         Paragraph('• Daña tejidos vasculares del árbol\n'
                   '• Reduce capacidad de sobrevivir la sequía\n'
                   '• Provoca pérdida de ramas (dieback)\n'
                   '• Actúa como {}'.format(red('parásita estructural')), sBullet)],
    ]
    dt = Table(dual_data, colWidths=[W/2 - 0.2*cm, W/2 - 0.2*cm])
    dt.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,0), HexColor('#EBF3E0')),
        ('BACKGROUND', (1,0),(1,0), RED_BG),
        ('BACKGROUND', (0,1),(0,1), HexColor('#F4FAF0')),
        ('BACKGROUND', (1,1),(1,1), HexColor('#FEF8F7')),
        ('BOX',  (0,0),(0,-1), 0.8, GREEN_M),
        ('BOX',  (1,0),(1,-1), 0.8, RED),
        ('TOPPADDING',   (0,0),(-1,-1), 8),
        ('BOTTOMPADDING',(0,0),(-1,-1), 8),
        ('LEFTPADDING',  (0,0),(-1,-1), 10),
        ('VALIGN',       (0,0),(-1,-1), 'TOP'),
        ('COLPADDING',   (0,0),(-1,-1), 6),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    story.append(dt)
    story.append(spacer(0.4))

    story.append(key_box([
        Paragraph(f'⚠ {ochre("Umbral clave:")} cuando {b("más del 50% de la superficie de una rama")} '
                  f'está cubierta de heno motita → intervención urgente justificada '
                  f'(Flores-Palacios 2014, {em("Prosopis laevigata")}).', sBody),
    ]))
    story.append(spacer(0.3))

    story.append(Paragraph('Por qué se expande tan rápido', sSectionTitle))
    story.append(Paragraph(f'• Una sola semilla puede fundar una colonia: la planta es '
                           f'{b("completamente autógama")} — no necesita otra planta para reproducirse.', sBullet))
    story.append(Paragraph(f'• El material separado del árbol {b("sigue siendo viable hasta 6 meses")} '
                           f'— si no se quema, puede re-establecerse.', sBullet))
    story.append(Paragraph(f'• El {b("comercio navideño")} es el principal vector artificial de dispersión '
                           f'(alerta formal CONAFOR).', sBullet))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # MÓDULO 2
    # ════════════════════════════════════════════════════════════
    story.append(mod_header('2', 'EVALUAR LA INFESTACIÓN', 'Cómo identificar árboles prioritarios', '5 minutos', GREEN))
    story.append(spacer(0.4))

    story.append(Paragraph('Escala de severidad por árbol', sSectionTitle))
    sev_data = [
        [Paragraph(b('Categoría'), S('th2', fontName='Helvetica-Bold', fontSize=9,
            textColor=WHITE, leading=11)),
         Paragraph(b('Criterio visual'), S('th2', fontName='Helvetica-Bold', fontSize=9,
            textColor=WHITE, leading=11)),
         Paragraph(b('Acción'), S('th2', fontName='Helvetica-Bold', fontSize=9,
            textColor=WHITE, leading=11))],
        [Paragraph(green('Baja'), sBody),
         Paragraph('<25% de cobertura en pocas ramas', sBody),
         Paragraph('Monitoreo — sin intervención urgente', sNote)],
        [Paragraph(ochre('Media'), sBody),
         Paragraph('25–50% de cobertura', sBody),
         Paragraph('Remoción con varilla en próxima campaña', sNote)],
        [Paragraph(red('Alta ★'), sBody),
         Paragraph('>50% en múltiples ramas', sBody),
         Paragraph(b('Intervención inmediata — árbol fuente'), sNote)],
        [Paragraph(red('Crítica'), sBody),
         Paragraph('Ramas con dieback visible (secas/muertas)', sBody),
         Paragraph(b('Poda + remoción total'), sNote)],
    ]
    st = Table(sev_data, colWidths=[2.2*cm, None, 5.5*cm])
    st.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), GREEN),
        ('BACKGROUND', (0,1),(-1,1), HexColor('#F4FAF0')),
        ('BACKGROUND', (0,2),(-1,2), WHITE),
        ('BACKGROUND', (0,3),(-1,3), HexColor('#FDF1EF')),
        ('BACKGROUND', (0,4),(-1,4), HexColor('#FEF0EF')),
        ('BOX',        (0,0),(-1,-1), 0.8, GREEN_L),
        ('INNERGRID',  (0,0),(-1,-1), 0.3, HexColor('#D0E0B8')),
        ('TOPPADDING', (0,0),(-1,-1), 7),
        ('BOTTOMPADDING',(0,0),(-1,-1), 7),
        ('LEFTPADDING',(0,0),(-1,-1), 10),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(st)
    story.append(spacer(0.4))

    story.append(Paragraph('Estrategia de priorización', sSectionTitle))
    story.append(Paragraph(
        f'Tratar primero el {b("20% de árboles con mayor carga")} de toda la zona '
        f'— estos son los que sostienen la metapoblación regional y exportan semillas '
        f'a todos los vecinos (Valverde & Bernal 2010).', sBody))
    story.append(spacer(0.2))
    story.append(Paragraph(f'• {b("Zona de inspección prioritaria:")} ramas bajas '
                           f'(mayor humedad, primera zona de recolonización).', sBullet))
    story.append(Paragraph(f'• {b("Árboles más grandes y sanos")} son menos susceptibles a reinfestación '
                           f'— priorizar los débiles/estresados.', sBullet))
    story.append(Paragraph(f'• Registrar por árbol: % estimado de cobertura, categoría '
                           f'(baja/media/alta/crítica), método a aplicar.', sBullet))
    story.append(spacer(0.3))

    story.append(key_box([
        Paragraph(f'{b("Ventana óptima de intervención:")} '
                  f'{ochre("enero – abril")} (temporada seca). '
                  f'Las aspersiones en lluvia (julio–septiembre) pierden efectividad. '
                  f'Esta ventana coincide además con la pre-dispersión de semillas — '
                  f'el mejor momento para cortar el ciclo.', sBody),
    ]))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # MÓDULO 3
    # ════════════════════════════════════════════════════════════
    story.append(mod_header('3', 'MÉTODOS DE CONTROL', 'Protocolos paso a paso', '10 minutos', GREEN_M))
    story.append(spacer(0.4))

    story.append(warn_box([
        Paragraph(f'{red("Principio fundamental:")} ningún método aislado es suficiente. '
                  f'El control duradero requiere {b("remoción mecánica + bicarbonato")} '
                  f'como complemento — en ese orden.', sBody),
    ]))
    story.append(spacer(0.35))

    # Método 1
    story.append(Paragraph('Método 1 — Varilla corrugada (mecánico principal)', sSectionTitle))
    story.append(Paragraph(f'{b("Indicación:")} infestación <50% por rama, cúmulos individuales. '
                           f'{b("Costo:")} el más económico. {b("Ventaja:")} no genera heridas de poda.', sBody))

    m1_steps = [
        ('1', 'Varilla de acero corrugada 3/8", longitud 2–3 m, punta doblada.'),
        ('2', 'Insertar la punta entre los cúmulos de heno y la rama.'),
        ('3', 'Girar/torcer para extraer sin cortar la rama.'),
        ('4', f'{red("Ensacar INMEDIATAMENTE")} — no dejar en el suelo. Viabilidad: 6 meses.'),
        ('5', 'Disponer por quema — único método aprobado por CONAFOR.'),
    ]
    step_data = [[Paragraph(b(n), S('sn', fontName='Helvetica-Bold', fontSize=11,
                   textColor=WHITE, alignment=TA_CENTER, leading=13)),
                  Paragraph(t, sBody)] for n, t in m1_steps]
    s1t = Table(step_data, colWidths=[0.8*cm, None])
    s1t.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(0,-1), GREEN_L),
        ('BACKGROUND', (0,3),(0,3), RED),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0),(-1,-1), 5),
        ('BOTTOMPADDING',(0,0),(-1,-1), 5),
        ('LEFTPADDING',(0,0),(0,-1), 5),
        ('LEFTPADDING',(1,0),(1,-1), 8),
        ('INNERGRID',  (0,0),(-1,-1), 0.3, WHITE),
        ('ROUNDEDCORNERS', [3,3,3,3]),
    ]))
    story.append(s1t)
    story.append(spacer(0.35))

    # Método 2
    story.append(Paragraph('Método 2 — Bicarbonato de sodio (complemento químico)', sSectionTitle))
    story.append(Paragraph(f'{b("Indicación:")} después de la remoción mecánica, o en material '
                           f'residual inaccesible. {b("Temporada:")} solo en época seca (enero–abril).', sBody))

    bic_data = [
        [Paragraph(b('Fuente'), S('bh', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=WHITE, leading=11)),
         Paragraph(b('Concentración'), S('bh', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=WHITE, leading=11)),
         Paragraph(b('Resultado'), S('bh', fontName='Helvetica-Bold', fontSize=8.5,
            textColor=WHITE, leading=11))],
        ['LSU AgCenter', '2.5–5% (25–50 g/L)', 'Eliminación 3–5 días'],
        [Paragraph(b('INIFAP (referencia México)'), sBulletB),
         Paragraph(b('66 g/L (1 kg / 15 L)'), sBulletB),
         Paragraph(b('Control efectivo — recomendado'), sBulletB)],
        ['UTTT 2024', '10% (100 g/L)', 'Más efectivo; recuperación ~1 semana post-tto.'],
    ]
    bt = Table(bic_data, colWidths=[4*cm, 4*cm, None])
    bt.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,0), GREEN_M),
        ('BACKGROUND', (0,2),(-1,2), HexColor('#EBF3E0')),
        ('BOX',        (0,0),(-1,-1), 0.8, GREEN_L),
        ('INNERGRID',  (0,0),(-1,-1), 0.3, HexColor('#C5D8A0')),
        ('TOPPADDING', (0,0),(-1,-1), 6),
        ('BOTTOMPADDING',(0,0),(-1,-1), 6),
        ('LEFTPADDING',(0,0),(-1,-1), 8),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
    ]))
    story.append(bt)
    story.append(spacer(0.25))

    story.append(Paragraph(f'• Disolver completamente antes de cargar la aspersora.', sBullet))
    story.append(Paragraph(f'• {b("Agitar constantemente")} durante la aplicación.', sBullet))
    story.append(Paragraph(f'• Aplicar hasta {b("saturación completa")} — no asperjar superficialmente.', sBullet))
    story.append(Paragraph(f'• {b("El musgo muerto no cae de inmediato")} — puede tardar 18 meses '
                           f'a 10 años. Esto es normal, no es falla del tratamiento.', sNote))
    story.append(spacer(0.3))

    # Método 3
    story.append(Paragraph('Método 3 — Poda de ramas (cuando aplicar)', sSectionTitle))
    story.append(Paragraph(f'Podar {b("solo")} cuando la rama tiene {b(">50% de cobertura")} '
                           f'{b("o presenta dieback")} (ramas secas/en declive).', sBody))
    story.append(Paragraph('• Cortar en el punto de unión con herramienta afilada.', sBullet))
    story.append(Paragraph(f'• {b("Pintar inmediatamente")} todas las heridas con sellador/cicatrizante.', sBullet))
    story.append(Paragraph('• Ensacar y quemar el material podado — no dejar en el suelo.', sBullet))
    story.append(Paragraph(f'• {b("100% de poda")} = podar TODAS las ramas infestadas del árbol '
                           f'(no el árbol completo). Dejar ramas con heno sin tratar '
                           f'reinicia la infestación. (Flores-Flores 2016, 86% reducción).', sNote))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # MÓDULO 4
    # ════════════════════════════════════════════════════════════
    story.append(mod_header('4', 'ERRORES COMUNES', 'Cómo evitar los fallos más frecuentes', '5 minutos', OCHRE))
    story.append(spacer(0.4))

    errors = [
        ('✗ Solo aplicar bicarbonato sin remoción mecánica',
         f'La planta inicia recuperación {b("~1 semana")} después de terminar el tratamiento de 9 semanas. '
         f'Alta resiliencia metabólica (UTTT 2024). La remoción mecánica es el componente principal.'),
        ('✗ Ver el musgo gris y asumir que el tratamiento funcionó',
         f'El heno motita muerto {b("no cae inmediatamente")} — puede persistir de {b("18 meses a 10 años")} '
         f'sobre las ramas, proveyendo microhábitat para nuevas colonias. '
         f'El material muerto sin remover es parte del problema.'),
        ('✗ Tratar un árbol aislado y no toda la zona',
         f'La reinfestación desde árboles vecinos ocurre en {b("menos de 1 año")} en el Valle del Mezquital. '
         f'Tratar un árbol sin tratar los vecinos es trabajo temporal. '
         f'Se requiere estrategia a escala de ejido o municipio.'),
        ('✗ Aplicar bicarbonato en temporada de lluvias',
         f'La lluvia diluye el producto y reduce su efectividad. '
         f'La ventana única es {b("enero–abril")} (temporada seca).'),
        ('✗ Dejar el material removido en el suelo o transportarlo abierto',
         f'La planta separada mantiene viabilidad {b("hasta 6 meses")}. '
         f'Material en el suelo → re-establecimiento en el mismo árbol o en otros. '
         f'Protocolo obligatorio: {b("ensacar + quemar")}.'),
        ('✗ Comprar o regalar heno motita como adorno navideño',
         f'CONAFOR emitió alerta formal: es el {b("principal vector de dispersión artificial")} '
         f'a nuevas zonas. El transporte sin bolsa sellada está desaconsejado.'),
    ]
    for title, desc in errors:
        story.append(KeepTogether([
            warn_box([
                Paragraph(title, sWarn),
                Paragraph(desc, sBody),
            ]),
            spacer(0.25),
        ]))

    story.append(PageBreak())

    # ════════════════════════════════════════════════════════════
    # MÓDULO 5
    # ════════════════════════════════════════════════════════════
    story.append(mod_header('5', 'PLAN DE ACCIÓN', 'Organizar la primera brigada de control', '5 minutos', FOREST))
    story.append(spacer(0.4))

    story.append(warn_box([
        Paragraph(f'{ochre("Meta realista de la primera campaña:")} no es la erradicación total — '
                  f'es {b("reducir la densidad de infestación por debajo del umbral de daño")}. '
                  f'La erradicación a escala de paisaje es prácticamente imposible sin manejo continuo.', sBody),
    ]))
    story.append(spacer(0.35))

    phases = [
        ('FASE 1', 'Antes de la campaña (octubre–diciembre)', [
            'Mapeo: recorrer la zona y clasificar cada árbol (baja/media/alta/crítica).',
            'Priorizar el 20% de árboles con mayor carga — estos son los árboles fuente.',
            'Preparar materiales: varillas, aspersoras, bicarbonato, bolsas, sellador de poda.',
            'Formar y capacitar la brigada (este taller).',
        ]),
        ('FASE 2', 'Intervención principal (enero–abril)', [
            'Tratar primero los árboles fuente con mayor infestación.',
            'Protocolo: remoción con varilla → poda de ramas críticas → bicarbonato 66 g/L.',
            'Ensacar y quemar todo el material el mismo día.',
            'Limpiar herramientas entre sitios de trabajo.',
        ]),
        ('FASE 3', 'Monitoreo y mantenimiento (a 12 meses)', [
            'Inspección visual de todos los árboles tratados.',
            'Zona prioritaria: ramas bajas (primera en recolonizarse).',
            'Árboles que superen 50% nuevamente → intervención en siguiente ventana.',
            'Monitoreo cada 4–6 meses en zonas de alta presión.',
        ]),
    ]
    for code, title, steps in phases:
        phase_data = [[
            Paragraph(b(code), S('pc', fontName='Helvetica-Bold', fontSize=9,
                textColor=OCHRE, leading=11, alignment=TA_CENTER)),
            [Paragraph(b(title), sSectionTitle)] +
            [Paragraph(f'• {s}', sBullet) for s in steps]
        ]]
        pt = Table(phase_data, colWidths=[1.8*cm, None])
        pt.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(-1,-1), HexColor('#F4FAF0')),
            ('LEFTBORDER', (0,0),(0,-1), 4, GREEN_L),
            ('BOX',        (0,0),(-1,-1), 0.6, GREEN_L),
            ('VALIGN',     (0,0),(-1,-1), 'TOP'),
            ('TOPPADDING', (0,0),(-1,-1), 10),
            ('BOTTOMPADDING',(0,0),(-1,-1), 8),
            ('LEFTPADDING',(0,0),(0,-1), 8),
            ('LEFTPADDING',(1,0),(1,-1), 10),
            ('ROUNDEDCORNERS', [4,4,4,4]),
        ]))
        story.append(pt)
        story.append(spacer(0.3))

    story.append(spacer(0.2))
    story.append(key_box([
        Paragraph(b('Materiales mínimos por brigada de 4 personas:'), sSectionTitle),
        Paragraph('• Varillas corrugadas 3/8" × 2–3 m con punta doblada (2 por brigada)', sBullet),
        Paragraph('• Aspersora de mochila (10–15 L) con boquilla de abanico', sBullet),
        Paragraph('• Bicarbonato de sodio: 1 kg por cada 15 L de agua (≈66 g/L)', sBullet),
        Paragraph('• Bolsas de plástico resistente (cierre hermético) para material removido', sBullet),
        Paragraph('• Sellador/cicatrizante para heridas de poda', sBullet),
        Paragraph('• Formatos de registro por árbol (categoría, % cobertura, método aplicado)', sBullet),
    ]))
    story.append(spacer(0.4))

    story.append(rule(OCHRE, 1))
    story.append(Paragraph(
        f'{b("Fuentes científicas:")} INIFAP · UTTT (Reséndiz-Vega et al. 2024) · CONAFOR · '
        f'Flores-Flores et al. 2016 · Valverde & Bernal 2010 · Flores-Palacios 2014 · LSU AgCenter. '
        f'Información compilada con base en evidencia revisada por pares.',
        sNote))

    # ════════════════════════════════════════════════════════════
    # MÓDULO ZRE — DECRETO FEDERAL
    # ════════════════════════════════════════════════════════════
    story.append(PageBreak())

    # Encabezado ZRE con esquema dorado
    GOLD_D = HexColor('#8B6914')
    GOLD_B = HexColor('#B8941A')
    GOLD_L = HexColor('#FFFBF0')
    GOLD_I = HexColor('#D4C070')

    zre_header_data = [[
        Paragraph('<b>ZRE</b>', S('zn', fontName='Helvetica-Bold', fontSize=16,
                  textColor=WHITE, leading=20, alignment=TA_CENTER)),
        [Paragraph('DECRETO FEDERAL · DOF 26/09/2024', S('zl', fontName='Helvetica-Bold',
                   fontSize=7.5, textColor=GOLD, leading=10, spaceAfter=2, letterSpacing=1.5)),
         Paragraph('Zona de Restauración Ecológica — Presa Endhó', S('zt', fontName='Helvetica-Bold',
                   fontSize=14, textColor=WHITE, leading=17)),
         Paragraph('Heno motita nombrado explícitamente como especie invasora objetivo', S('zs',
                   fontName='Helvetica', fontSize=8, textColor=HexColor('#C8E8A0'), leading=11))]
    ]]
    zre_h = Table(zre_header_data, colWidths=[2*cm, None])
    zre_h.setStyle(TableStyle([
        ('BACKGROUND', (0,0),(-1,-1), GOLD_D),
        ('VALIGN',     (0,0),(-1,-1), 'MIDDLE'),
        ('LEFTPADDING', (0,0),(0,0), 10),
        ('RIGHTPADDING',(0,0),(0,0), 8),
        ('TOPPADDING',  (0,0),(-1,-1), 10),
        ('BOTTOMPADDING',(0,0),(-1,-1), 10),
        ('ROUNDEDCORNERS', [6,6,6,6]),
    ]))
    story.append(zre_h)
    story.append(spacer(0.4))

    story.append(Paragraph('¿Qué establece el decreto?', sSectionTitle))
    story.append(Paragraph(
        f'El {b("Decreto ZRE Presa Endhó")} (DOF 26 de septiembre de 2024, LGEEPA Arts. 78 y 78 BIS) '
        f'declara {b("36,637 hectáreas")} del Valle del Mezquital como Zona de Restauración Ecológica '
        f'y nombra al {em("heno motita")} como especie invasora de control obligatorio — '
        f'la primera vez que existe una obligación legal federal expresa para controlarlo.',
        sBody))
    story.append(spacer(0.3))

    story.append(Paragraph('Artículos directamente relevantes al heno motita', sSectionTitle))
    decree_arts = [
        ('Art. 3° fracc. III',
         'Implementar programas de monitoreo y control del heno motita y el lirio acuático '
         'mediante métodos mecánicos y/o biológicos; incluir educación comunitaria sobre su impacto.'),
        ('Art. 3° fracc. XII',
         'Capacitar en los 8 municipios y formar brigadas de saneamiento forestal '
         'para el control de plagas epífitas.'),
        ('Art. 4° fracc. V',
         'Prohibición expresa de introducir o liberar especies invasoras en la ZRE — '
         'refuerza la alerta de CONAFOR sobre el comercio navideño de heno motita.'),
    ]
    for art, text in decree_arts:
        art_data = [[
            Paragraph(b(art), S('al', fontName='Helvetica-Bold', fontSize=8.5,
                       textColor=WHITE, leading=11, alignment=TA_CENTER)),
            Paragraph(text, sBody)
        ]]
        at = Table(art_data, colWidths=[2.8*cm, None])
        at.setStyle(TableStyle([
            ('BACKGROUND', (0,0),(0,-1), GOLD_D),
            ('BACKGROUND', (1,0),(1,-1), GOLD_L),
            ('BOX',    (0,0),(-1,-1), 0.8, GOLD_B),
            ('VALIGN', (0,0),(-1,-1), 'MIDDLE'),
            ('TOPPADDING',    (0,0),(-1,-1), 8),
            ('BOTTOMPADDING', (0,0),(-1,-1), 8),
            ('LEFTPADDING',   (0,0),(0,-1), 6),
            ('LEFTPADDING',   (1,0),(1,-1), 10),
            ('ROUNDEDCORNERS', [3,3,3,3]),
        ]))
        story.append(at)
        story.append(spacer(0.2))

    story.append(spacer(0.2))

    # Estadísticas clave
    story.append(Paragraph('Alcance del decreto', sSectionTitle))
    stats_data = [
        [Paragraph(b('36,637 ha'), S('sv', fontName='Helvetica-Bold', fontSize=20,
                   textColor=FOREST, leading=24, alignment=TA_CENTER)),
         Paragraph(b('8 municipios'), S('sv', fontName='Helvetica-Bold', fontSize=20,
                   textColor=FOREST, leading=24, alignment=TA_CENTER)),
         Paragraph(b('12 años'), S('sv', fontName='Helvetica-Bold', fontSize=20,
                   textColor=FOREST, leading=24, alignment=TA_CENTER))],
        [Paragraph('Superficie total ZRE', S('sl', fontName='Helvetica', fontSize=7.5,
                   textColor=INK_L, leading=10, alignment=TA_CENTER)),
         Paragraph('Atitalaquia · Atotonilco · Tepeji · Tepetitlán<br/>'
                   'Tezontepec · Tlahuelilpan · Tlaxcoapan · Tula de Allende',
                   S('sl', fontName='Helvetica', fontSize=7, textColor=INK_L, leading=9, alignment=TA_CENTER)),
         Paragraph('Duración máx. de proyectos', S('sl', fontName='Helvetica', fontSize=7.5,
                   textColor=INK_L, leading=10, alignment=TA_CENTER))],
    ]
    stt = Table(stats_data, colWidths=[W/3 - 0.2*cm, W/3 + 0.4*cm, W/3 - 0.2*cm])
    stt.setStyle(TableStyle([
        ('BACKGROUND',  (0,0),(-1,-1), GOLD_L),
        ('BOX',         (0,0),(-1,-1), 0.8, GOLD_B),
        ('INNERGRID',   (0,0),(-1,-1), 0.3, GOLD_I),
        ('TOPPADDING',  (0,0),(-1,0), 10),
        ('BOTTOMPADDING',(0,0),(-1,0), 4),
        ('TOPPADDING',  (0,1),(-1,1), 4),
        ('BOTTOMPADDING',(0,1),(-1,1), 10),
        ('VALIGN',      (0,0),(-1,-1), 'MIDDLE'),
        ('ROUNDEDCORNERS', [4,4,4,4]),
    ]))
    story.append(stt)
    story.append(spacer(0.35))

    # Mapa ZRE
    zre_img_path = os.path.join(os.path.dirname(__file__), 'ZRE.png')
    if os.path.exists(zre_img_path):
        img = RLImage(zre_img_path)
        aspect = img.imageHeight / float(img.imageWidth)
        img.drawWidth  = W
        img.drawHeight = W * aspect
        if img.drawHeight > 10*cm:
            img.drawWidth  = 10*cm / aspect
            img.drawHeight = 10*cm
        story.append(Paragraph(
            'Mapa oficial de la Zona de Restauración Ecológica (DOF 26/09/2024)',
            S('cap', fontName='Helvetica-Oblique', fontSize=8, textColor=INK_L,
              leading=11, alignment=TA_CENTER)))
        story.append(spacer(0.15))
        story.append(img)
        story.append(spacer(0.2))

    story.append(key_box([
        Paragraph(
            f'{b("Implicación práctica:")} las brigadas formadas en este taller están '
            f'respaldadas por mandato federal. SEMARNAT debe publicar el programa de restauración '
            f'con protocolos para municipios de la ZRE.',
            sBody),
    ]))

    doc.build(story, onFirstPage=make_page, onLaterPages=make_page)
    print(f'PDF generado: {OUTPUT}')

if __name__ == '__main__':
    build()
