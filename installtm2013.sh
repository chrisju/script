#!/bin/bash -e
# Public Domain

: ${TMPREFIX:=$HOME/.winetm}

export WINEPREFIX="$TMPREFIX" WINEARCH=win32
export WINEDEBUG=fixme-all

env -u DISPLAY wineboot -u
winetricks -q riched20 mfc42
winetricks -q ie7 || true

regfile=/tmp/winetm.reg 
cat > "$regfile" <<'REG'
Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Wine\DllOverrides]
"urlmon.dll"="builtin"
REG
regedit "$regfile"
rm -f "$regfile"

tmexe=TM2013Preview1.exe
# tmexe=TM2013Preview2.exe
[[ -f "$tmexe" ]] || tmexe=$(locate -b '\'"$tmexe" || true)
[[ ! -f "$tmexe" ]] || wget http://dldir1.qq.com/qqfile/tm/TM2013Preview1.exe
# [[ ! -f "$tmexe" ]] || wget http://dldir1.qq.com/qqfile/qq/tm/2013P ... eview2.exe
wine $tmexe
