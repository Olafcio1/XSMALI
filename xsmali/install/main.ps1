$path = "${ENV:TEMP}/xsmali-installer.ps1";
Invoke-WebRequest "https://raw.githubusercontent.com/Olafcio1/XSMALI/main/xsmali/install/child.ps1" -OutFile $path;
powershell -NoLogo -Mta -NoProfile -File $path -ExecutionPolicy Bypass;
