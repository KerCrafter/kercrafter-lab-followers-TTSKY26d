<!--
Fiche du projet pour la documentation Tiny Tapeout.
-->

## How it works

**KerCrafter Lab — followers wall.** A VGA "thank you" screen (640×480 @ 60 Hz) on which the names of
the KerCrafter Lab Twitch channel followers scroll like movie end credits.

Each time someone follows the channel during a live stream, the stream overlay calls the GitHub API:
a workflow adds the name to `followers.txt`, regenerates the text ROM (`src/credits_rom.v`) and the
8×8 font ROM (`src/font_rom.v`), runs the cocotb tests and opens a pull request. Every follower is
literally engraved in the silicon.

The design is a classic character generator: a VGA sync generator, a 40×N text ROM (16×16 px cells,
8×8 font doubled), a vertical scroll register updated every frame, and a faint blue grid background.

## How to test

Connect a [TinyVGA Pmod](https://github.com/mole99/tiny-vga) to the output pins and a VGA monitor,
set the clock to 25.175 MHz and release reset. The names scroll at 60 px/s.

- `ui_in[0]` = pause
- `ui_in[1]` = fast scroll (2 px per frame)

## External hardware

TinyVGA Pmod on the dedicated outputs, VGA monitor.
