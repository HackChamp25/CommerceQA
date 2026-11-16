import pytest

from pages.products_page import ProductPage
from utils.test_data_reader import load_test_data

SORT_DATA = load_test_data("product_sort_order.json")


@pytest.mark.ui
@pytest.mark.regression
def test_product_listing(authenticated_page):
    products_page = ProductPage(authenticated_page)
    assert products_page.get_product_count() == 6

    product_names = products_page.get_product_name()
    assert "Sauce Labs Backpack" in product_names

@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.parametrize("test_data", SORT_DATA, ids = [item['description'] for item in SORT_DATA])
def test_sort_products(authenticated_page, test_data):
    products_page = ProductPage(authenticated_page)
    products_page.sort_products(test_data['sort_option'])
    prices = products_page.get_product_prices()
    if test_data['expected_order'] == 'ascending':
        assert prices == sorted(prices)
    else:
        assert prices == sorted(prices, reverse=True)
    
@pytest.mark.ui
@pytest.mark.regression
def test_add_product_to_cart(authenticated_page):
    products_page = ProductPage(authenticated_page)
    products_page.add_product_to_cart("Sauce-Labs-Backpack")
    products_page.open_cart()
    assert products_page.product_in_cart.count() == 1
    assert "Sauce Labs Backpack" in products_page.get_product_name()

@pytest.mark.ui
@pytest.mark.regression
def test_remove_product_from_cart(authenticated_page):
    products_page = ProductPage(authenticated_page)
    products_page.add_product_to_cart("Sauce-Labs-Backpack")
    products_page.remove_product_from_cart("Sauce-Labs-Backpack")
    assert products_page.product_in_cart.count() == 0
    assert "Sauce Labs Backpack" not in products_page.get_product_name()

