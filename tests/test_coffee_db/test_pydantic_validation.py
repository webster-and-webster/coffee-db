from pydantic import BaseModel, validator
import pytest

from coffee_db.coffee import check_name, tasting_notes_must_be_lower_case, elevation_must_be_greater_than_zero
from coffee_db.validate import validate_payload


class DummyClass(BaseModel):
    name: str
    tasting_notes: str
    elevation: int

    _check_name = validator("name", allow_reuse=True)(check_name)
    _check_tasting_notes = validator("tasting_notes", allow_reuse=True)(
        tasting_notes_must_be_lower_case
    )
    _check_elevation = validator("elevation", allow_reuse=True)(
        elevation_must_be_greater_than_zero
    )


@pytest.fixture(scope="module")
def dummy_class():
    return DummyClass


def test_validate_payload_pass(dummy_class):

    payload = {"name": "Name", "tasting_notes": "one, two, three", "elevation": 1}

    output = validate_payload(payload, dummy_class)

    assert isinstance(output, dummy_class)


def test_name_fail(dummy_class):

    payload = {"name": "name", "tasting_notes": "one, two, three", "elevation": 1}
    output = validate_payload(payload, dummy_class)

    assert output == "'Name must be capitalized'"


def test_tasting_notes_fails(dummy_class):

    payload = {"name": "Name", "tasting_notes": "some, Upper", "elevation": 1}
    output = validate_payload(payload, dummy_class)

    assert output == "'tasting notes must be comma separated, and lower case'"


def test_elevation_fails(dummy_class):

    payload = {"name": "Name", "tasting_notes": "one, two, three", "elevation": -1}
    output = validate_payload(payload, dummy_class)

    assert output == "'elevation must be greater than zero'"
