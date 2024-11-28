from dotenv import dotenv_values


config = dotenv_values('./config/.env')
API_TOKEN = config['TOKEN']
ADMIN_ID = config['ADMIN']

