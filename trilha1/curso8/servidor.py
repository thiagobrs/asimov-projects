from fastmcp import FastMCP
import wikipedia

servidor_mcp = FastMCP("mcp-busca-wikipedia")


@servidor_mcp.tool()
async def buscar_wikipedia(busca: str) -> str:
    return wikipedia.summary(busca)


if __name__ == '__main__':
    servidor_mcp.run(transport="sse")  # Server Side Execution, rodando remoto
    # servidor_mcp.run(transport="stdio")  # Modo de texto, rodando local
