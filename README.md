# fmaps2kml

[![Release](https://img.shields.io/github/v/release/robertobissanti/fmaps2kml)](https://github.com/robertobissanti/fmaps2kml/releases/latest)
[![Downloads](https://img.shields.io/github/downloads/robertobissanti/fmaps2kml/total)](https://github.com/robertobissanti/fmaps2kml/releases)
[![Build](https://img.shields.io/github/actions/workflow/status/robertobissanti/fmaps2kml/release.yml)](https://github.com/robertobissanti/fmaps2kml/actions/workflows/release.yml)
[![License](https://img.shields.io/github/license/robertobissanti/fmaps2kml)](LICENSE)
![Platforms](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-blue)

[![Download](https://img.shields.io/badge/Download-ultima%20versione-brightgreen?style=for-the-badge&logo=github)](https://github.com/robertobissanti/fmaps2kml/releases/latest)
Convert fmaps (JSON) file, created by formaps.com, to KML file
## Download
Scarica l'ultima versione per il tuo sistema dalla pagina [Releases](https://github.com/robertobissanti/fmaps2kml/releases/latest):

| Sistema | File |
|---|---|
| Windows | `fmaps2kml-windows-x64.zip` |
| macOS Apple Silicon | `fmaps2kml-macos-arm64.zip` |
| macOS Intel | `fmaps2kml-macos-x64.zip` |
| Linux | `fmaps2kml-linux-x64.tar.gz` |

Su macOS l'app non è firmata: al primo avvio usa tasto destro → *Apri*.

## Uso
- **GUI**: avvia l'app, scegli il file `.fmaps`, (opzionale) cambia il percorso KML, premi *Converti*.
- **Riga di comando**: `fmaps2kml input.fmaps [output.kml]`

## Build
Le release vengono generate automaticamente da GitHub Actions al push di un tag `v*`.
