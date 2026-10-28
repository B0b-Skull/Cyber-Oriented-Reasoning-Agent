# Known Issue (Low Priority): Console Posture Background & Default Font Color in QTerminal

**Author:** CROW Innovations  

- **Status:** Open (Deferred / Low Priority)
- **Severity:** Low (Cosmetic / Terminal-Specific)
- **Affected Component:** [`core/Network_Isolation/console_posture.py`](../core/Network_Isolation/console_posture.py), [`core/Network_Isolation/ConsolePostureDetection_NIX.sh`](../core/Network_Isolation/ConsolePostureDetection_NIX.sh)
- **Affected Environment:** Linux desktops using **QTerminal** (`/usr/bin/qterminal` v2.4.0 linked against `libqtermwidget6.so.2` on Kali XFCE)

---

## 1. Symptom Description

When running `./core/Network_Isolation/ConsolePostureDetection_NIX.sh` (e.g., `--apply lan`, `--apply airgap`, `--demo`) or launching `./run_cora_NIX.sh cli` under network isolation inside **QTerminal**:
- The **Security Posture Banner**, **Prompt Tag** (`[UNRESTRICTED]`, `[LAN+USB]`, `[AIR-GAP]`), and **Bottom-Pinned HUD** (`NET:UNRESTRICTED(FULL-ACCESS)`, `NET:ISOLATED-LAN+USB(llm-local)`, `NET:AIR-GAPPED(llm-isolated)`) **change colors and update properly**.
- However, the **overall terminal window background color** (`#1C0A0D`, `#081426`, `#061A0E`) and **default console font color** (`#FFE8E8`, `#E0F4FF`, `#D1FAE5`) remain at QTerminal's default profile colors (`WhiteOnBlack`).

---

## 2. Root Cause Analysis

1. **`libqtermwidget6.so.2` Ignores Dynamic XTerm `OSC 10` / `OSC 11` / `OSC 12` Palette Sequences:**
   - Standard XTerm-compatible terminals (XTerm, GNOME Terminal, XFCE4-Terminal, Konsole, Alacritty, Kitty) dynamically re-tint the window background and foreground in-place when receiving `\033]11;#RRGGBB\007` (`OSC 11`) and `\033]10;#RRGGBB\007` (`OSC 10`).
   - In `libqtermwidget6.so.2` (used by Kali's `qterminal` 2.4.0), `Session::setUserTitle(11, color)` emits `Session::changeBackgroundColorRequest(QColor)`, but `QTermWidget::init()` never connects that Qt signal to `TerminalDisplay::setBackgroundColor(QColor)`, and `Vt102Emulation` ignores `OSC 10` and `OSC 12`.
2. **CLI Minor Flag Handling Noted During Testing (Resolved):**
   - Passing `--apply demo` (in addition to `--demo`) and passing trailing `posture -detect` flags to `./run_cora_NIX.sh cli` are supported cleanly so they do not misparse arguments.

---

## 3. Workarounds & Future Resolution Options (When Prioritized)

- **Current Functional Indicators:** The active network security posture is always unambiguously displayed in:
  1. The **Startup Posture Banner** (Crimson Red / Electric Cyan / Matrix Green border and header badge).
  2. The **Interactive Prompt Prefix** (`[UNRESTRICTED] You>`, `[LAN+USB] You>`, `[AIR-GAP] You>`).
  3. The **Bottom-Pinned HUD Bar** (which uses 24-bit TrueColor ANSI SGR background fills `\033[48;2;R;G;Bm` that QTerminal renders natively).
- **Future Fix Path for Full-Screen Background in QTerminal:**
  - Emit persistent 24-bit TrueColor SGR background/foreground sequences (`\033[48;2;R;G;B;38;2;R;G;Bm`) combined with Background Color Erase (`\033[2J\033[H` and `\033[K` on line breaks) rather than relying solely on `OSC 11`/`OSC 10`, or use a terminal emulator that connects `OSC 11`/`OSC 10` (such as `xfce4-terminal`, `kitty`, `alacritty`, or `konsole`).
