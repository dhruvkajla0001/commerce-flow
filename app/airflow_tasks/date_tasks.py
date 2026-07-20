from app.etl.loaders.dates_loader import DatesLoader


def load_dates():
    loader = DatesLoader()
    loader.run()