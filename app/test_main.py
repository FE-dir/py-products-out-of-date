import datetime
import pytest
from unittest.mock import patch
import app.main as main
from typing import List, Dict, Any


@pytest.fixture
def sample_products() -> List[Dict[str, Any]]:
    return [
        {
            "name": "salmon",
            "expiration_date": datetime.date(2022, 2, 10),
            "price": 600,
        },
        {
            "name": "chicken",
            "expiration_date": datetime.date(2022, 2, 5),
            "price": 120,
        },
        {
            "name": "duck",
            "expiration_date": datetime.date(2022, 2, 1),
            "price": 160,
        },
    ]


def test_outdated_products(sample_products: List[Dict[str, Any]]) -> None:
    with patch("app.main.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(2022, 2, 2)
        assert main.outdated_products(sample_products) == ["duck"]


def test_outdated_products_no_expired(sample_products: List[Dict[str, Any]]) -> None:
    with patch("app.main.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(2022, 1, 31)
        assert main.outdated_products(sample_products) == []


def test_outdated_products_all_expired(sample_products: List[Dict[str, Any]]) -> None:
    with patch("app.main.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(2023, 1, 1)
        assert main.outdated_products(sample_products) == [
            "salmon",
            "chicken",
            "duck",
        ]


def test_expiration_day_today_not_outdated(sample_products: List[Dict[str, Any]]) -> None:
    with patch("app.main.datetime") as mock_datetime:
        mock_datetime.date.today.return_value = datetime.date(2022, 2, 10)
        assert main.outdated_products(sample_products) == ["chicken", "duck"], (
            "Product with expiration date equal to today should NOT be outdated."
        )
