# Simple LaTeX MCP Renderer

A minimal local MCP server that compiles LaTeX and shows PDFs. No cloud, no complexity.

## What It Does

1. You chat with Claude (or any MCP-compatible AI)
2. AI writes LaTeX code
3. MCP server compiles it locally
4. PDF opens automatically

That's it!

## Architecture

```
┌─────────────────┐
│  Claude Desktop │ (or any MCP client)
│      App        │
└────────┬────────┘
         │ MCP Protocol
┌────────▼────────┐
│   MCP Server    │ (runs locally)
│   (Python/Node) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│pdflatex│ │  PDF    │
│(TeX Live)│ │ Viewer │
└────────┘ └─────────┘
```

## Requirements

- **TeX Live** (for pdflatex)
- **Python 3.10+** or **Node.js 18+**
- **Claude Desktop** (or any MCP client)
- That's all!

## MCP Server Features

### Tools Provided

1. **compile_latex**
   - Input: LaTeX code as string
   - Output: Path to generated PDF
   - Auto-opens PDF in default viewer

2. **compile_latex_file**
   - Input: Path to .tex file
   - Output: Path to generated PDF
   - Auto-opens PDF

### Resources

- Recent compilations (last 10 PDFs)
- Build logs for debugging

## Project Structure

```
latex-mcp/
├── src/
│   ├── server.py          # MCP server (Python)
│   └── server.js          # MCP server (Node.js alternative)
├── output/                # Generated PDFs
├── logs/                  # Build logs
├── examples/
│   └── sample.tex         # Example LaTeX file
├── package.json           # Node.js version
├── pyproject.toml         # Python version
└── README.md
```

## Installation

### Option 1: Python Version

```bash
# Install TeX Live (if not already installed)
# Ubuntu/Debian:
sudo apt-get install texlive-full

# macOS:
brew install --cask mactex

# Windows:
# Download from https://www.tug.org/texlive/

# Clone and setup
git clone <your-repo>
cd latex-mcp
pip install mcp pdflatex

# Run server
python src/server.py
```

### Option 2: Node.js Version

```bash
# Install TeX Live (same as above)

# Clone and setup
git clone <your-repo>
cd latex-mcp
npm install

# Run server
npm start
```

## Configuration

Add to Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "latex": {
      "command": "python",
      "args": ["/absolute/path/to/latex-mcp/src/server.py"]
    }
  }
}
```

Or for Node.js version:

```json
{
  "mcpServers": {
    "latex": {
      "command": "node",
      "args": ["/absolute/path/to/latex-mcp/src/server.js"]
    }
  }
}
```

## Usage

1. **Start Claude Desktop**
2. **Ask Claude to compile LaTeX**:

```
User: "Compile this LaTeX:
\documentclass{article}
\begin{document}
Hello World!
\end{document}"

Claude: *uses compile_latex tool*
```

3. **PDF opens automatically!**

## Example Prompts

### Simple Document
```
"Create a simple LaTeX document with a title and some text, then compile it"
```

### Math Paper
```
"Create a LaTeX document with Einstein's field equations and compile it"
```

### Resume
```
"Create a professional resume in LaTeX and compile it"
```

### From File
```
"Compile the LaTeX file at /path/to/document.tex"
```

## Features

✅ Local compilation (no cloud needed)
✅ Auto-opens PDF viewer
✅ Keeps build logs for debugging
✅ Works with any MCP-compatible AI
✅ Free and open source
✅ No deployment needed
✅ Simple setup

## Limitations

- Runs on your machine only (not a web service)
- Requires TeX Live installed locally
- No collaboration features
- No real-time preview
- No version control (just compiles)

But that's the point - it's **simple**!

## Advanced Usage

### Custom Output Directory

Edit the server code to change output directory:

```python
OUTPUT_DIR = "/your/custom/path"
```

### Different Compilers

Change from `pdflatex` to `xelatex` or `lualatex`:

```python
COMPILER = "xelatex"  # or "lualatex"
```

### Bibliography Support

The server automatically runs `bibtex` if it detects `\bibliography{}`:

```latex
\documentclass{article}
\begin{document}
\cite{einstein1905}
\bibliography{refs}
\end{document}
```

## Troubleshooting

### PDF doesn't open
- Check if default PDF viewer is set
- Look in `output/` directory manually

### Compilation errors
- Check `logs/` directory for error messages
- Ensure TeX Live is installed correctly
- Run `pdflatex --version` to verify

### MCP connection issues
- Restart Claude Desktop
- Check config file path is absolute
- Check server script is executable

## Future Enhancements (Optional)

If you want to add features later:
- Web UI for live preview
- File watcher for auto-recompile
- Template library
- Package manager integration

But for now - keep it simple!

## License

MIT - Free for everyone
