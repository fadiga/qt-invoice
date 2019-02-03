﻿; Turn off old selected section
; 10 2019: IBS-Mali

; -------------------------------
; Start

  !define MUI_PRODUCT "Invoice"
  !define MUI_FILE "main"
  !define MUI_VERSION "0.4-beta"
  !define MUI_BRANDINGTEXT "${MUI_PRODUCT} ${MUI_VERSION}"
  !define IMAGES "img"
  !define TEMPLATE "template"
  ;CRCCheck On

  !include "${NSISDIR}\Contrib\Modern UI\System.nsh"


;---------------------------------
;General

  OutFile "Install-${MUI_PRODUCT}-${MUI_VERSION}.exe"
  ShowInstDetails "nevershow"
  ShowUninstDetails "nevershow"
  ;SetCompressor off

  !define MUI_ICON "logo.ico"
  !define MUI_UNICON "logo.ico"
  !define MUI_SPECIALBITMAP "Bitmap.bmp"

;--------------------------------
;Folder selection page

  InstallDir "C:\${MUI_PRODUCT}"
;--------------------------------
;Data
    ;LicenseData "README.txt"
;--------------------------------
;Installer Sections
;Section "install" Installation info
Section "install"

;Add files
  SetOutPath "$INSTDIR"

  ;File "${MUI_FILE}.exe"
  ;File "README.txt"

  ;List of files/folders to copy
  File /r dist\*.*
  File /r ${IMAGES}
  File /r ${TEMPLATE}

;create desktop shortcut
  CreateShortCut "$DESKTOP\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" parameters "$INSTDIR\${IMAGES}\${MUI_ICON}"

;create start-menu items
  CreateDirectory "$SMPROGRAMS\${MUI_PRODUCT}"
  CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\Uninstall.lnk" "$INSTDIR\Uninstall.exe" "" "$INSTDIR\${IMAGES}\${MUI_ICON}" 0
  CreateShortCut "$SMPROGRAMS\${MUI_PRODUCT}\${MUI_PRODUCT}.lnk" "$INSTDIR\${MUI_FILE}.exe" "" "$INSTDIR\${IMAGES}\${MUI_ICON}" 0

;write uninstall information to the registry
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "DisplayName" "${MUI_PRODUCT} (remove only)"
  WriteRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}" "UninstallString" "$INSTDIR\Uninstall.exe"

  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd


;--------------------------------
;Uninstaller Section
Section "Uninstall"

;Delete Files
;  RMDir /r "$INSTDIR\*.*"

;Remove the installation directory
;  RMDir "$INSTDIR"

# now delete installed file
delete $INSTDIR\*.exe
delete $INSTDIR\*.dll
delete $INSTDIR\*.lib
delete $INSTDIR\*.zip
delete $INSTDIR\*.pdf
delete $INSTDIR\*.json
delete $INSTDIR\*.pyd

RMDir /r $INSTDIR\build
RMDir /r $INSTDIR\${IMAGES}
RMDir /r $INSTDIR\dist
RMDir /r $INSTDIR\tcl

;Delete Start Menu Shortcuts
  Delete "$DESKTOP\${MUI_PRODUCT}.lnk"
  Delete "$SMPROGRAMS\${MUI_PRODUCT}\*.*"
  RmDir  "$SMPROGRAMS\${MUI_PRODUCT}"

;Delete Uninstaller And Unistall Registry Entries
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\${MUI_PRODUCT}"
  DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\${MUI_PRODUCT}"

SectionEnd

;--------------------------------
Function .onInstSuccess
  ;MessageBox MB_OK "Vous avez installé le ${MUI_PRODUCT}.Utilise son icon sur le ;bureau pour lancer le program."

   SetOutPath $INSTDIR
   ExecShell "" '"$INSTDIR\${MUI_FILE}.exe"'
FunctionEnd

Function un.onUninstSuccess
  MessageBox MB_OK "You have successfully uninstalled ${MUI_PRODUCT}."
FunctionEnd

;eof