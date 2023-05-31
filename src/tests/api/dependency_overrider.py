import typing

from fastapi import FastAPI


class DependencyOverrider:
    def __init__(
        self, app: FastAPI, overrides: typing.Mapping[typing.Callable, typing.Callable]
    ) -> None:
        self.overrides = overrides
        self._app = app
        self._old_overrides = {}

    async def __aenter__(self):
        for dep, new_dep in self.overrides.items():
            if dep in self._app.dependency_overrides:
                self._old_overrides[dep] = self._app.dependency_overrides[dep]
            self._app.dependency_overrides[dep] = new_dep
        return self

    async def __aexit__(self, *args: typing.Any) -> None:
        for dep in self.overrides.keys():
            if dep in self._old_overrides:
                self._app.dependency_overrides[dep] = self._old_overrides.pop(dep)
            else:
                del self._app.dependency_overrides[dep]
