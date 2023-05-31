import asyncio
import functools
from typing import Awaitable, Callable, ParamSpec, TypeVar
R = TypeVar("R")
P = ParamSpec("P")


def make_async(_func: Callable[P, R]) -> Callable[P, Awaitable[R]]:
    async def wrapped(*args: P.args, **kwargs: P.kwargs) -> R:
        func = functools.partial(_func, *args, **kwargs)
        return await asyncio.get_event_loop().run_in_executor(executor=None, func=func)

    return wrapped
