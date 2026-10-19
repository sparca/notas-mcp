import asyncio
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

AQUI = Path(__file__).parent


async def main() -> None:
    params = StdioServerParameters(
        command=sys.executable, args=[str(AQUI / "servidor.py")]
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            init = await session.initialize()
            listados = await session.list_resources()
            uris = [str(r.uri) for r in listados.resources]
            uri = uris[0]
            lido = await session.read_resource(uri)
            texto = lido.contents[0].text

    primeira = next((l.strip() for l in texto.splitlines() if l.strip()), "")
    envelope = {
        "transporte": "stdio",
        "servidor": (getattr(init, "server_info", None) or init.serverInfo).name,
        "resources": uris,
        "resource_lido": uri,
        "conteudo_chars": len(texto),
        "conteudo_linhas": len(texto.splitlines()),
        "primeira_linha": primeira,
    }
    saida = json.dumps(envelope, ensure_ascii=False, indent=2)
    (AQUI / "evidencia-mcp.json").write_text(saida, encoding="utf-8")
    print(saida)


if __name__ == "__main__":
    asyncio.run(main())
