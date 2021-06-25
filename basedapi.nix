{ lib, pkgs, config, ... }:
with lib;                      
let
  cfg = config.services.basedapi;
in {
  options.services.basedapi = {
    enable = mkEnableOption "basedapi service";
    pythonPackage = mkOption {
      type = types.str;
      default = "pkgs.python39";
      example = "pkgs.python3";
    };
  };

  config = mkIf cfg.enable {
    systemd.services.basedapi = {
      wantedBy = [ "multi-user.target" ];
      serviceConfig = {
          ExecStart = "${cfg.pythonPackage}/bin/python ${escapeShellArg pkgs.basedapi}";
      };
    };
  };
}