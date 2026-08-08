; SIAP-RTC Windows installer
; Build with Inno Setup 6 on a Windows build host.

#define AppName "SIAP-RTC"
#define AppVersion "0.1.0"
#define AppPublisher "Coordinación de Comunicación Social"
#define AppExeName "SIAP-RTC.exe"

[Setup]
AppId={{8F2C7D5A-0C0D-4D2D-9E9D-RTC000000001}}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
DefaultDirName={autopf}\SIAP-RTC
DefaultGroupName={#AppName}
OutputDir=output
OutputBaseFilename=SIAP-RTC-Setup-{#AppVersion}
Compression=lzma
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest

[Files]
Source: "..\dist\SIAP-RTC\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\{#AppName}"; Filename: "{app}\{#AppExeName}"
Name: "{autodesktop}\{#AppName}"; Filename: "{app}\{#AppExeName}"

[Dirs]
Name: "{userappdata}\SIAP-RTC"
Name: "{userappdata}\SIAP-RTC\data"
Name: "{userappdata}\SIAP-RTC\imports"
Name: "{userappdata}\SIAP-RTC\reports"
Name: "{userappdata}\SIAP-RTC\logs"
Name: "{userappdata}\SIAP-RTC\backups"

[Run]
Filename: "{app}\{#AppExeName}"; Description: "Iniciar SIAP-RTC"; Flags: nowait postinstall skipifsilent
