# backend/run.py
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host="localhost", port=8051, debug=True)
    
    
#if __name__ == '__main__':
 #   with app.app_context():
  #      db.create_all()
   # port = int(os.environ.get("PORT", 8051))
    #app.run(host="localhost", port=port, debug=True)