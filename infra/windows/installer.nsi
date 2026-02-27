Outfile "ggtesla-setup.exe"
InstallDir "$PROGRAMFILES\\GGTesla"
Page directory
Page instfiles
Section "Install"
  SetOutPath "$INSTDIR"
  File "..\\..\\apps\\windows\\src\\main.ps1"
SectionEnd
