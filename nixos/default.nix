
{ lib, pkgs, config }:
with lib;                      
let
    cfg = config.services.basedapi;
in 
{
    options.services.basedapi = {
    enable = mkEnableOption "basedapi service";
    };

    config = mkIf cfg.enable {
    systemd.services.basedapi = {
        wantedBy = [ "multi-user.target" ];
        serviceConfig = {
            ExecStart = "${pkgs.basedapi}/bin/basedapi";
        };
    };
}