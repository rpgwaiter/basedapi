{ lib, buildPythonApplication, dateutil, flask, flask-cors, flask-caching, pymediainfo, setuptools }:

buildPythonApplication rec {
  pname = "basedapi";
  version = "0.1.0";

  src = ./.;

  checkInputs = [  ];
  propagatedBuildInputs = [ pymediainfo setuptools flask flask-cors flask-caching ];

  meta = with lib; {
    homepage = "https://github.com/rpgwaiter/basedapi";
    description = "basedfilehost api";
    license = licenses.gpl3Plus;
    maintainers = with maintainers; [ rpgwaiter ];
  };
}