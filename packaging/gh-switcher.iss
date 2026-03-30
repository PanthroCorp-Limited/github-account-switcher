; Inno Setup script for gh-switcher
; Build with: ISCC /DMyAppVersion=1.2.3 packaging\gh-switcher.iss

#ifndef MyAppVersion
  #define MyAppVersion "0.0.0"
#endif

[Setup]
AppName=GitHub Account Switcher
AppVersion={#MyAppVersion}
AppPublisher=Panthrocorp
AppPublisherURL=https://github.com/PanthroCorp-Limited/github-account-switcher
AppSupportURL=https://github.com/PanthroCorp-Limited/github-account-switcher/issues
AppUpdatesURL=https://github.com/PanthroCorp-Limited/github-account-switcher/releases
DefaultDirName={userpf}\gh-switcher
DefaultGroupName=GitHub Account Switcher
DisableProgramGroupPage=yes
OutputDir=Output
OutputBaseFilename=GhSwitcherSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "autostart"; Description: "Start automatically at login"; GroupDescription: "Startup options:"

[Files]
Source: "..\dist\gh-switcher\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\GitHub Account Switcher"; Filename: "{app}\gh-switcher.exe"
Name: "{group}\{cm:UninstallProgram,GitHub Account Switcher}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\GitHub Account Switcher"; Filename: "{app}\gh-switcher.exe"; Tasks: desktopicon

[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "GhSwitcher"; ValueData: "{app}\gh-switcher.exe"; Flags: uninsdeletevalue; Tasks: autostart

[Run]
Filename: "{app}\gh-switcher.exe"; Description: "{cm:LaunchProgram,GitHub Account Switcher}"; Flags: nowait postinstall skipifsilent
