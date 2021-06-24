{ lib, buildPythonPackage, dateutil, flask, pymediainfo }:

buildPythonPackage rec {
  pname = "basedapi";
  version = "0.1.0";

  src = ./.;

  checkInputs = [  ];
  propagatedBuildInputs = [ ];

  meta = with lib; {
    homepage = "https://github.com/rpgwaiter/basedapi";
    description = "basedfilehost api";
    license = licenses.gpl3Plus;
    maintainers = with maintainers; [ rpgwaiter ];
  };
}