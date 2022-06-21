from dataclasses import fields
import unittest
from __seedwork.domain.exceptions import ValidationException
from __seedwork.domain.validators import ValidatorFieldsInterface, ValidatorRules


class TestValidatorRules(unittest.TestCase):

    def test_values_method(self):
        validator = ValidatorRules.values("some value", "prop")
        self.assertIsInstance(validator, ValidatorRules)
        self.assertEqual(validator.value, "some value")
        self.assertEqual(validator.prop, "prop")

    def test_required_rule(self):

        invalid_data = [
            {"value": None, "prop": "prop"},
            {"value": "", "prop": "prop"},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(i["value"], i["prop"]).required()
            self.assertEqual("The prop is required",
                             assert_error.exception.args[0])

        valid_data = [
            {"value": "test", "prop": "prop"},
            {"value": 5, "prop": "prop"},
            {"value": 0, "prop": "prop"},
            {"value": False, "prop": "prop"},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i["value"], i["prop"]).required(),
                ValidatorRules
            )

    def test_string_rule(self):

        invalid_data = [
            {"value": 5, "prop": "prop"},
            {"value": True, "prop": "prop"},
            {"value": {}, "prop": "prop"},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(i["value"], i["prop"]).string()
            self.assertEqual("The prop must be a string",
                             assert_error.exception.args[0])

        valid_data = [
            {"value": None, "prop": "prop"},
            {"value": "", "prop": "prop"},
            {"value": "some values", "prop": "prop"},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i["value"], i["prop"]).string(),
                ValidatorRules
            )

    def test_max_length_rule(self):

        invalid_data = [
            {"value": "t" * 5, "prop": "prop"},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(i["value"], i["prop"]).max_length(4)
            self.assertEqual("The prop must be less than 4 characters",
                             assert_error.exception.args[0])

        valid_data = [
            {"value": None, "prop": "prop"},
            {"value": "t" * 5, "prop": "prop"},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i["value"], i["prop"]).max_length(5),
                ValidatorRules
            )

    def test_boolean_rule(self):

        invalid_data = [
            {"value": "", "prop": "prop"},
            {"value": 5, "prop": "prop"},
            {"value": {}, "prop": "prop"},
        ]

        for i in invalid_data:
            msg = f'value: {i["value"]}, prop: {i["prop"]}'
            with self.assertRaises(ValidationException, msg=msg) as assert_error:
                ValidatorRules.values(i["value"], i["prop"]).boolean()
            self.assertEqual("The prop must be a boolean",
                             assert_error.exception.args[0])

        valid_data = [
            {"value": None, "prop": "prop"},
            {"value": True, "prop": "prop"},
            {"value": False, "prop": "prop"},
        ]

        for i in valid_data:
            self.assertIsInstance(
                ValidatorRules.values(i["value"], i["prop"]).boolean(),
                ValidatorRules
            )

    def test_throw_a_validation_exception_when_combine_two_or_more_rules(self):
        # the value is required, it's not None or ""
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None, "prop").required().string().max_length(5)
        self.assertEqual("The prop is required",
                         assert_error.exception.args[0])

        # the value is not string
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5, "prop").required().string().max_length(5)
        self.assertEqual("The prop must be a string",
                         assert_error.exception.args[0])

        # the max_length is not value accept
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                "t" * 6, "prop").required().string().max_length(5)
        self.assertEqual("The prop must be less than 5 characters",
                         assert_error.exception.args[0])

        # the value is required, it's not None or ""
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                None, "prop").required()
        self.assertEqual("The prop is required",
                         assert_error.exception.args[0])

        # the is not value accept (False or True)
        with self.assertRaises(ValidationException) as assert_error:
            ValidatorRules.values(
                5, "prop").required().boolean()
        self.assertEqual("The prop must be a boolean",
                         assert_error.exception.args[0])

    def test_valid_cases_for_combination_between_rules(self):
        ValidatorRules("test", "prop").required().string()
        ValidatorRules("tests" * 1, "prop").required().string().max_length(5)
        ValidatorRules(True, "prop").required().boolean()
        ValidatorRules(False, "prop").required().boolean()
        self.assertTrue(True)


class TestValidatorFieldsInterface(unittest.TestCase):

    def test_throw_error_when_validate_method_not_implemented(self):
        with self.assertRaises(TypeError) as assert_error:
            # pylint: disable=abstract-class-instantiated
            ValidatorFieldsInterface()
        self.assertEqual(
            assert_error.exception.args[0], "Can't instantiate abstract class ValidatorFieldsInterface with abstract method validate")

    def test_fields(self):
        fields_class = fields(ValidatorFieldsInterface)
        errors_field = fields_class[0]
        self.assertEqual(errors_field.name, "errors")
        self.assertIsNone(errors_field.default)

        validated_data_field = fields_class[1]
        self.assertEqual(validated_data_field.name, "validated_data")
        self.assertIsNone(validated_data_field.default)
