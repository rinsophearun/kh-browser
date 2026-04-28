; ─────────────────────────────────────────────────────────────────────────────
;  KHBrowser — Inno Setup 6 Installer Script
;  Creates a professional Windows Setup.exe with:
;    ✅ Install wizard with logo
;    ✅ Program Files installation
;    ✅ Desktop + Start Menu shortcuts
;    ✅ Add/Remove Programs entry
;    ✅ Uninstaller
;    ✅ First-run launch option
; ─────────────────────────────────────────────────────────────────────────────

#define AppName      "KH Browser"
#define AppExeName   "KHBrowser.exe"
#define AppVersion   "1.0.0"
#define AppPublisher "KH Browser Team"
#define AppURL       "https://github.com/your-org/kh-browser"
#define AppID        "{{B7C3A1D0-9F4E-4B2A-8C6D-1E5F3A2B0D9C}"

[Setup]
AppId={#AppID}
AppName={#AppName}
AppVersion={#AppVersion}
AppPublisher={#AppPublisher}
AppPublisherURL={#AppURL}
AppSupportURL={#AppURL}/issues
AppUpdatesURL={#AppURL}/releases

; Install location
DefaultDirName={autopf}\{#AppName}
DefaultGroupName={#AppName}
AllowNoIcons=yes

; Output
OutputDir=installer_output
OutputBaseFilename=KHBrowser-{#AppVersion}-Setup-Windows
SetupIconFile=assets\icon.ico

; Compression
Compression=lzma2/ultra64
SolidCompression=yes
LZMAUseSeparateProcess=yes

; UI Options
WizardStyle=modern
WizardSizePercent=120
DisableWelcomePage=no
DisableDirPage=no
DisableProgramGroupPage=no

; Privileges
PrivilegesRequired=admin
PrivilegesRequiredOverridesAllowed=dialog

; Minimum Windows version: Windows 10
MinVersion=10.0

; Code signing (uncomment if you have a certificate)
; SignTool=signtool
; SignedUninstaller=yes

[Languages]
Name: "english";   MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon";    Description: "{cm:CreateDesktopIcon}";  GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunch";    Description: "Add to &Quick Launch bar"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; Main application from PyInstaller dist folder
Source: "dist\KHBrowser\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Assets folder
Source: "assets\*"; DestDir: "{app}\assets"; Flags: ignoreversion recursesubdirs

[Icons]
; Start Menu
Name: "{group}\{#AppName}";                FileName: "{app}\{#AppExeName}";  IconFilename: "{app}\assets\icon.ico"
Name: "{group}\Uninstall {#AppName}";      FileName: "{uninstallexe}";       IconFilename: "{app}\assets\icon.ico"
; Desktop (optional)
Name: "{autodesktop}\{#AppName}";          FileName: "{app}\{#AppExeName}";  IconFilename: "{app}\assets\icon.ico"; Tasks: desktopicon
; Quick Launch (optional, Windows XP/Vista/7)
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#AppName}"; FileName: "{app}\{#AppExeName}"; Tasks: quicklaunch

[Run]
Filename: "{app}\{#AppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(AppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{localappdata}\KHBrowser"

[Registry]
; Add to PATH (optional)
; Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: NeedsAddPath('{app}')

[Code]
// ── Welcome page with custom text ──────────────────────────────────────────
function InitializeSetup(): Boolean;
begin
  Result := True;
end;

procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel2.Caption :=
    'This will install ' + '{#AppName}' + ' version ' + '{#AppVersion}' + ' on your computer.' + #13#10 + #13#10 +
    'KH Browser lets you:' + #13#10 +
    '  • Manage multiple browser profiles with unique fingerprints' + #13#10 +
    '  • Configure proxies per profile' + #13#10 +
    '  • Automate tasks with RPA' + #13#10 +
    '  • Manage teams and sync to cloud' + #13#10 + #13#10 +
    'Click Next to continue.';
end;
