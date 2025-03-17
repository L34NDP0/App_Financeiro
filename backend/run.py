# backend/run.py
from app import create_app, db
import os

app = create_app()

#criando banco de dados
with app.app_context():
        db.create_all()
        
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))    
    app.run(host="localhost", port=port, debug=True)