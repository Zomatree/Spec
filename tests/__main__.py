from typing import Annotated, Optional
import unittest
import spec

class Simple(spec.Model):
    a: int
    b: str

class TestSimple(unittest.TestCase):
    INPUT = {"a": 1, "b": "value"}

    def setUp(self):
        self.instance = Simple(self.INPUT)

    def test_a_value(self):
        self.assertEqual(self.instance.a, 1)

    def test_b_value(self):
        self.assertEqual(self.instance.b, "value")

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<Simple a=1 b='value'>")

class Inner(spec.Model):
    value: int

class Outer(spec.Model):
    inner: Inner

class TestDeepModel(unittest.TestCase):
    INPUT = {"inner": {"value": 1}}

    def setUp(self):
        self.instance = Outer(self.INPUT)

    def test_inner_value(self):
        self.assertEqual(self.instance.inner, Inner(self.INPUT["inner"]))

    def test_inner_value_value(self):
        self.assertEqual(self.instance.inner.value, 1)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<Outer inner=<Inner value=1>>")

class List(spec.Model):
    data: list[int]

class TestListModel(unittest.TestCase):
    INPUT = {"data": [1, 2, 3]}

    def setUp(self):
        self.instance = List(self.INPUT)

    def test_data_value(self):
        self.assertEqual(self.instance.data, [1, 2, 3])

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<List data=[1, 2, 3]>")

class ListOuter(spec.Model):
    inners: list[Inner]

class TestListDeepModel(unittest.TestCase):
    INPUT = {"inners": [{"value": 1}, {"value": 2}]}

    def setUp(self):
        self.instance = ListOuter(self.INPUT)

    def test_inner_value(self):
        self.assertEqual(self.instance.inners, [Inner(data) for data in self.INPUT["inners"]])

    def test_inner_value_value(self):
        for inner, data in zip(self.instance.inners, self.INPUT["inners"]):
            self.assertEqual(inner.value, data["value"])

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<ListOuter inners=[<Inner value=1>, <Inner value=2>]>")

class Dict(spec.Model):
    data: dict[str, int]

class TestDictModel(unittest.TestCase):
    INPUT = {"data": {"a": 1, "b": 2}}

    def setUp(self):
        self.instance = Dict(self.INPUT)

    def test_data_value(self):
        self.assertEqual(self.instance.data, self.INPUT["data"])

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<Dict data={'a': 1, 'b': 2}>")

class AnnotatedUsage(spec.Model):
    a: Annotated[int, spec.rename("b")]

class TestAnnotated(unittest.TestCase):
    INPUT = {"b": 1}

    def setUp(self):
        self.instance = AnnotatedUsage(self.INPUT)

    def test_data_value(self):
        self.assertEqual(self.instance.a, self.INPUT["b"])

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), self.INPUT)

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<AnnotatedUsage a=1>")

class DefaultUsage(spec.Model):
    a: Annotated[int, spec.default(lambda: 0)]

class TestDefault(unittest.TestCase):
    INPUT = {}

    def setUp(self):
        self.instance = DefaultUsage(self.INPUT)

    def test_data_value(self):
        self.assertEqual(self.instance.a, 0)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"a": 0})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<DefaultUsage a=0>")

class OptionalNotPassed(spec.Model):
    value: Optional[int]

class OptionalNotPassedUsage(unittest.TestCase):
    INPUT = {}

    def setUp(self):
        self.instance = OptionalNotPassed(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, None)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"value": None})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<OptionalNotPassed value=None>")

class OptionalPassedNone(spec.Model):
    value: Optional[int]

class OptionalPassedNoneUsage(unittest.TestCase):
    INPUT = {"value": None}

    def setUp(self):
        self.instance = OptionalPassedNone(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, None)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"value": None})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<OptionalPassedNone value=None>")

class OptionalPassedValue(spec.Model):
    value: Optional[int]

class OptionalPassedValuedUsage(unittest.TestCase):
    INPUT = {"value": 1}

    def setUp(self):
        self.instance = OptionalPassedValue(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, 1)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"value": 1})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<OptionalPassedValue value=1>")

class AnnotatedOptional(spec.Model):
    value: Annotated[Optional[int], spec.rename("data")]

class AnnotatedOptionalUsage(unittest.TestCase):
    INPUT = {"data": 1}

    def setUp(self):
        self.instance = AnnotatedOptional(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, 1)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"data": 1})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<AnnotatedOptional value=1>")

class AnnotatedOptionalWithDefault(spec.Model):
    value: Annotated[Optional[int], spec.default(lambda: 0)]

class AnnotatedOptionalWithDefaultUsage(unittest.TestCase):
    INPUT = {}

    def setUp(self):
        self.instance = AnnotatedOptionalWithDefault(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, 0)

    def test_to_dict(self):
        self.assertEqual(self.instance.to_dict(), {"value": 0})

    def test_repr(self):
        self.assertEqual(repr(self.instance), "<AnnotatedOptionalWithDefault value=0>")

class DefaultClsAttr(spec.Model):
    value: int = 1

class DefaultClsAttrUsage(unittest.TestCase):
    INPUT = {}

    def setUp(self) -> None:
        self.instance = DefaultClsAttr(self.INPUT)

    def test_value_value(self):
        self.assertEqual(self.instance.value, DefaultClsAttr.value)

class Invalid(spec.Model):
    a: int

class InvalidUsage(unittest.TestCase):
    def test_fail(self):
        with self.assertRaises(spec.InvalidType):
            Invalid({"a": "not a string"})

class PartA(spec.Model):
    a: int

class PartB(spec.Model):
    b: str

class UntaggedPart(spec.TransparentModel[PartA | PartB]):
    pass


class UntaggedUnionUsage(unittest.TestCase):
    INPUT_1 = {"a": 1}
    INPUT_2 = {"b": "data"}

    def setUp(self):
        self.instance_1 = UntaggedPart(self.INPUT_1)
        self.instance_2 = UntaggedPart(self.INPUT_2)

    def test_instance_1(self):
        self.assertIsInstance(self.instance_1.value, PartA)

        assert isinstance(self.instance_1.value, PartA)

        self.assertEqual(self.instance_1.value.a, self.INPUT_1["a"])

    def test_instance_b(self):
        self.assertIsInstance(self.instance_2.value, PartB)

        assert isinstance(self.instance_2.value, PartB)

        self.assertEqual(self.instance_2.value.b, self.INPUT_2["b"])

ExternallyTaggedPart = spec.transparent(Annotated[PartA | PartB, spec.tag("external")])

class ExternallyTaggedUnionUsage(unittest.TestCase):
    INPUT_1 = {"PartA": {"a": 1}}
    INPUT_2 = {"PartB": {"b": "data"}}

    def setUp(self):
        self.instance_1 = ExternallyTaggedPart(self.INPUT_1)
        self.instance_2 = ExternallyTaggedPart(self.INPUT_2)

    def test_instance_1(self):
        self.assertIsInstance(self.instance_1.value, PartA)

        assert isinstance(self.instance_1.value, PartA)

        self.assertEqual(self.instance_1.value.a, self.INPUT_1["PartA"]["a"])

    def test_instance_b(self):
        self.assertIsInstance(self.instance_2.value, PartB)

        assert isinstance(self.instance_2.value, PartB)

        self.assertEqual(self.instance_2.value.b, self.INPUT_2["PartB"]["b"])

if __name__ == "__main__":
    unittest.main()
