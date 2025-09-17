from dotenv import load_dotenv
import multiprocessing
import os


load_dotenv()

workers = int(os.getenv('GUNICORN_PROCESSES', multiprocessing.cpu_count() * 2))
threads = int(os.getenv('GUNICORN_THREADS', '4'))
timeout = int(os.getenv('GUNICORN_TIMEOUT', '120'))

bind = os.getenv('GUNICORN_BIND', '0.0.0.0:8082')

forwarded_allow_ips = os.getenv('GUNICORN_FORWARDED_ALLOW_IPS', '*')

secure_scheme_headers = {'X-Forwarded-Proto': 'https'}
