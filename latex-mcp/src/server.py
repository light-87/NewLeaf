#!/usr/bin/env python3
"""
Enhanced LaTeX MCP Server
Compiles LaTeX locally with support for:
- Citations and bibliographies (BibTeX/BibLaTeX)
- ZIP file templates (extract and compile)
- Images and assets (figures, graphics, etc.)
"""

import asyncio
import os
import shutil
import subprocess
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "output"
LOGS_DIR = Path(__file__).parent.parent / "logs"
TEMP_DIR = Path(__file__).parent.parent / "temp"
COMPILER = "pdflatex"  # Options: pdflatex, xelatex, lualatex

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)
TEMP_DIR.mkdir(exist_ok=True)

# Keep track of recent compilations
recent_pdfs = []


def find_main_tex_file(directory: Path) -> Optional[Path]:
    """
    Find the main .tex file in a directory.
    Looks for common patterns like main.tex, paper.tex, or \\documentclass
    """
    # Common main file names
    common_names = ["main.tex", "paper.tex", "manuscript.tex", "article.tex", "document.tex"]

    for name in common_names:
        candidate = directory / name
        if candidate.exists():
            return candidate

    # If not found, look for any .tex file with \documentclass
    for tex_file in directory.rglob("*.tex"):
        try:
            content = tex_file.read_text(encoding='utf-8', errors='ignore')
            if "\\documentclass" in content:
                return tex_file
        except:
            continue

    # Fallback: return first .tex file
    tex_files = list(directory.glob("*.tex"))
    if tex_files:
        return tex_files[0]

    return None


def extract_zip(zip_path: Path, extract_to: Path) -> Path:
    """
    Extract a ZIP file and return the extraction directory.
    Handles nested directories intelligently.
    """
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)

    # Check if everything is in a single subdirectory
    items = list(extract_to.iterdir())
    if len(items) == 1 and items[0].is_dir():
        return items[0]

    return extract_to


def copy_assets_to_temp(source_dir: Path, temp_dir: Path, tex_file: Path):
    """
    Copy all necessary assets (images, .bib files, etc.) to temp directory.
    Maintains relative directory structure.
    """
    # Copy the main .tex file
    shutil.copy2(tex_file, temp_dir / tex_file.name)

    # Find and copy all related files
    extensions = [
        '.bib',      # Bibliography files
        '.bst',      # Bibliography styles
        '.cls',      # Document classes
        '.sty',      # Style files
        '.png', '.jpg', '.jpeg', '.gif',  # Images
        '.pdf', '.eps', '.svg',            # Vector graphics
        '.tex',      # Other .tex files (includes)
    ]

    # Copy files from source directory
    for item in source_dir.rglob('*'):
        if item.is_file() and item.suffix.lower() in extensions:
            # Calculate relative path
            rel_path = item.relative_to(source_dir)
            dest_path = temp_dir / rel_path

            # Create parent directories if needed
            dest_path.parent.mkdir(parents=True, exist_ok=True)

            # Copy file
            shutil.copy2(item, dest_path)


def compile_latex_project(
    project_dir: Path,
    main_tex_file: Optional[Path] = None,
    filename: Optional[str] = None,
    use_biber: bool = False
) -> dict:
    """
    Compile a LaTeX project with all its assets.

    Args:
        project_dir: Directory containing the LaTeX project
        main_tex_file: Path to main .tex file (auto-detected if None)
        filename: Output PDF filename (without .pdf)
        use_biber: Use biber instead of bibtex for bibliographies

    Returns:
        dict with 'success', 'pdf_path', 'log', and 'error' keys
    """
    # Find main .tex file if not provided
    if main_tex_file is None:
        main_tex_file = find_main_tex_file(project_dir)
        if main_tex_file is None:
            return {
                "success": False,
                "pdf_path": None,
                "log": "",
                "error": "No .tex file found in project"
            }

    # Generate filename if not provided
    if not filename:
        filename = main_tex_file.stem

    # Create temporary directory for compilation
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)

        # Copy all assets to temp directory
        copy_assets_to_temp(project_dir, tmpdir_path, main_tex_file)

        # Get the main .tex file in temp directory
        temp_tex_file = tmpdir_path / main_tex_file.name

        # Read content to check for bibliography
        tex_content = temp_tex_file.read_text(encoding='utf-8', errors='ignore')
        has_bibliography = (
            "\\bibliography{" in tex_content or
            "\\addbibresource{" in tex_content or
            "\\cite{" in tex_content or
            "\\bibitem{" in tex_content
        )

        # Detect if we should use biber (BibLaTeX)
        if "\\usepackage{biblatex}" in tex_content or "\\usepackage[" in tex_content and "biblatex" in tex_content:
            use_biber = True

        all_logs = []

        try:
            # First pass - initial compilation
            result = subprocess.run(
                [COMPILER, "-interaction=nonstopmode", "-shell-escape", temp_tex_file.name],
                cwd=tmpdir_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            all_logs.append(f"=== First Pass ===\n{result.stdout}")

            # Run bibliography tool if needed
            if has_bibliography:
                if use_biber:
                    # Use biber for BibLaTeX
                    bib_result = subprocess.run(
                        ["biber", main_tex_file.stem],
                        cwd=tmpdir_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    all_logs.append(f"=== Biber ===\n{bib_result.stdout}")
                else:
                    # Use bibtex for traditional bibliography
                    bib_result = subprocess.run(
                        ["bibtex", main_tex_file.stem],
                        cwd=tmpdir_path,
                        capture_output=True,
                        text=True,
                        timeout=30
                    )
                    all_logs.append(f"=== BibTeX ===\n{bib_result.stdout}")

                # Second pass - process citations
                result = subprocess.run(
                    [COMPILER, "-interaction=nonstopmode", "-shell-escape", temp_tex_file.name],
                    cwd=tmpdir_path,
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                all_logs.append(f"=== Second Pass ===\n{result.stdout}")

            # Final pass - resolve all references
            result = subprocess.run(
                [COMPILER, "-interaction=nonstopmode", "-shell-escape", temp_tex_file.name],
                cwd=tmpdir_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            all_logs.append(f"=== Final Pass ===\n{result.stdout}")

            # Combine all logs
            log_content = "\n\n".join(all_logs)
            log_content += f"\n\n=== Stderr ===\n{result.stderr}"

            # Save log
            log_file = LOGS_DIR / f"{filename}.log"
            log_file.write_text(log_content)

            # Check if PDF was created
            pdf_file = tmpdir_path / f"{main_tex_file.stem}.pdf"
            if pdf_file.exists():
                # Move PDF to output directory
                output_pdf = OUTPUT_DIR / f"{filename}.pdf"
                shutil.copy2(pdf_file, output_pdf)

                # Track recent PDFs
                recent_pdfs.insert(0, str(output_pdf))
                if len(recent_pdfs) > 10:
                    recent_pdfs.pop()

                # Check for warnings/errors in log
                warnings = []
                if "Warning" in log_content:
                    warnings.append("LaTeX warnings detected (check log)")
                if "Overfull" in log_content or "Underfull" in log_content:
                    warnings.append("Box warnings detected")
                if "Citation" in log_content and "undefined" in log_content:
                    warnings.append("Some citations may be undefined")

                return {
                    "success": True,
                    "pdf_path": str(output_pdf),
                    "log": log_content,
                    "error": None,
                    "warnings": warnings
                }
            else:
                return {
                    "success": False,
                    "pdf_path": None,
                    "log": log_content,
                    "error": "PDF generation failed. Check log for errors."
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "pdf_path": None,
                "log": "\n\n".join(all_logs),
                "error": "Compilation timed out (60s limit per pass)"
            }
        except Exception as e:
            return {
                "success": False,
                "pdf_path": None,
                "log": "\n\n".join(all_logs),
                "error": f"Compilation error: {str(e)}"
            }


def compile_latex(latex_content: str, filename: str = None) -> dict:
    """
    Compile LaTeX content to PDF (simple single-file version)
    """
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"document_{timestamp}"

    # Create a temporary directory and write the content
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        tex_file = tmpdir_path / f"{filename}.tex"
        tex_file.write_text(latex_content, encoding='utf-8')

        # Use the project compilation function
        return compile_latex_project(tmpdir_path, tex_file, filename)


def open_pdf(pdf_path: str):
    """Open PDF in default viewer"""
    try:
        if os.name == 'posix':  # macOS or Linux
            if os.uname().sysname == 'Darwin':  # macOS
                subprocess.run(["open", pdf_path])
            else:  # Linux
                subprocess.run(["xdg-open", pdf_path])
        elif os.name == 'nt':  # Windows
            os.startfile(pdf_path)
    except Exception as e:
        print(f"Could not open PDF: {e}")


# Create MCP server
app = Server("latex-compiler")


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available MCP tools"""
    return [
        Tool(
            name="compile_latex",
            description="Compile LaTeX code to PDF and open it. Supports citations and bibliographies.",
            inputSchema={
                "type": "object",
                "properties": {
                    "latex_content": {
                        "type": "string",
                        "description": "The LaTeX source code to compile"
                    },
                    "filename": {
                        "type": "string",
                        "description": "Optional output filename (without .pdf extension)"
                    },
                    "auto_open": {
                        "type": "boolean",
                        "description": "Whether to automatically open the PDF (default: true)"
                    }
                },
                "required": ["latex_content"]
            }
        ),
        Tool(
            name="compile_latex_project",
            description="Compile a LaTeX project directory with all assets (images, .bib files, etc.).",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_path": {
                        "type": "string",
                        "description": "Path to directory containing LaTeX project"
                    },
                    "main_file": {
                        "type": "string",
                        "description": "Optional: name of main .tex file (auto-detected if not provided)"
                    },
                    "auto_open": {
                        "type": "boolean",
                        "description": "Whether to automatically open the PDF (default: true)"
                    }
                },
                "required": ["project_path"]
            }
        ),
        Tool(
            name="compile_latex_zip",
            description="Extract and compile a LaTeX project from a ZIP file (e.g., Overleaf templates, arXiv sources).",
            inputSchema={
                "type": "object",
                "properties": {
                    "zip_path": {
                        "type": "string",
                        "description": "Path to the ZIP file containing the LaTeX project"
                    },
                    "main_file": {
                        "type": "string",
                        "description": "Optional: name of main .tex file (auto-detected if not provided)"
                    },
                    "auto_open": {
                        "type": "boolean",
                        "description": "Whether to automatically open the PDF (default: true)"
                    }
                },
                "required": ["zip_path"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls"""

    if name == "compile_latex":
        latex_content = arguments.get("latex_content")
        filename = arguments.get("filename")
        auto_open = arguments.get("auto_open", True)

        # Compile
        result = compile_latex(latex_content, filename)

        # Open PDF if successful
        if result["success"] and auto_open:
            open_pdf(result["pdf_path"])

        # Return result
        if result["success"]:
            warnings_text = ""
            if result.get("warnings"):
                warnings_text = f"\n\n⚠️ Warnings:\n" + "\n".join(f"  - {w}" for w in result["warnings"])

            return [TextContent(
                type="text",
                text=f"✅ LaTeX compiled successfully!\n\nPDF: {result['pdf_path']}{warnings_text}\n\nThe PDF has been opened in your default viewer."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Compilation failed\n\nError: {result['error']}\n\nLog file: {LOGS_DIR / (filename or 'latest') + '.log'}\n\nLog preview:\n{result['log'][-1000:]}"
            )]

    elif name == "compile_latex_project":
        project_path = Path(arguments.get("project_path"))
        main_file = arguments.get("main_file")
        auto_open = arguments.get("auto_open", True)

        if not project_path.exists():
            return [TextContent(
                type="text",
                text=f"❌ Project directory not found: {project_path}"
            )]

        # Find main file if specified
        main_tex_file = None
        if main_file:
            main_tex_file = project_path / main_file
            if not main_tex_file.exists():
                return [TextContent(
                    type="text",
                    text=f"❌ Main file not found: {main_tex_file}"
                )]

        # Compile
        result = compile_latex_project(project_path, main_tex_file)

        # Open PDF if successful
        if result["success"] and auto_open:
            open_pdf(result["pdf_path"])

        # Return result
        if result["success"]:
            warnings_text = ""
            if result.get("warnings"):
                warnings_text = f"\n\n⚠️ Warnings:\n" + "\n".join(f"  - {w}" for w in result["warnings"])

            return [TextContent(
                type="text",
                text=f"✅ LaTeX project compiled successfully!\n\nProject: {project_path}\nPDF: {result['pdf_path']}{warnings_text}\n\nThe PDF has been opened in your default viewer."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Compilation failed\n\nError: {result['error']}\n\nLog preview:\n{result['log'][-1000:]}"
            )]

    elif name == "compile_latex_zip":
        zip_path = Path(arguments.get("zip_path"))
        main_file = arguments.get("main_file")
        auto_open = arguments.get("auto_open", True)

        if not zip_path.exists():
            return [TextContent(
                type="text",
                text=f"❌ ZIP file not found: {zip_path}"
            )]

        # Extract ZIP file
        extract_dir = TEMP_DIR / f"zip_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        extract_dir.mkdir(parents=True, exist_ok=True)

        try:
            project_dir = extract_zip(zip_path, extract_dir)
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Failed to extract ZIP file: {e}"
            )]

        # Find main file if specified
        main_tex_file = None
        if main_file:
            main_tex_file = project_dir / main_file
            if not main_tex_file.exists():
                return [TextContent(
                    type="text",
                    text=f"❌ Main file not found in ZIP: {main_file}"
                )]

        # Compile
        result = compile_latex_project(project_dir, main_tex_file, zip_path.stem)

        # Clean up temp directory
        try:
            shutil.rmtree(extract_dir)
        except:
            pass

        # Open PDF if successful
        if result["success"] and auto_open:
            open_pdf(result["pdf_path"])

        # Return result
        if result["success"]:
            warnings_text = ""
            if result.get("warnings"):
                warnings_text = f"\n\n⚠️ Warnings:\n" + "\n".join(f"  - {w}" for w in result["warnings"])

            return [TextContent(
                type="text",
                text=f"✅ LaTeX ZIP compiled successfully!\n\nZIP: {zip_path}\nPDF: {result['pdf_path']}{warnings_text}\n\nThe PDF has been opened in your default viewer."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Compilation failed\n\nError: {result['error']}\n\nLog preview:\n{result['log'][-1000:]}"
            )]

    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


@app.list_resources()
async def list_resources() -> list[Any]:
    """List recent compilations"""
    resources = []
    for i, pdf_path in enumerate(recent_pdfs[:10]):
        if Path(pdf_path).exists():
            resources.append({
                "uri": f"file://{pdf_path}",
                "name": f"Recent compilation #{i+1}: {Path(pdf_path).name}",
                "mimeType": "application/pdf"
            })
    return resources


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    print("Starting Enhanced LaTeX MCP Server...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    print(f"Temp directory: {TEMP_DIR}")
    print("")
    print("Features:")
    print("  ✓ Citations & bibliographies (BibTeX/BibLaTeX)")
    print("  ✓ ZIP file support (templates)")
    print("  ✓ Images & assets (figures, graphics)")
    print("  ✓ Multi-file projects")
    asyncio.run(main())
