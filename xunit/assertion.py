from typing import Iterable


class Assertion:

    def __init__(self, actual_value: any) -> None:
        self.__negated = False
        self.__reason = "Expected value "
        self.__actual_value = actual_value
        
    def not_(self) -> "Assertion":
        self.__negated = True
        self.__reason = self.__reason + "not "
        return self

    def to_be(self, expected_value: any) -> None:
        reason = f"{self.__reason}to be '{expected_value}', but was '{self.__actual_value}'"
        if self.__negated:
            assert self.__actual_value != expected_value, reason
        else:
            assert self.__actual_value == expected_value, reason

    def to_contain(self, search_value: any) -> None:
        self.__to_be_in(search_value, self.__actual_value)

    def to_be_in(self, container: any) -> None:
        self.__to_be_in(self.__actual_value, container)

    def __to_be_in(self, item: any, container: any) -> None:
        if not self.__is_iterable(container):
            container = str(container)
        if type(container) == str:
            item = str(item)
        if self.__negated:
            assert item not in container, f"Expected '{item}' not to be in '{container}'"
        else:
            assert item in container, f"Expected '{item}' to be in '{container}'"

    def to_raise(self, exception_type: Exception) -> str:
        try:
            self.__actual_value()
        except exception_type as right_exception:
            return str(right_exception)
        except Exception as wrong_exception:
            raise AssertionError(f"Expected '{exception_type}' to be thrown, but was '{type(wrong_exception)}'")
        else:
            raise AssertionError(f"Expected '{exception_type}' to be thrown, but none was thrown.")

    def __is_iterable(self, iterable: any) -> bool:
        return type(iterable) == Iterable or type(iterable) == range


def expect(expected_value: any) -> Assertion:
    return Assertion(expected_value)


def fail(reason: str):
    raise AssertionError(reason)
