#!/usr/bin/env python3
"""
Simple LaTeX MCP Server
Compiles LaTeX locally and opens PDFs
"""

import asyncio
import os
import subprocess
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource

# Configuration
OUTPUT_DIR = Path(__file__).parent.parent / "output"
LOGS_DIR = Path(__file__).parent.parent / "logs"
COMPILER = "pdflatex"  # Options: pdflatex, xelatex, lualatex

# Ensure directories exist
OUTPUT_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

# Keep track of recent compilations
recent_pdfs = []


def compile_latex(latex_content: str, filename: str = None) -> dict:
    """
    Compile LaTeX content to PDF

    Args:
        latex_content: LaTeX source code
        filename: Optional output filename (without .pdf)

    Returns:
        dict with 'success', 'pdf_path', 'log', and 'error' keys
    """
    # Generate filename if not provided
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"document_{timestamp}"

    # Create temporary directory for compilation
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir_path = Path(tmpdir)
        tex_file = tmpdir_path / f"{filename}.tex"

        # Write LaTeX content to file
        tex_file.write_text(latex_content)

        # Compile with pdflatex
        try:
            # First pass
            result = subprocess.run(
                [COMPILER, "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file.name],
                cwd=tmpdir_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            # Check if bibtex is needed
            if "\\bibliography{" in latex_content or "\\addbibresource{" in latex_content:
                # Run bibtex
                subprocess.run(
                    ["bibtex", filename],
                    cwd=tmpdir_path,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                # Second pass for citations
                subprocess.run(
                    [COMPILER, "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file.name],
                    cwd=tmpdir_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )

            # Final pass for references
            result = subprocess.run(
                [COMPILER, "-interaction=nonstopmode", "-output-directory", tmpdir, tex_file.name],
                cwd=tmpdir_path,
                capture_output=True,
                text=True,
                timeout=30
            )

            # Save log
            log_content = result.stdout + result.stderr
            log_file = LOGS_DIR / f"{filename}.log"
            log_file.write_text(log_content)

            # Check if PDF was created
            pdf_file = tmpdir_path / f"{filename}.pdf"
            if pdf_file.exists():
                # Move PDF to output directory
                output_pdf = OUTPUT_DIR / f"{filename}.pdf"
                pdf_file.rename(output_pdf)

                # Track recent PDFs
                recent_pdfs.insert(0, str(output_pdf))
                if len(recent_pdfs) > 10:
                    recent_pdfs.pop()

                return {
                    "success": True,
                    "pdf_path": str(output_pdf),
                    "log": log_content,
                    "error": None
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
                "log": "",
                "error": "Compilation timed out (30s limit)"
            }
        except Exception as e:
            return {
                "success": False,
                "pdf_path": None,
                "log": "",
                "error": f"Compilation error: {str(e)}"
            }


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
            description="Compile LaTeX code to PDF and open it. Returns the path to the generated PDF.",
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
            name="compile_latex_file",
            description="Compile a LaTeX file from disk to PDF and open it.",
            inputSchema={
                "type": "object",
                "properties": {
                    "file_path": {
                        "type": "string",
                        "description": "Path to the .tex file to compile"
                    },
                    "auto_open": {
                        "type": "boolean",
                        "description": "Whether to automatically open the PDF (default: true)"
                    }
                },
                "required": ["file_path"]
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
            return [TextContent(
                type="text",
                text=f"✅ LaTeX compiled successfully!\n\nPDF: {result['pdf_path']}\n\nThe PDF has been opened in your default viewer."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Compilation failed\n\nError: {result['error']}\n\nLog file: {LOGS_DIR / 'latest.log'}\n\nLog preview:\n{result['log'][-500:]}"
            )]

    elif name == "compile_latex_file":
        file_path = arguments.get("file_path")
        auto_open = arguments.get("auto_open", True)

        # Read file
        try:
            latex_content = Path(file_path).read_text()
            filename = Path(file_path).stem
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Could not read file: {e}"
            )]

        # Compile
        result = compile_latex(latex_content, filename)

        # Open PDF if successful
        if result["success"] and auto_open:
            open_pdf(result["pdf_path"])

        # Return result
        if result["success"]:
            return [TextContent(
                type="text",
                text=f"✅ LaTeX file compiled successfully!\n\nSource: {file_path}\nPDF: {result['pdf_path']}\n\nThe PDF has been opened in your default viewer."
            )]
        else:
            return [TextContent(
                type="text",
                text=f"❌ Compilation failed\n\nError: {result['error']}\n\nLog preview:\n{result['log'][-500:]}"
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
    print("Starting LaTeX MCP Server...")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"Logs directory: {LOGS_DIR}")
    asyncio.run(main())
