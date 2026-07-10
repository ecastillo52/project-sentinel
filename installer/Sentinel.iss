; Build this file with Inno Setup after running build-release.ps1.
; The resulting Sentinel-Setup.exe is the only file a recipient needs.

#define MyAppName "Project Sentinel"
#define MyAppVersion "0.7.2"
#define MyAppPublisher "Erik Castillo"
#define MyAppExeName "Sentinel.exe"

[Setup]
AppId={{9418D5B9-9E6B-4A82-A5A0-8AD726F3953A}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Project Sentinel
DefaultGroupName=Project Sentinel
DisableProgramGroupPage=yes
OutputDir=..\release
OutputBaseFilename=Sentinel-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
UninstallDisplayIcon={app}\{#MyAppExeName}
CloseApplications=yes
RestartApplications=no

[Files]
Source: "..\dist\Sentinel.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\Project Sentinel"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\Project Sentinel"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Project Sentinel"; Flags: nowait postinstall skipifsilent
