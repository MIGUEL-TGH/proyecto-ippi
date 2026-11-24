import sys
# Lee mide.tsv (salida de mide.ps1) y marca texto que se sale de su cuadro y tablas que bajan demasiado.
n_txt = n_tab = 0; malas = []
for l in open(sys.argv[1], encoding="utf-8-sig"):
    p = l.rstrip("\n").split("\t")
    if len(p) < 7: continue
    tipo, sl, nombre, top, alto, bound, lineas = p[0], int(p[1]), p[2], float(p[3]), float(p[4]), float(p[5]), p[6]
    rot = float(p[7]) if len(p) > 7 and p[7] else 0.0
    if rot != 0: continue          # textos verticales de la plantilla
    if tipo == "TXT":
        n_txt += 1
        if bound > alto + 2.5 and nombre not in ("Título",):
            malas.append(f"lámina {sl}: «{nombre}» texto {bound:.0f} pt > cuadro {alto:.0f} pt  (+{bound-alto:.0f})")
        if nombre == "Título" and bound > alto + 2.5:
            malas.append(f"lámina {sl}: TÍTULO desborda ({bound:.0f} > {alto:.0f})")
    else:
        n_tab += 1
        if top + alto > 10.3 * 72:
            malas.append(f"lámina {sl}: tabla termina en {(top+alto)/72:.2f} in (> 10.3)")
print(f"{n_txt} cuadros de texto y {n_tab} tablas revisados; problemas: {len(malas)}")
for m in malas[:60]: print("  ", m)
