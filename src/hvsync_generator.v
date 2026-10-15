// Balayage VGA 640x480 @ 60 Hz (horloge pixel 25,175 MHz). Synchros actives à l'état bas.
`default_nettype none
module hvsync_generator (
  input  wire       clk,
  input  wire       reset,
  output reg        hsync,
  output reg        vsync,
  output wire       display_on,
  output reg  [9:0] hpos,
  output reg  [9:0] vpos
);
  localparam H_DISPLAY = 640, H_FRONT = 16, H_SYNC = 96, H_BACK = 48;
  localparam V_DISPLAY = 480, V_FRONT = 10, V_SYNC = 2,  V_BACK = 33;
  localparam H_MAX = H_DISPLAY + H_FRONT + H_SYNC + H_BACK - 1;   // 799
  localparam V_MAX = V_DISPLAY + V_FRONT + V_SYNC + V_BACK - 1;   // 524

  wire hmaxxed = (hpos == H_MAX) || reset;
  wire vmaxxed = (vpos == V_MAX) || reset;

  always @(posedge clk) begin
    hsync <= ~(hpos >= H_DISPLAY + H_FRONT && hpos < H_DISPLAY + H_FRONT + H_SYNC);
    if (hmaxxed) hpos <= 0; else hpos <= hpos + 1;
  end
  always @(posedge clk) begin
    vsync <= ~(vpos >= V_DISPLAY + V_FRONT && vpos < V_DISPLAY + V_FRONT + V_SYNC);
    if (hmaxxed) begin
      if (vmaxxed) vpos <= 0; else vpos <= vpos + 1;
    end
  end
  assign display_on = (hpos < H_DISPLAY) && (vpos < V_DISPLAY);
endmodule
