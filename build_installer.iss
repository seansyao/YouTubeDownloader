; Inno Setup installer script for YouTube MP4 Downloader
; This script creates a Windows installer that includes the application,
; FFmpeg, and automatically configures PATH variables.
;
; To use this script:
; 1. Install Inno Setup from: http://www.jrsoftware.org/isdl.php
; 2. Run: "C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_installer.iss
; 3. The installer will be created in: output/YouTubeDownloaderSetup.exe

[Setup]
AppName=YouTube MP4 Downloader
AppVersion=1.0.0
DefaultDirName={autopf}\YouTubeDownloader
DefaultGroupName=YouTube MP4 Downloader
OutputDir=output
OutputBaseFilename=YouTubeDownloaderSetup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64

; Request admin privileges for PATH modification
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Main application executable
Source: "dist\YouTubeDownloader.exe"; DestDir: "{app}"; Flags: ignoreversion

; FFmpeg binaries (ensure these exist before building)
; Download from: https://ffmpeg.org/download.html
Source: "bin\ffmpeg.exe"; DestDir: "{app}\bin"; Flags: ignoreversion
Source: "bin\ffprobe.exe"; DestDir: "{app}\bin"; Flags: ignoreversion

; Documentation
Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion isreadme
Source: "MANUAL.md"; DestDir: "{app}"; Flags: ignoreversion
Source: "plan.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YouTube MP4 Downloader"; Filename: "{app}\YouTubeDownloader.exe"; Comment: "Download YouTube videos as MP4"; WorkingDir: "{app}"
Name: "{group}\{cm:UninstallProgram,YouTube MP4 Downloader}"; Filename: "{uninstallexe}"
Name: "{userdesktop}\YouTube MP4 Downloader"; Filename: "{app}\YouTubeDownloader.exe"; Tasks: desktopicon; WorkingDir: "{app}"

[Run]
; Run the application after installation
Filename: "{app}\YouTubeDownloader.exe"; Description: "{cm:LaunchProgram,YouTube MP4 Downloader}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
; Clean up application data on uninstall
Type: dirifempty; Name: "{app}"

[Code]
{ Custom Pascal code for PATH management and admin verification }

const
  RegPath = 'SYSTEM\CurrentControlSet\Control\Session Manager\Environment';

procedure CheckAdminPrivileges;
begin
  if not IsAdminInstallMode then
  begin
    MsgBox('This installation requires administrator privileges to configure PATH variables.' + #13 +
           'Please restart the installer and choose "Yes" when prompted for administrator access.',
           mbError, MB_OK);
    Abort;
  end;
end;

function GetEnvVarValue(const VarName: string): string;
begin
  if not RegQueryStringValue(HKEY_LOCAL_MACHINE, RegPath, VarName, Result) then
    Result := '';
end;

procedure AddToPath(const AppPath: string);
var
  EnvPath: string;
  NewPath: string;
begin
  EnvPath := GetEnvVarValue('PATH');
  
  { Check if path already exists }
  if Pos(AppPath, EnvPath) > 0 then
  begin
    Log('FFmpeg bin directory already in PATH');
    Exit;
  end;
  
  { Add to PATH }
  if Length(EnvPath) > 0 then
    NewPath := EnvPath + ';' + AppPath
  else
    NewPath := AppPath;
  
  if not RegWriteStringValue(HKEY_LOCAL_MACHINE, RegPath, 'PATH', NewPath) then
  begin
    MsgBox('Failed to update PATH variable. You may need to add "' + AppPath + '" manually.', 
           mbError, MB_OK);
  end
  else
  begin
    Log('Added to PATH: ' + AppPath);
  end;
end;

procedure RemoveFromPath(const AppPath: string);
var
  EnvPath: string;
  NewPath: string;
  PartBefore: string;
  PartAfter: string;
  Pos1: integer;
begin
  EnvPath := GetEnvVarValue('PATH');
  Pos1 := Pos(AppPath, EnvPath);
  
  if Pos1 = 0 then
    Exit;
  
  { Remove the path entry }
  PartBefore := Copy(EnvPath, 1, Pos1 - 1);
  PartAfter := Copy(EnvPath, Pos1 + Length(AppPath), Length(EnvPath));
  
  { Clean up extra semicolons }
  if (Length(PartBefore) > 0) and (PartBefore[Length(PartBefore)] = ';') then
    PartBefore := Copy(PartBefore, 1, Length(PartBefore) - 1);
  
  if (Length(PartAfter) > 0) and (PartAfter[1] = ';') then
    PartAfter := Copy(PartAfter, 2, Length(PartAfter));
  
  NewPath := PartBefore;
  if (Length(PartBefore) > 0) and (Length(PartAfter) > 0) then
    NewPath := PartBefore + ';' + PartAfter
  else
    NewPath := PartBefore + PartAfter;
  
  RegWriteStringValue(HKEY_LOCAL_MACHINE, RegPath, 'PATH', NewPath);
end;

procedure CurStepChanged(CurStep: TSetupStep);
begin
  { Add FFmpeg bin directory to PATH after files are installed }
  if CurStep = ssPostInstall then
  begin
    AddToPath(ExpandConstant('{app}\bin'));
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
  { Remove FFmpeg bin directory from PATH on uninstall }
  if CurUninstallStep = usPostUninstall then
  begin
    RemoveFromPath(ExpandConstant('{app}\bin'));
  end;
end;

function InitializeSetup: Boolean;
begin
  { Check for admin privileges before proceeding }
  CheckAdminPrivileges;
  Result := True;
end;
