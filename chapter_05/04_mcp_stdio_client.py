import asyncio

from mcp.client.stdio import stdio_client
from mcp import ClientSession, StdioServerParameters


async def stdio_run():
    # 子进程
    # stdio的客户端和服务端是同一台机器当中的两个进程，此时，我们需要告知给客户端，服务端怎么启动起来
    server_params = StdioServerParameters(
        command=r"C:\MySoftware\Anaconda3\envs\python311\python.exe",
        args=[r"D:\Projects\SGG\sgg_langchain_demo\chapter_05\04_mcp_stdio_server.py"],
    )

    # read write 就是标准输入，输出，也就是说为 stdio
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 初始化连接
            await session.initialize()

            # 获取可用工具
            tools = await session.list_tools()
            print(tools)
            print()

            # 调用工具
            call_res = await session.call_tool("add_two_number", {"a": 1, "b": 2})
            print(call_res)
            print()


asyncio.run(stdio_run())
