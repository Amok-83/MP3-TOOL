; MP3 Album Tool - NSIS Installer Script
; ======================================

!define APPNAME "MP3 Album Tool"
!define COMPANYNAME "MP3 Album Tool"
!define DESCRIPTION "Ferramenta para organizar e editar metadados de álbuns MP3"
!define VERSIONMAJOR 1
!define VERSIONMINOR 0
!define VERSIONBUILD 0
!define HELPURL "https://github.com/mp3albumtool"
!define UPDATEURL "https://github.com/mp3albumtool/releases"
!define ABOUTURL "https://github.com/mp3albumtool"
!define INSTALLSIZE 50000

RequestExecutionLevel admin
InstallDir "$PROGRAMFILES\${APPNAME}"
LicenseData "LICENSE.txt"
Name "${APPNAME}"
Icon "icon.ico"
outFile "MP3AlbumTool_Setup.exe"

!include LogicLib.nsh

page license
page directory
page instfiles

!macro VerifyUserIsAdmin
UserInfo::GetAccountType
pop $0
${If} $0 != "admin"
    messageBox mb_iconstop "Privilégios de administrador são necessários!"
    setErrorLevel 740
    quit
${EndIf}
!macroend

function .onInit
    setShellVarContext all
    !insertmacro VerifyUserIsAdmin
functionEnd

section "install"
    setOutPath $INSTDIR
    
    # Ficheiros da aplicação
    file "dist\MP3AlbumTool.exe"
    file "README.md"
    file "LICENSE.txt"
    
    # Scripts de desinstalação
    file "MP3AlbumTool_Uninstaller.ps1"
    file "DesinstalarMP3AlbumTool.bat"
    file "DesinstalarMP3AlbumTool_Simples.bat"
    
    # Criar atalho no desktop
    createShortCut "$DESKTOP\${APPNAME}.lnk" "$INSTDIR\MP3AlbumTool.exe" "" "$INSTDIR\MP3AlbumTool.exe"
    
    # Criar atalho no menu iniciar
    createDirectory "$SMPROGRAMS\${APPNAME}"
    createShortCut "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk" "$INSTDIR\MP3AlbumTool.exe" "" "$INSTDIR\MP3AlbumTool.exe"
    createShortCut "$SMPROGRAMS\${APPNAME}\Desinstalar.lnk" "$INSTDIR\uninstall.exe" "" "$INSTDIR\uninstall.exe"
    createShortCut "$SMPROGRAMS\${APPNAME}\Desinstalar (PowerShell).lnk" "$INSTDIR\DesinstalarMP3AlbumTool.bat" "" "$INSTDIR\DesinstalarMP3AlbumTool.bat"
    createShortCut "$SMPROGRAMS\${APPNAME}\Desinstalar (Simples).lnk" "$INSTDIR\DesinstalarMP3AlbumTool_Simples.bat" "" "$INSTDIR\DesinstalarMP3AlbumTool_Simples.bat"
    
    # Registar no sistema
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayName" "${APPNAME}"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "InstallLocation" "$\"$INSTDIR$\""
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayIcon" "$\"$INSTDIR\MP3AlbumTool.exe$\""
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "Publisher" "${COMPANYNAME}"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "HelpLink" "${HELPURL}"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLUpdateInfo" "${UPDATEURL}"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "URLInfoAbout" "${ABOUTURL}"
    writeRegStr HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "DisplayVersion" "${VERSIONMAJOR}.${VERSIONMINOR}.${VERSIONBUILD}"
    writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMajor" ${VERSIONMAJOR}
    writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "VersionMinor" ${VERSIONMINOR}
    writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoModify" 1
    writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "NoRepair" 1
    writeRegDWORD HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}" "EstimatedSize" ${INSTALLSIZE}
    
    # Criar desinstalador
    writeUninstaller "$INSTDIR\uninstall.exe"
sectionEnd

section "uninstall"
    # Remover ficheiros
    delete "$INSTDIR\MP3AlbumTool.exe"
    delete "$INSTDIR\README.md"
    delete "$INSTDIR\LICENSE.txt"
    delete "$INSTDIR\uninstall.exe"
    
    # Remover scripts de desinstalação
    delete "$INSTDIR\MP3AlbumTool_Uninstaller.ps1"
    delete "$INSTDIR\DesinstalarMP3AlbumTool.bat"
    delete "$INSTDIR\DesinstalarMP3AlbumTool_Simples.bat"
    
    # Remover atalhos
    delete "$DESKTOP\${APPNAME}.lnk"
    delete "$SMPROGRAMS\${APPNAME}\${APPNAME}.lnk"
    delete "$SMPROGRAMS\${APPNAME}\Desinstalar.lnk"
    delete "$SMPROGRAMS\${APPNAME}\Desinstalar (PowerShell).lnk"
    delete "$SMPROGRAMS\${APPNAME}\Desinstalar (Simples).lnk"
    rmDir "$SMPROGRAMS\${APPNAME}"
    
    # Remover pasta de instalação
    rmDir "$INSTDIR"
    
    # Remover do registo
    deleteRegKey HKLM "Software\Microsoft\Windows\CurrentVersion\Uninstall\${APPNAME}"
sectionEnd