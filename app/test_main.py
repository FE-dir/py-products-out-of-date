import datetime
import pytest
import app.main as main


@pytest.fixture
def sample_products() -> list:
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


def test_outdated_products(mocker, sample_products) -> None:
    mock_date = mocker.patch("app.main.datetime.date", wraps=datetime.date)
    mock_date.today.return_value = datetime.date(2022, 2, 2)
    assert main.outdated_products(sample_products) == ["duck"]


def test_outdated_products_no_expired(mocker, sample_products) -> None:
    mock_date = mocker.patch("app.main.datetime.date", wraps=datetime.date)
    mock_date.today.return_value = datetime.date(2022, 1, 31)
    assert main.outdated_products(sample_products) == []


def test_outdated_products_all_expired(mocker, sample_products) -> None:
    mock_date = mocker.patch("app.main.datetime.date", wraps=datetime.date)
    mock_date.today.return_value = datetime.date(2023, 1, 1)
    assert main.outdated_products(sample_products) == [
        "salmon",
        "chicken",
        "duck",
    ]


def test_expiration_day_today_not_outdated(mocker, sample_products) -> None:
    mock_date = mocker.patch("app.main.datetime.date", wraps=datetime.date)
    mock_date.today.return_value = datetime.date(2022, 2, 10)
    assert main.outdated_products(sample_products) == ["chicken", "duck"], (
        "Product with expiration date equal to today should NOT be outdated."
    )
