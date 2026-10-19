from pathlib import Path

try:  # mcp >= 2
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP

NOTAS = Path(__file__).parent / "notas.md"

mcp = FastMCP("notas-mcp")


@mcp.resource("notas://minhas-notas", mime_type="text/markdown")
def minhas_notas() -> str:
    """Conteúdo atual do notas.md (lido do disco a cada leitura)."""
    return NOTAS.read_text(encoding="utf-8")


if __name__ == "__main__":
    mcp.run(transport="stdio")
