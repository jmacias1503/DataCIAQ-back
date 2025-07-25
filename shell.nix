{pkgs ? import <nixpkgs> {}}:
pkgs.mkShell {
  buildInputs = with pkgs; [
    python312
    python312Packages.annotated-types
    python312Packages.anyio
    python312Packages.click
    python312Packages.dnspython
    python312Packages.et_xmlfile
    python312Packages.fastapi
    python312Packages.h11
    python312Packages.idna
    python312Packages.motor
    python312Packages.numpy
    python312Packages.openpyxl
    python312Packages.pandas
    python312Packages.pydantic
    python312Packages.pydantic-core
    python312Packages.pymongo
    python312Packages.python-dateutil
    python312Packages.python-dotenv
    python312Packages.pytz
    python312Packages.six
    python312Packages.sniffio
    python312Packages.starlette
    python312Packages.typing-inspect
    python312Packages.typing-extensions
    python312Packages.tzdata
    python312Packages.uvicorn
  ];

  shellHook = ''
    echo "Entorno de desarrollo Python para FastAPI"
    # Opcional: Configura variables de entorno si son necesarias
  '';
}
