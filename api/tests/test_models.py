import pytest
from api.models import Product
from decimal import Decimal

@pytest.mark.django_db
def test_create_product():
    product = Product.objects.create(
        name="Test Product",
        description="Test Description",
        price=Decimal("99.99")
    )
    assert product.name == "Test Product"
    assert product.price == Decimal("99.99") 