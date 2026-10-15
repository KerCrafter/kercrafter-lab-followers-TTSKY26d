// GENERE par scripts/followers.py a partir de followers.txt -- ne pas modifier a la main
// 3 followers, 32 lignes de texte
`default_nettype none
module credits_rom (
  input  wire [6:0] ligne_brute,
  input  wire [5:0] colonne,
  output reg  [5:0] code,
  output reg  [5:0] couleur
);
  // le texte fait 32 lignes : on boucle dessus (le defilement fait 128 lignes, multiple de 32)
  wire [4:0] ligne = ligne_brute[4:0];
  wire _unused = &{ligne_brute, 1'b0};
  always @(*) begin
    case ({ligne, colonne})
      {5'd1, 6'd9}: code = 6'd13;   // M
      {5'd1, 6'd10}: code = 6'd5;   // E
      {5'd1, 6'd11}: code = 6'd18;   // R
      {5'd1, 6'd12}: code = 6'd3;   // C
      {5'd1, 6'd13}: code = 6'd9;   // I
      {5'd1, 6'd15}: code = 6'd1;   // A
      {5'd1, 6'd17}: code = 6'd14;   // N
      {5'd1, 6'd18}: code = 6'd15;   // O
      {5'd1, 6'd19}: code = 6'd19;   // S
      {5'd1, 6'd21}: code = 6'd6;   // F
      {5'd1, 6'd22}: code = 6'd15;   // O
      {5'd1, 6'd23}: code = 6'd12;   // L
      {5'd1, 6'd24}: code = 6'd12;   // L
      {5'd1, 6'd25}: code = 6'd15;   // O
      {5'd1, 6'd26}: code = 6'd23;   // W
      {5'd1, 6'd27}: code = 6'd5;   // E
      {5'd1, 6'd28}: code = 6'd18;   // R
      {5'd1, 6'd29}: code = 6'd19;   // S
      {5'd2, 6'd17}: code = 6'd41;   // ~
      {5'd2, 6'd19}: code = 6'd41;   // ~
      {5'd2, 6'd21}: code = 6'd41;   // ~
      {5'd4, 6'd16}: code = 6'd11;   // K
      {5'd4, 6'd17}: code = 6'd5;   // E
      {5'd4, 6'd18}: code = 6'd18;   // R
      {5'd4, 6'd19}: code = 6'd20;   // T
      {5'd4, 6'd20}: code = 6'd5;   // E
      {5'd4, 6'd21}: code = 6'd19;   // S
      {5'd4, 6'd22}: code = 6'd20;   // T
      {5'd5, 6'd12}: code = 6'd11;   // K
      {5'd5, 6'd13}: code = 6'd5;   // E
      {5'd5, 6'd14}: code = 6'd18;   // R
      {5'd5, 6'd15}: code = 6'd2;   // B
      {5'd5, 6'd16}: code = 6'd12;   // L
      {5'd5, 6'd17}: code = 6'd1;   // A
      {5'd5, 6'd18}: code = 6'd2;   // B
      {5'd5, 6'd19}: code = 6'd12;   // L
      {5'd5, 6'd20}: code = 6'd1;   // A
      {5'd5, 6'd21}: code = 6'd20;   // T
      {5'd5, 6'd22}: code = 6'd5;   // E
      {5'd5, 6'd23}: code = 6'd19;   // S
      {5'd5, 6'd24}: code = 6'd20;   // T
      {5'd5, 6'd25}: code = 6'd5;   // E
      {5'd5, 6'd26}: code = 6'd18;   // R
      {5'd6, 6'd14}: code = 6'd11;   // K
      {5'd6, 6'd15}: code = 6'd5;   // E
      {5'd6, 6'd16}: code = 6'd18;   // R
      {5'd6, 6'd17}: code = 6'd2;   // B
      {5'd6, 6'd18}: code = 6'd12;   // L
      {5'd6, 6'd19}: code = 6'd1;   // A
      {5'd6, 6'd20}: code = 6'd20;   // T
      {5'd6, 6'd21}: code = 6'd5;   // E
      {5'd6, 6'd22}: code = 6'd19;   // S
      {5'd6, 6'd23}: code = 6'd20;   // T
      {5'd6, 6'd24}: code = 6'd5;   // E
      {5'd6, 6'd25}: code = 6'd18;   // R
      {5'd8, 6'd10}: code = 6'd7;   // G
      {5'd8, 6'd11}: code = 6'd18;   // R
      {5'd8, 6'd12}: code = 6'd1;   // A
      {5'd8, 6'd13}: code = 6'd22;   // V
      {5'd8, 6'd14}: code = 6'd5;   // E
      {5'd8, 6'd15}: code = 6'd19;   // S
      {5'd8, 6'd17}: code = 6'd16;   // P
      {5'd8, 6'd18}: code = 6'd15;   // O
      {5'd8, 6'd19}: code = 6'd21;   // U
      {5'd8, 6'd20}: code = 6'd18;   // R
      {5'd8, 6'd22}: code = 6'd20;   // T
      {5'd8, 6'd23}: code = 6'd15;   // O
      {5'd8, 6'd24}: code = 6'd21;   // U
      {5'd8, 6'd25}: code = 6'd10;   // J
      {5'd8, 6'd26}: code = 6'd15;   // O
      {5'd8, 6'd27}: code = 6'd21;   // U
      {5'd8, 6'd28}: code = 6'd18;   // R
      {5'd8, 6'd29}: code = 6'd19;   // S
      {5'd9, 6'd13}: code = 6'd11;   // K
      {5'd9, 6'd14}: code = 6'd5;   // E
      {5'd9, 6'd15}: code = 6'd18;   // R
      {5'd9, 6'd16}: code = 6'd3;   // C
      {5'd9, 6'd17}: code = 6'd18;   // R
      {5'd9, 6'd18}: code = 6'd1;   // A
      {5'd9, 6'd19}: code = 6'd6;   // F
      {5'd9, 6'd20}: code = 6'd20;   // T
      {5'd9, 6'd21}: code = 6'd5;   // E
      {5'd9, 6'd22}: code = 6'd18;   // R
      {5'd9, 6'd24}: code = 6'd12;   // L
      {5'd9, 6'd25}: code = 6'd1;   // A
      {5'd9, 6'd26}: code = 6'd2;   // B
      default: code = 6'd0;
    endcase
    case (ligne)
      5'd1: couleur = 6'b111100;   // MERCI A NOS FOLLOWERS
      5'd2: couleur = 6'b110001;   // ~ ~ ~
      5'd4: couleur = 6'b111111;   // KERTEST
      5'd5: couleur = 6'b111111;   // KERBLABLATESTER
      5'd6: couleur = 6'b111111;   // KERBLATESTER
      5'd8: couleur = 6'b011011;   // GRAVES POUR TOUJOURS
      5'd9: couleur = 6'b111100;   // KERCRAFTER LAB
      default: couleur = 6'b111111;
    endcase
  end
endmodule
