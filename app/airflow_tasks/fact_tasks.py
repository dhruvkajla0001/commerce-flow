from app.etl.loaders.fact_orders_loader import FactOrdersLoader


def load_fact_orders():
    loader = FactOrdersLoader()
    loader.run()