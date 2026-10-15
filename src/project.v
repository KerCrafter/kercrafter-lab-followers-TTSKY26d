/*
 * KerCrafter Lab — mur des followers
 * Écran de remerciement VGA 640x480 : les pseudos des followers défilent comme un générique de fin.
 * Sortie : Pmod TinyVGA sur uo_out. Entrées : ui_in[0] = pause, ui_in[1] = défilement rapide.
 * La liste des pseudos est dans followers.txt ; src/credits_rom.v et src/font_rom.v sont générés.
 */
`default_nettype none

module tt_um_kercrafter_followers (
  input  wire [7:0] ui_in,
  output wire [7:0] uo_out,
  input  wire [7:0] uio_in,
  output wire [7:0] uio_out,
  output wire [7:0] uio_oe,
  input  wire       ena,
  input  wire       clk,
  input  wire       rst_n
);
  localparam LB = 7;                    // jusqu'à 128 lignes de texte (la ROM boucle sur sa propre longueur)
  localparam SB = LB + 4;               // bits du défilement (16 px par ligne)

  wire hsync, vsync, video;
  wire [9:0] x, y;
  hvsync_generator vga (.clk(clk), .reset(~rst_n), .hsync(hsync), .vsync(vsync),
                        .display_on(video), .hpos(x), .vpos(y));

  /* défilement : +1 ou +2 px par image, au début de la synchro verticale */
  reg [SB-1:0] scroll;
  reg vsync_q;
  always @(posedge clk) begin
    if (!rst_n) begin scroll <= 0; vsync_q <= 1'b1; end
    else begin
      vsync_q <= vsync;
      if (vsync_q && !vsync && !ui_in[0]) scroll <= scroll + (ui_in[1] ? 11'd2 : 11'd1);
    end
  end

  wire [SB-1:0] yy = {1'b0, y} + scroll;        // y de l'écran + défilement (boucle sur la hauteur du texte)
  wire [LB-1:0] ligne   = yy[SB-1:4];
  wire [2:0]    rang    = yy[3:1];        // police 8x8 affichée en x2
  wire [5:0]    colonne = x[9:4];
  wire [2:0]    bitx    = x[3:1];

  wire [5:0] code, couleur;
  wire [7:0] motif;
  credits_rom texte (.ligne_brute(ligne), .colonne(colonne), .code(code), .couleur(couleur));
  font_rom    police (.code(code), .rang(rang), .bits(motif));

  wire pixel  = motif[3'd7 - bitx];
  wire grille = (x[4:0] == 5'd0) || (y[4:0] == 5'd0);

  reg [1:0] R, G, B;
  always @(posedge clk) begin
    if (!rst_n || !video) {R, G, B} <= 6'd0;
    else if (pixel)       {R, G, B} <= couleur;
    else if (grille)      {R, G, B} <= 6'b000001;    // quadrillage bleu discret
    else                  {R, G, B} <= 6'd0;
  end

  /* Pmod TinyVGA */
  assign uo_out  = {hsync, B[0], G[0], R[0], vsync, B[1], G[1], R[1]};
  assign uio_out = 8'd0;
  assign uio_oe  = 8'd0;
  wire _unused = &{ena, uio_in, ui_in[7:2], yy[0], 1'b0};
endmodule
