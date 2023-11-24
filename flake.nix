{
  inputs = {
    # I typically use the exact nixpkgs set that I use for building my current
    # system to avoid redundancy.
    nixpkgs.url = "github:dpaetzel/nixpkgs/dpaetzel/nixos-config";
  };

  outputs = { self, nixpkgs }:
    let
      system = "x86_64-linux";
      pkgs = import nixpkgs { inherit system; };
      python = pkgs.python310;
    in rec {
      defaultPackage.${system} = python.pkgs.buildPythonPackage rec {
        pname = "ematools";
        version = "v0.1";

        src = self;

        format = "pyproject";

        propagatedBuildInputs = with python.pkgs; [
          click
          matplotlib
          networkx
          pydot
          pygraphviz
          requests
          toolz
          tqdm
        ];

        meta = with pkgs.lib; {
          description = "Python scripts that interface with emanote";
          license = licenses.gpl3;
        };
      };

      devShell.${system} = pkgs.mkShell {

        # TODO Install graph.py script properly

        shellHook = ''
          export LD_LIBRARY_PATH=${pkgs.xorg.libXxf86vm.out}:$LD_LIBRARY_PATH
        '';

        buildInputs = with python.pkgs;
          [ ipython python ]
          ++ defaultPackage.${system}.propagatedBuildInputs;

      };
    };
}
