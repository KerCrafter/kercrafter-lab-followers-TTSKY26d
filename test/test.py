# SPDX-FileCopyrightText: © 2026 KerCrafter Lab
# SPDX-License-Identifier: Apache-2.0
#
# Tests du mur des followers. Uniquement par les broches de sortie (aussi valable en test "gate level") :
#  - synchros VGA 640x480 @ 60 Hz
#  - les 64 premieres lignes de l'image sont identiques, pixel par pixel, au modele Python
#    (scripts/followers.py, celui qui dessine docs/apercu.png)
import os, sys
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, FallingEdge

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import followers as F

H_TOTAL, V_TOTAL = 800, 525


def rgb(uo):
    r = ((uo >> 0) & 1) << 1 | ((uo >> 4) & 1)
    g = ((uo >> 1) & 1) << 1 | ((uo >> 5) & 1)
    b = ((uo >> 2) & 1) << 1 | ((uo >> 6) & 1)
    return r << 4 | g << 2 | b


def attendu(L, x, y):
    yy = y % (len(L) * 16)
    t, typ = L[yy // 16]
    t = t[:F.COLS]
    x0 = (F.COLS - len(t)) // 2
    ci = x // 16 - x0
    if 0 <= ci < len(t) and F.G[t[ci]][(yy % 16) // 2][(x % 16) // 2] == "#":
        return F.COUL[typ]
    return 0b000001 if (x % 32 == 0 or y % 32 == 0) else 0


async def demarrer(dut):
    cocotb.start_soon(Clock(dut.clk, 40, unit="ns").start())   # ~25 MHz
    dut.ena.value = 1
    dut.ui_in.value = 1          # pause : le texte reste immobile pendant le test
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1


async def lire(dut):
    await FallingEdge(dut.clk)
    return int(dut.uo_out.value)


@cocotb.test()
async def test_synchros(dut):
    await demarrer(dut)
    uo = await lire(dut)
    while not (uo >> 7) & 1:                  # sortir d'une éventuelle synchro en cours
        uo = await lire(dut)
    while (uo >> 7) & 1:                      # attendre le début d'une synchro horizontale
        uo = await lire(dut)
    bas = 0
    for _ in range(H_TOTAL):
        if not (uo >> 7) & 1:
            bas += 1
        uo = await lire(dut)
    assert bas == 96, "hsync doit durer 96 pixels (mesuré : %d)" % bas
    assert not (uo >> 7) & 1, "période horizontale différente de 800 pixels"


@cocotb.test()
async def test_texte(dut):
    await demarrer(dut)
    L, _ = F.lignes(F.lire())
    # repère : le premier échantillon où vsync passe à 0 correspond au compteur (ligne 490, pixel 1)
    uo = await lire(dut)
    while not (uo >> 3) & 1:
        uo = await lire(dut)
    while (uo >> 3) & 1:
        uo = await lire(dut)
    c = 490 * H_TOTAL + 1
    total = H_TOTAL * V_TOTAL
    erreurs, allumes = 0, 0
    fin = (V_TOTAL - 490 + 64) * H_TOTAL
    for _ in range(fin):
        p = (c - 1) % total                    # la couleur sort un cycle après la position
        x, y = p % H_TOTAL, p // H_TOTAL
        if x < 640 and y < 64:
            v, a = rgb(uo), attendu(L, x, y)
            if v != a:
                erreurs += 1
            if v not in (0, 1):
                allumes += 1
        uo = await lire(dut)
        c += 1
    assert allumes > 500, "aucun texte affiché"
    assert erreurs == 0, "%d pixels différents du modèle" % erreurs
