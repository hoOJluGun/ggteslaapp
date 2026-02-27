OutFile "GGTeslaInstaller.exe"
InstallDir "$PROGRAMFILES\GGTesla"

Section
  SetOutPath $INSTDIR
  WriteUninstaller "$INSTDIR\uninstall.exe"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\uninstall.exe"
  RMDir $INSTDIR
SectionEnd
