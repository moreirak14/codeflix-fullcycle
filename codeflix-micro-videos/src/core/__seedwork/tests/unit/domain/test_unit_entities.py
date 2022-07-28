# pylint: disable=unexpected-keyword-arg
from abc import ABC
from dataclasses import dataclass, is_dataclass
import unittest
from core.__seedwork.domain.entities import Entity
from core.__seedwork.domain.value_objects import UniqueEntityId


@dataclass(kw_only=True, frozen=True)
class StubEntity(Entity):
    prop1: str
    prop2: str


class TestEntityUnit(unittest.TestCase):
    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(Entity))

    def test_if_is_a_abstract_class(self):
        self.assertIsInstance(Entity(), ABC)

    def test_set_unique_entity_id_and_props(self):
        entity = StubEntity(prop1="value1", prop2="value2")
        self.assertEqual(entity.prop1, "value1")
        self.assertEqual(entity.prop2, "value2")
        self.assertIsInstance(entity.unique_entity_id, UniqueEntityId)
        self.assertEqual(entity.unique_entity_id.id, entity.id)

    def test_accept_a_valid_uuid(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("6eac08e5-5a54-4d2b-afeb-16253d0e75fb"),
            prop1="value1",
            prop2="value2",
        )
        self.assertEqual(entity.id, "6eac08e5-5a54-4d2b-afeb-16253d0e75fb")

    def test_to_dict_method(self):
        entity = StubEntity(
            unique_entity_id=UniqueEntityId("6eac08e5-5a54-4d2b-afeb-16253d0e75fb"),
            prop1="value1",
            prop2="value2",
        )
        self.assertDictEqual(
            entity.to_dict(),
            {
                "id": "6eac08e5-5a54-4d2b-afeb-16253d0e75fb",
                "prop1": "value1",
                "prop2": "value2",
            },
        )

    def test_set_method(self):
        entity = StubEntity(prop1="value1", prop2="value2")
        entity._set("prop1", "changed")  # pylint: disable=protected-access
        self.assertEqual(entity.prop1, "changed")
