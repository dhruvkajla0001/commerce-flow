from app.etl.loaders.products_loader import ProductsLoader


def load_products():
    loader = ProductsLoader()
    loader.run()