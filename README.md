# fmaps2kml
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
