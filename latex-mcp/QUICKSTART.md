# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install TeX Live

### macOS
```bash
brew install --cask mactex
```

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install texlive-full
```

### Windows
Download and install from: https://www.tug.org/texlive/

## Step 2: Install Python Dependencies

```bash
pip install mcp
```

That's it! Just one package.

## Step 3: Get the Absolute Path

```bash
# Navigate to the project
cd /path/to/latex-mcp

# Get absolute path (macOS/Linux)
pwd
# Copy this path!

# On Windows (PowerShell)
(Get-Location).Path
```

## Step 4: Configure Claude Desktop

### macOS
Edit: `~/Library/Application Support/Claude/claude_desktop_config.json`

### Windows
Edit: `%APPDATA%\Claude\claude_desktop_config.json`

### Linux
Edit: `~/.config/Claude/claude_desktop_config.json`

**Add this:**
```json
{
  "mcpServers": {
    "latex": {
      "command": "python",
      "args": ["/PASTE/ABSOLUTE/PATH/HERE/src/server.py"]
    }
  }
}
```

Replace `/PASTE/ABSOLUTE/PATH/HERE/` with the path from Step 3!

**Example:**
```json
{
  "mcpServers": {
    "latex": {
      "command": "python",
      "args": ["/Users/yourname/projects/latex-mcp/src/server.py"]
    }
  }
}
```

## Step 5: Restart Claude Desktop

Close and reopen Claude Desktop app.

## Step 6: Test It!

In Claude, type:

```
Compile this LaTeX:
\documentclass{article}
\begin{document}
Hello from MCP!
\end{document}
```

Claude will use the MCP server to compile it, and your PDF should open automatically! 🎉

## Verify Installation

To check if TeX Live is installed:

```bash
pdflatex --version
```

Should show version info.

To check if Python has MCP:

```bash
python -c "import mcp; print('MCP installed!')"
```

Should print "MCP installed!"

## Common Issues

### "command not found: pdflatex"

TeX Live is not in your PATH. After installing:
- **macOS**: Restart terminal or run `eval "$(/usr/libexec/path_helper)"`
- **Linux**: Run `source ~/.bashrc` or restart terminal
- **Windows**: Restart computer after TeX Live installation

### "No module named 'mcp'"

Run: `pip install mcp`

If still fails, try: `pip3 install mcp`

### MCP server not showing in Claude

1. Double-check the absolute path in config is correct
2. Make sure there are no typos in the JSON
3. Restart Claude Desktop completely (quit and reopen)
4. Check Claude Desktop logs (Help → Show Logs)

## What's Next?

Try these examples:

**Math equation:**
```
Create a LaTeX document with Euler's formula and compile it
```

**Resume:**
```
Create a simple resume in LaTeX with my name "John Doe" and compile it
```

**From file:**
```
Compile the LaTeX file at examples/sample.tex
```

**Custom filename:**
```
Compile this LaTeX and save as "my_document":
\documentclass{article}
\begin{document}
Test
\end{document}
```

Enjoy! 🚀
