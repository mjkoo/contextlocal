from contextvars import Context, ContextVar, copy_context

from contextlocal import LocalProxy, Local, LocalStack

_local_proxy = ContextVar("local_proxy")
local_proxy = LocalProxy(_local_proxy)

_local_stack = ContextVar("local_stack")
local_stack = LocalStack(_local_stack)

_local_dict = ContextVar("local_dict")
local_dict = Local(_local_dict)


def test_local_proxy() -> None:
    def check_value(v: str) -> bool:
        return local_proxy == v

    def test_inner() -> bool:
        context = copy_context()
        context.run(_local_proxy.set, "bar")

        assert check_value("foo")
        assert context.run(check_value, "bar")

    context = copy_context()
    context.run(_local_proxy.set, "foo")
    context.run(test_inner)


def test_local_stack() -> None:
    def check_value(v: str) -> bool:
        return local_stack.top == v

    def test_inner() -> bool:
        context = copy_context()
        context.run(local_stack.push, "bar")

        assert check_value("foo")
        assert context.run(check_value, "bar")

    context = copy_context()
    context.run(_local_stack.set, ["foo"])
    context.run(test_inner)


def test_local_dict() -> None:
    def set_value(v: str) -> None:
        local_dict.key = v

    def check_value(v: str) -> bool:
        return local_dict.key == v

    def test_inner() -> bool:
        context = copy_context()
        context.run(set_value, "bar")

        assert check_value("foo")
        assert context.run(check_value, "bar")

    context = copy_context()
    context.run(set_value, "foo")
    context.run(test_inner)
