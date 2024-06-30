# coding: utf-8

from __future__ import annotations
from datetime import date, datetime  # noqa: F401

import re  # noqa: F401
from typing import Any, Dict, List, Optional  # noqa: F401

from pydantic import AnyUrl, BaseModel, EmailStr, Field, validator  # noqa: F401


class CatForCoffeeResponse(BaseModel):
    """NOTE: This class is auto generated by
    OpenAPI Generator (https://openapi-generator.tech).

    Do not edit the class manually.

    CatForCoffeeResponse - a model defined in OpenAPI

        id: The id of this CatForCoffeeResponse.
    """

    id: int = Field(alias="id")


CatForCoffeeResponse.update_forward_refs()