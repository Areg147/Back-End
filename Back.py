from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

app = Flask(__name__)
CORS(app)

# Database setup
engine = create_engine('sqlite:///data.db')
Base = declarative_base()

class Info(Base):
    __tablename__ = 'info'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@app.route('/')
def home():
    return "Barev Dzez Ynkerner jan"

@app.route('/add', methods=['POST'])
def add_info():
    print("Areg")
    data = request.json
    session = Session()
    new_info = Info(name=data['name'], email=data['email'])
    session.add(new_info)
    session.commit()
    session.close()
    return jsonify({'message': 'Info added successfully'}), 201

@app.route('/list', methods=['GET'])
def list_info():
    session = Session()
    infos = session.query(Info).all()
    session.close()
    return jsonify([{'id': i.id, 'name': i.name, 'email': i.email} for i in infos])

if __name__ == '__main__':
    app.run(debug=True)