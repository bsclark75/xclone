from app import create_app

# Pass your production config class here
app = create_app('config.ProductionConfig')
