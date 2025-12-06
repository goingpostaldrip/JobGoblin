# Build Instructions for JobGoblin

## Easy Launch Scripts

### Windows
Simply double-click `run.bat` to launch JobGoblin. It will:
- Automatically create a virtual environment (if needed)
- Install dependencies
- Launch the GUI

### macOS / Linux
Run the launch script:
```bash
chmod +x run.sh
./run.sh
```

---

## Building Installers with PyInstaller

### Prerequisites
Install PyInstaller and additional tools:
```bash
pip install pyinstaller pyinstaller-hooks-contrib
```

### Build for Current Platform

#### Windows Executable (.exe)
```bash
pyinstaller jobgoblin.spec
```
This creates `dist/JobGoblin/JobGoblin.exe` - a standalone executable

#### macOS App Bundle (.app)
```bash
pyinstaller jobgoblin.spec
```
This creates `dist/JobGoblin.app` - a native macOS application

#### Linux Binary
```bash
pyinstaller jobgoblin.spec
```
This creates `dist/JobGoblin/JobGoblin` - a standalone binary

### Output Locations
- **Windows**: `dist/JobGoblin/JobGoblin.exe`
- **macOS**: `dist/JobGoblin.app`
- **Linux**: `dist/JobGoblin/JobGoblin`

---

## Creating Windows Installer (.MSI or .EXE)

For a professional Windows installer, use `pyinstaller` with additional tools:

### Option 1: Using PyInstaller (Simple)
```bash
pyinstaller jobgoblin.spec --windowed
```

### Option 2: Using NSIS (Professional Installer)
Install NSIS from https://nsis.sourceforge.io/

Create `installer.nsi`:
```nsis
; JobGoblin Installer Script
!include "MUI2.nsh"

Name "JobGoblin - Lead Finder"
OutFile "JobGoblin-Installer.exe"
InstallDir "$PROGRAMFILES\JobGoblin"

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  File /r "dist\JobGoblin\*.*"
  CreateShortCut "$SMPROGRAMS\JobGoblin.lnk" "$INSTDIR\JobGoblin.exe"
SectionEnd
```

Build the installer:
```bash
makensis installer.nsi
```

---

## For macOS: Creating .DMG Installer

```bash
# Create DMG from the app bundle
hdiutil create -volname "JobGoblin" -srcfolder dist/ -ov -format UDZO JobGoblin.dmg
```

---

## For Linux: Creating .DEB or .AppImage

### .AppImage
```bash
pip install appimage-builder
# Configure appimage-builder.yml with JobGoblin settings
appimage-builder --recipe appimage-builder.yml
```

### .DEB (Debian/Ubuntu)
```bash
pip install fpm
fpm -s dir -t deb -n jobgoblin -v 1.0.0 -C dist/JobGoblin
```

---

## Tips

1. **Icon**: Add your app icon to `gui_app.py` and reference it in `jobgoblin.spec`
2. **One-File Builds**: Add `--onefile` flag for single executable file
3. **Console Output**: Set `console=True` in spec if you want error messages visible
4. **Code Signing**: For macOS, sign your app: `codesign -s - dist/JobGoblin.app`

---

## Quick Build Summary

| Platform | Command | Output |
|----------|---------|--------|
| Windows  | `pyinstaller jobgoblin.spec` | `dist/JobGoblin/JobGoblin.exe` |
| macOS    | `pyinstaller jobgoblin.spec` | `dist/JobGoblin.app` |
| Linux    | `pyinstaller jobgoblin.spec` | `dist/JobGoblin/JobGoblin` |

---

**Built with ❤️ by NERDY BIRD IT** 🟢
