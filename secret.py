import os
from werkzeug.security import check_password_hash,generate_password_hash

print(os.urandom(12))

print(generate_password_hash("KIKO"))