from playwright.sync_api import Page, expect

from pages.base_page import basePage

class ProductPage(basePage):
    def __init__(self, page: Page):
        super().__init__(page)

        self.product_items = page.locator(".inventory_item")
        self.product_names = page.locator(".inventory_item_name")
        self.product_price = page.locator(".inventory_item_price")
        self.sort_container = page.locator('[data-test="product-sort-container"]')
        self.cart_link = page.locator('.shopping_cart_link')
        self.cart_bridge = page.locator('.shopping_cart_badge')
        self.product_in_cart = page.locator('[data-test="inventory-item"]')

    def get_product_count(self):
        return self.product_items.count()
    
    def get_product_name(self):
        return self.product_names.all_text_contents()

    def sort_products(self, sort_option: str):
        self.sort_container.select_option(sort_option)
    
    def get_product_prices(self):
        prices = self.product_price.all_text_contents()
        return [float(price.replace("$", "")) for price in prices]
    
    def add_product_to_cart(self, product_name: str):
        # product = self.product_items.filter(has=self.page.get_by_text(product_name, exact=True))
        # product.get_by_role("button", name="Add to cart").click()


        self.page.locator(f"//*[@id='add-to-cart-{product_name.lower()}']").click()
    
    def open_cart(self):
        self.cart_link.click()

    def remove_product_from_cart(self, product_name: str):
        self.open_cart()
        self.page.locator(f"//*[@id='remove-{product_name.lower()}']").click()
