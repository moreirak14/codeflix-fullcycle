from dataclasses import FrozenInstanceError, is_dataclass
import unittest
import uuid
from __seedwork.domain.exceptions import InvalidUuidException
from __seedwork.domain.value_objects import UniqueEntityId
from unittest.mock import patch


class TestUniqueEntityIdUnit(unittest.TestCase):

    def test_if_is_a_dataclass(self):
        self.assertTrue(is_dataclass(UniqueEntityId))

    def test_throw_exception_when_uuid_is_invalid(self):
        with patch.object(
            UniqueEntityId,
            "_UniqueEntityId__validate",
            autospec=True,
            side_effect=UniqueEntityId._UniqueEntityId__validate
        ) as mock_validate:

            with self.assertRaises(InvalidUuidException) as error:
                UniqueEntityId("Fake ID")
            
            mock_validate.assert_called_once()
            self.assertEqual(error.exception.args[0], "ID must be a valid UUID")

    def test_accept_uuid_passed_in_constructor(self):
        with patch.object(
                UniqueEntityId,
                "_UniqueEntityId__validate",
                autospec=True,
                side_effect=UniqueEntityId._UniqueEntityId__validate
            ) as mock_validate:

                value_object = UniqueEntityId("6eac08e5-5a54-4d2b-afeb-16253d0e75fb")
                mock_validate.assert_called_once()
                self.assertEqual(value_object.id, "6eac08e5-5a54-4d2b-afeb-16253d0e75fb")
        
        #without mock validate
        uuid_value = uuid.uuid4()
        value_object = UniqueEntityId(uuid_value)
        self.assertEqual(value_object.id, str(uuid_value))

    def test_generate_id_when_no_passed_id_in_constructor(self):
        with patch.object(
                UniqueEntityId,
                "_UniqueEntityId__validate",
                autospec=True,
                side_effect=UniqueEntityId._UniqueEntityId__validate
            ) as mock_validate:
            value_object = UniqueEntityId()
            uuid.UUID(value_object.id)
            mock_validate.assert_called_once()

    def test_is_immutable(self):
        with self.assertRaises(FrozenInstanceError):
            value_object = UniqueEntityId()
            value_object.id = "Fake ID"
