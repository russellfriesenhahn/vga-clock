`default_nettype none
module cmdProc (
    input wire Clk,
    input wire Rst,
    input wire [7:0] Data,
    input wire       DataValid,
    output reg       CmdWrite,
    output reg       CmdRead,
    output reg [7:0] CmdAddr,
    output reg [7:0] CmdWriteData
);

    // ------------------------------------------------------------------------
    // Command Processing
    // ------------------------------------------------------------------------

    localparam STATE_CMD_IDLE   = 0;
    localparam STATE_ADDR       = 1;
    localparam STATE_WRITE      = 2;
    localparam STATE_READ       = 3;

    reg [2:0]   cmd_state;
    reg [7:0]   cmdByte;

    always @(posedge Clk) begin
        if (Rst == 1'b1) begin
            cmd_state <= STATE_CMD_IDLE;
            CmdWrite <= 0;
            CmdRead <= 0;
        end else begin

            case (cmd_state)
                STATE_CMD_IDLE: begin
                    CmdWrite <= 0;
                    CmdRead <= 0;
                    if (DataValid == 1'b1) begin
                        cmdByte <= Data;
                        cmd_state <= STATE_ADDR;
                    end
                end
                STATE_ADDR: begin
                    if (DataValid == 1'b1) begin
                        CmdAddr <= Data;
                        if (cmdByte == 8'h02) begin
                            cmd_state <= STATE_WRITE;
                        end else begin
                            cmd_state <= STATE_READ;
                        end
                    end
                end
                STATE_WRITE: begin
                    if (DataValid == 1'b1) begin
                        CmdWriteData <= Data;
                        CmdWrite <= 1'b1;
                        cmd_state <= STATE_CMD_IDLE;
                    end
                end
                STATE_READ: begin
                end
                default: begin
                    cmd_state <= STATE_CMD_IDLE;
                end
            endcase
        end
    end
endmodule
`default_nettype wire 
