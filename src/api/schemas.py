from typing import Optional
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from src.db import models


class PostBase(BaseModel):
    text: str = Field(
        ...,
        description="Post text",
        json_schema_extra={"example": "This is the best post ever made"},
    )


class PostCreate(PostBase):
    rubrics: list[str] = Field(
        ...,
        description="Rubrics to which the post will belong",
        json_schema_extra={"example": ["VK_228", "VK_1337"]},
    )


class PostUpdate(BaseModel):
    text: Optional[str] = Field(
        None,
        description="New post text",
        json_schema_extra={
            "example": "This is changed post but still the best post ever made"
        },
    )


class Post(PostBase):
    id: int = Field(
        ...,
        description="Post ID",
        json_schema_extra={"example": "1"},
    )
    created_date: datetime = Field(
        ...,
        description="Post creation date",
        json_schema_extra={"example": "2026-07-02 03:27:30.162073"},
    )
    rubrics: list[str] = Field(
        [],
        description="Rubrics to which the post will belong",
        json_schema_extra={"example": ["VK_228", "VK_1337"]},
    )

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate_with_rubrics(cls, post: models.Post, rubrics: list[str]):
        return cls(
            id=post.id, text=post.text, created_date=post.created_date, rubrics=rubrics
        )


class RubricBase(BaseModel):
    vk_id: str = Field(
        ...,
        description="Rubrics unique ID",
        json_schema_extra={"example": "VK_228"},
    )
    post_id: int = Field(
        ...,
        description="ID of the post rubric belong to",
        json_schema_extra={"example": "VK_228"},
    )


class RubricCreate(RubricBase):
    pass


class RubricUpdate(BaseModel):
    vk_id: Optional[str] = Field(
        None,
        description="Rubrics unique ID",
        json_schema_extra={"example": "VK_228"},
    )


class Rubric(RubricBase):
    id: int = Field(
        ...,
        description="Rubrics DB ID",
        json_schema_extra={"example": "VK_228"},
    )

    model_config = ConfigDict(from_attributes=True)


class SearchRequest(BaseModel):
    text: str = Field(
        ...,
        description="Text query to search among posts texts",
        json_schema_extra={"example": "Привет"},
    )


class SearchResponse(BaseModel):
    posts: list[Post] = Field(
        ...,
        description="Posts found for search query",
        json_schema_extra={
            "example": """
{
  "posts": [
    {
      "text": "Привет вам из детства, от Сашеньки и Вовки❤ они сейчас наваляются вдоволь, промокнут до нитки и греться бегом домой, к батарее. \nА какое настроение у вас? ❄",
      "id": 1158,
      "created_date": "2026-07-02T03:44:11.217925",
      "rubrics": [
        "VK-1603736028819866",
        "VK-10847316026",
        "VK-27470760776"
      ]
    },
    ... 19 more
  ]
}
"""
        },
    )
