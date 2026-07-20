from app.etl.loaders.sellers_loader import SellersLoader


def load_sellers():
    loader = SellersLoader()
    loader.run()