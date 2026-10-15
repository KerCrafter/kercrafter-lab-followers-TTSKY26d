#!/usr/bin/env python3
"""Mur des followers KerCrafter Lab : liste des pseudos -> ROM Verilog de l'écran de remerciement.

  python scripts/followers.py add <pseudo>   ajoute un pseudo (validé, sans doublon) puis régénère
  python scripts/followers.py gen            régénère src/credits_rom.v, src/font_rom.v et docs/apercu.png
  python scripts/followers.py check          vérifie que les fichiers générés sont à jour (CI)

Source unique : followers.txt (un pseudo par ligne). Les fichiers Verilog sont générés, ne pas les éditer.
"""
import os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LISTE = os.path.join(ROOT, "followers.txt")
PSEUDO_OK = re.compile(r"^[A-Za-z0-9_]{1,25}$")          # format des pseudos Twitch
COLS, LIGNE_BITS = 40, 7                                    # 40 colonnes de 16 px, jusqu'à 128 lignes de texte

# ---------------------------------------------------------------------------
# Police 8x8 (majuscules, chiffres, quelques signes). Un seul endroit : sert au Verilog ET à l'aperçu PNG.
# ---------------------------------------------------------------------------
G = {
 " ": ["........"]*8,
 "A": ["..###...",".##.##..","##...##.","##...##.","#######.","##...##.","##...##.","........"],
 "B": ["######..","##...##.","##...##.","######..","##...##.","##...##.","######..","........"],
 "C": [".#####..","##...##.","##......","##......","##......","##...##.",".#####..","........"],
 "D": ["#####...","##..##..","##...##.","##...##.","##...##.","##..##..","#####...","........"],
 "E": ["#######.","##......","##......","######..","##......","##......","#######.","........"],
 "F": ["#######.","##......","##......","######..","##......","##......","##......","........"],
 "G": [".#####..","##...##.","##......","##.####.","##...##.","##...##.",".######.","........"],
 "H": ["##...##.","##...##.","##...##.","#######.","##...##.","##...##.","##...##.","........"],
 "I": [".######.","...##...","...##...","...##...","...##...","...##...",".######.","........"],
 "J": ["....###.",".....##.",".....##.",".....##.","##...##.","##...##.",".#####..","........"],
 "K": ["##...##.","##..##..","##.##...","####....","##.##...","##..##..","##...##.","........"],
 "L": ["##......","##......","##......","##......","##......","##......","#######.","........"],
 "M": ["##...##.","###.###.","#######.","##.#.##.","##...##.","##...##.","##...##.","........"],
 "N": ["##...##.","###..##.","####.##.","##.####.","##..###.","##...##.","##...##.","........"],
 "O": [".#####..","##...##.","##...##.","##...##.","##...##.","##...##.",".#####..","........"],
 "P": ["######..","##...##.","##...##.","######..","##......","##......","##......","........"],
 "Q": [".#####..","##...##.","##...##.","##...##.","##.#.##.","##..##..",".###.##.","........"],
 "R": ["######..","##...##.","##...##.","######..","##.##...","##..##..","##...##.","........"],
 "S": [".#####..","##...##.","##......",".#####..",".....##.","##...##.",".#####..","........"],
 "T": ["######..","..##....","..##....","..##....","..##....","..##....","..##....","........"],
 "U": ["##...##.","##...##.","##...##.","##...##.","##...##.","##...##.",".#####..","........"],
 "V": ["##...##.","##...##.","##...##.","##...##.",".##.##..","..###...","...#....","........"],
 "W": ["##...##.","##...##.","##...##.","##.#.##.","#######.","###.###.","##...##.","........"],
 "X": ["##...##.",".##.##..","..###...","..###...","..###...",".##.##..","##...##.","........"],
 "Y": ["##..##..","##..##..","##..##..",".####...","..##....","..##....","..##....","........"],
 "Z": ["#######.",".....##.","....##..","...##...","..##....",".##.....","#######.","........"],
 "0": [".#####..","##...##.","##..###.","##.#.##.","###..##.","##...##.",".#####..","........"],
 "1": ["...##...","..###...",".####...","...##...","...##...","...##...",".######.","........"],
 "2": [".#####..","##...##.",".....##.","...###..",".###....","##......","#######.","........"],
 "3": [".#####..","##...##.",".....##.","..####..",".....##.","##...##.",".#####..","........"],
 "4": ["....##..","...###..","..####..",".##.##..","#######.","....##..","....##..","........"],
 "5": ["#######.","##......","######..",".....##.",".....##.","##...##.",".#####..","........"],
 "6": [".#####..","##......","##......","######..","##...##.","##...##.",".#####..","........"],
 "7": ["#######.",".....##.","....##..","...##...","..##....","..##....","..##....","........"],
 "8": [".#####..","##...##.","##...##.",".#####..","##...##.","##...##.",".#####..","........"],
 "9": [".#####..","##...##.","##...##.",".######.",".....##.",".....##.",".#####..","........"],
 "_": ["........","........","........","........","........","........","#######.","........"],
 "!": ["...##...","...##...","...##...","...##...","...##...","........","...##...","........"],
 "-": ["........","........","........",".#####..","........","........","........","........"],
 ".": ["........","........","........","........","........","........","...##...","........"],
 "~": [".##.##..","#######.","#######.","#######.",".#####..","..###...","...#....","........"],   # cœur
}
CODES = list(G.keys())          # code 6 bits = position dans cette liste ; 0 = espace
assert len(CODES) <= 64

# Couleurs (RRGGBB sur 2 bits chacun) : 0 = fond, puis une couleur par type de ligne
COUL = {"titre": 0b111100, "coeur": 0b110001, "nom": 0b111111, "pied": 0b011011, "rien": 0b111111}

def lire():
    if not os.path.exists(LISTE): return []
    out = []
    with open(LISTE, encoding="utf-8") as fh: contenu = fh.read().splitlines()
    for l in contenu:
        l = l.strip()
        if l and not l.startswith("#"): out.append(l)
    return out

def lignes(noms):
    """Contenu défilant : en-tête, pseudos, pied. Retourne [(texte, type)]."""
    L = [("", "rien"), ("MERCI A NOS FOLLOWERS", "titre"), ("~ ~ ~", "coeur"), ("", "rien")]
    for n in noms: L.append((n.upper(), "nom"))
    L += [("", "rien"), ("GRAVES POUR TOUJOURS", "pied"), ("KERCRAFTER LAB", "titre"), ("", "rien"), ("", "rien")]
    if len(L) > 2 ** LIGNE_BITS:
        raise SystemExit("Trop de pseudos pour la ROM (%d lignes max) : augmente LIGNE_BITS et la taille de tuile." % 2 ** LIGNE_BITS)
    n = 32                                         # au moins 512 px : le texte ne se répète pas à l'écran
    while n < len(L): n *= 2                       # longueur en puissance de 2 : le défilement boucle tout seul
    return L + [("", "rien")] * (n - len(L)), n

def gen():
    noms = lire()
    L, n = lignes(noms)
    nb = max(1, (n - 1).bit_length())
    # --- ROM du texte : seuls les caractères non vides sont listés, le reste vaut "espace"
    cas, coul = [], []
    for i, (t, typ) in enumerate(L):
        if not t: continue
        t = t[:COLS]; x0 = (COLS - len(t)) // 2
        for j, ch in enumerate(t):
            c = CODES.index(ch) if ch in G else CODES.index(" ")
            if c: cas.append("      {%d'd%d, 6'd%d}: code = 6'd%d;   // %s" % (nb, i, x0 + j, c, ch))
        coul.append("      %d'd%d: couleur = 6'b%s;   // %s" % (nb, i, format(COUL[typ], "06b"), t))
    rom = """// GENERE par scripts/followers.py a partir de followers.txt -- ne pas modifier a la main
// %d followers, %d lignes de texte
`default_nettype none
module credits_rom (
  input  wire [6:0] ligne_brute,
  input  wire [5:0] colonne,
  output reg  [5:0] code,
  output reg  [5:0] couleur
);
  // le texte fait %d lignes : on boucle dessus (le defilement fait 128 lignes, multiple de %d)
  wire [%d:0] ligne = ligne_brute[%d:0];
  wire _unused = &{ligne_brute, 1'b0};
  always @(*) begin
    case ({ligne, colonne})
%s
      default: code = 6'd0;
    endcase
    case (ligne)
%s
      default: couleur = 6'b111111;
    endcase
  end
endmodule
""" % (len(noms), n, n, n, nb - 1, nb - 1, "\n".join(cas), "\n".join(coul))
    open(os.path.join(ROOT, "src", "credits_rom.v"), "w", encoding="utf-8").write(rom)
    # --- police
    rows = []
    for c, ch in enumerate(CODES):
        for r, s in enumerate(G[ch]):
            v = int(s.replace(".", "0").replace("#", "1"), 2)
            if v: rows.append("      {6'd%d, 3'd%d}: bits = 8'b%s;" % (c, r, format(v, "08b")))
    font = """// GENERE par scripts/followers.py -- police 8x8 (majuscules, chiffres, _ ! - . et le coeur)
`default_nettype none
module font_rom (
  input  wire [5:0] code,
  input  wire [2:0] rang,
  output reg  [7:0] bits
);
  always @(*) begin
    case ({code, rang})
%s
      default: bits = 8'b0;
    endcase
  end
endmodule
""" % "\n".join(rows)
    open(os.path.join(ROOT, "src", "font_rom.v"), "w", encoding="utf-8").write(font)
    apercu(L)
    return noms

def apercu(L, decalage=0):
    """Image de l'écran (640x480) telle que la puce l'affiche, pour le README et les Pull Requests."""
    try:
        from PIL import Image
    except ImportError:
        return
    W, H = 640, 480
    im = Image.new("RGB", (W, H), (0, 0, 0)); px = im.load()
    def c2(v): return [0, 85, 170, 255][v]
    for y in range(H):
        yy = (y + decalage) % (len(L) * 16)
        li, ry = yy // 16, (yy % 16) // 2
        t, typ = L[li]; t = t[:COLS]; x0 = (COLS - len(t)) // 2
        col = COUL[typ]; rgb = (c2(col >> 4 & 3), c2(col >> 2 & 3), c2(col & 3))
        for x in range(W):
            if (x % 32 == 0 or y % 32 == 0): px[x, y] = (0, 0, 85)             # quadrillage discret
            ci = x // 16 - x0
            if 0 <= ci < len(t) and t[ci] in G and G[t[ci]][ry][(x % 16) // 2] == "#": px[x, y] = rgb
    os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
    im.save(os.path.join(ROOT, "docs", "apercu.png"))

def add(p):
    p = p.strip().lstrip("@")
    if not PSEUDO_OK.match(p):
        print("refuse=format"); return 2
    noms = lire()
    if p.lower() in (n.lower() for n in noms):
        print("ajoute=false"); print("pseudo=" + p); return 0
    with open(LISTE, encoding="utf-8") as fh: fin_ok = fh.read().endswith("\n")
    with open(LISTE, "a", encoding="utf-8") as f:
        if not fin_ok: f.write("\n")
        f.write(p + "\n")
    gen()
    print("ajoute=true"); print("pseudo=" + p); print("total=%d" % (len(noms) + 1))
    return 0

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "gen"
    if cmd == "add": sys.exit(add(sys.argv[2] if len(sys.argv) > 2 else ""))
    if cmd == "gen": print("%d followers" % len(gen())); sys.exit(0)
    if cmd == "check":
        avant = open(os.path.join(ROOT, "src", "credits_rom.v"), encoding="utf-8").read()
        gen()
        sys.exit(0 if avant == open(os.path.join(ROOT, "src", "credits_rom.v"), encoding="utf-8").read() else 1)
    print(__doc__); sys.exit(1)
