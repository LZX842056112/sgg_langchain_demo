import asyncio


# 协程适用于I/O密集型任务。CPU密集型任务不适用，
# I/O密集型：等待数据传输的任务，比方说http请求（调用大模型API时，就是发送一个HTTP的一个请求），比方说传输文件，接收文件
# CPU密集型任务：数学计算，图像处理，加密计算，这些任务会一直占用CPU计算能力
async def func1():
    print("func1 开始")
    # I/O 等待场景
    await asyncio.sleep(5)
    print("func1 结束")


async def func2():
    print("func2 开始")
    await asyncio.sleep(3)
    print("func2 结束")


async def func3():
    print("func3 开始")
    await asyncio.sleep(10)
    print("func3 结束")


async def main():
    await asyncio.gather(func3(), func2(), func1())


import time

start_time = time.time()
# 底层通过一个事件循环方式去维护多个协程，最终的运行时间，取决于耗时最长的任务
asyncio.run(main())
end_time = time.time()
