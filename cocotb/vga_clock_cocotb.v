
`default_nettype none
module vga_clock_cocotb(
    input wire CSPI_sys_clk,
    input wire clk, 
    input wire reset_n,
    input wire adj_hrs,
    input wire adj_min,
    input wire adj_sec,
    input wire SPI_clk,
    input wire SPI_csb,
    input wire SPI_copi,
    output wire SPI_cipo,
    output wire hsync,
    output wire vsync,
    output wire [5:0] rrggbb
);
    
    vga_clock i_vga_clock (
        .clk    (clk ),
        .reset_n(reset_n),
        .adj_hrs(adj_hrs),
        .adj_min(adj_min),
        .adj_sec(adj_sec),
        .SPI_clk(SPI_clk),
        .SPI_csb(SPI_csb),
        .SPI_copi(SPI_copi),
        .SPI_cipo(SPI_cipo),
        .hsync  (hsync  ),
        .vsync  (vsync  ),
        .rrggbb (rrggbb )
    );

    `ifdef COCOTB_SIM
    initial begin
        $dumpfile("vga-clock_cocotb.lxt2");
        $dumpvars;
    end
    `endif
endmodule
`default_nettype wire
