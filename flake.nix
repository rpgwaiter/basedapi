{
  inputs = {
    nixpkgs.url = "nixpkgs/nixos-unstable";
    devshell.url = "github:numtide/devshell";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, devshell, flake-utils }: let
    pkgs = import nixpkgs { system = "x86_64-linux"; };
  in
    flake-utils.lib.eachDefaultSystem (system: {
      devShell =
        let pkgs = import nixpkgs {
          inherit system;

          overlays = [ devshell.overlay ];
        };
        in
        pkgs.devshell.mkShell {
          imports = [ (pkgs.devshell.importTOML ./devshell.toml) ];
        };
    }) // rec {
      packages.x86_64-linux = rec {
        basedapi = pkgs.callPackage ./default.nix { 
          inherit (pkgs) lib dateutil;
          inherit (pkgs.python39Packages) buildPythonApplication setuptools flask-cors flask-caching pymediainfo flask;
        };
      };
      defaultPackage.x86_64-linux = packages.x86_64-linux.basedapi;

      nixosModules.basedapi = import ./nixos;
      nixosModule = nixosModules.basedapi;
    };
}
