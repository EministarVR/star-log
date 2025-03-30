; -- installer.iss --
; Inno Setup-Skript für StarLog

[Setup]
AppName=StarLog
AppVersion=1.0
AppPublisher=Eministar Dev Group n.e.V.
AppPublisherURL=https://discord.gg/ErFRp9eSrj
AppSupportURL=https://discord.gg/ErFRp9eSrj
AppUpdatesURL=https://discord.gg/ErFRp9eSrj
DisableProgramGroupPage=yes
DisableDirPage=no
DisableReadyPage=no
DisableFinishedPage=no
DefaultDirName={pf}\EministarDev\StarLog
DefaultGroupName=StarLog
OutputDir=.\Output
OutputBaseFilename=StarLog-Setup
Compression=lzma2
SolidCompression=yes
SetupIconFile=.\assets\star_logo.ico
WizardImageFile=.\assets\setup_banner.bmp
WizardSmallImageFile=.\assets\small_logo.bmp
LicenseFile=.\assets\agb.txt
UninstallDisplayIcon={app}\starlog.exe

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1

[Files]
Source: ".\dist\starlog.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: ".\assets\agb.txt"; DestDir: "{app}"; Flags: ignoreversion


[Icons]
Name: "{group}\StarLog"; Filename: "{app}\starlog.exe"
Name: "{group}\{cm:UninstallProgram,StarLog}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\StarLog"; Filename: "{app}\starlog.exe"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\StarLog"; Filename: "{app}\starlog.exe"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\starlog.exe"; Description: "{cm:LaunchProgram,StarLog}"; Flags: nowait postinstall skipifsilent

[Code]
var
  AGBPage: TInputOptionWizardPage;

procedure InitializeWizard;
begin
  // AGB-Zustimmungsseite erstellen
  AGBPage := CreateInputOptionPage(wpLicense,
    'Allgemeine Geschäftsbedingungen',
    'Bitte lesen und bestätigen Sie die AGB',
    'Um die Installation fortzusetzen, müssen Sie unseren AGB zustimmen.',
    True, False);
  AGBPage.Add('Ich akzeptiere die Allgemeinen Geschäftsbedingungen');
  AGBPage.Values[0] := False;
end;

function NextButtonClick(CurPageID: Integer): Boolean;
begin
  Result := True;
  
  if CurPageID = AGBPage.ID then
  begin
    if not AGBPage.Values[0] then
    begin
      MsgBox('Sie müssen den AGB zustimmen, um fortzufahren.', mbError, MB_OK);
      Result := False;
    end;
  end;
end;

[Messages]
ButtonNext=&Weiter >
ButtonBack=< &Zurück
ButtonInstall=&Installieren
ButtonCancel=&Abbrechen
ButtonFinish=&Beenden
ButtonBrowse=&Durchsuchen...
ButtonNo=&Nein
ButtonYes=&Ja
ButtonOK=OK
ButtonWizardBrowse=&Durchsuchen...
ClickNext=Klicken Sie auf Weiter, um fortzufahren.
WizardLicense=Lizenzvereinbarung
LicenseLabel3=Ich akzeptiere die Vereinbarung
LicenseText=Bitte lesen Sie die folgenden Lizenzvereinbarungen sorgfältig durch. Sie müssen die Vereinbarungen akzeptieren, um fortzufahren.