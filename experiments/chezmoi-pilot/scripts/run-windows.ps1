#Requires -Version 7.0
[CmdletBinding()]
param(
    [string]$EvidencePath
)

$ErrorActionPreference = 'Stop'
if ($env:OS -ne 'Windows_NT') {
    throw 'This adapter supports native Windows only.'
}

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$Pilot = Join-Path $ScriptDir 'pilot.py'
$Python = Get-Command py -ErrorAction SilentlyContinue
if ($Python) {
    $PythonArgs = @('-3', $Pilot, 'evaluate', '--platform', 'windows')
} else {
    $Python = Get-Command python -ErrorAction Stop
    $PythonArgs = @($Pilot, 'evaluate', '--platform', 'windows')
}

if ($EvidencePath) {
    $PythonArgs += @('--output', $EvidencePath)
}

Write-Host 'Piloto Windows nativo: únicamente destino temporal; no modifica settings activos.'
& $Python.Source @PythonArgs
exit $LASTEXITCODE
