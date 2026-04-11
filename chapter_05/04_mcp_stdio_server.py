from mcp.server.fastmcp import FastMCP

fast_mcp_instance = FastMCP(name="demo_mcp")


@fast_mcp_instance.tool()
def add_two_number(a: int, b: int):
    return a + b


if __name__ == '__main__':
    fast_mcp_instance.run(transport="stdio")
