from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_restful import Api,Resource

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    api = Api(app)
    from .views import views
    from .auth import auth
    from .models import User, Note

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    
    

    class Notes(Resource):
    
        def get(self,sno):
            car = Note.query.filter_by(id=sno).first()
        
            if car:
                return car.json()
            else:
                return {'name':None},404

        def post(self,sno,data):
            car = Note(id=sno,data=data,date="",user_id=10)
            db.session.add(car)
            db.session.commit()

            return car.json()
         
        def delete(self,sno):
            car = Note.query.filter_by(id=sno).first()
            db.session.delete(car)
            db.session.commit()

            return {'note' : 'Delete Success'}
          

    class Allnotes(Resource):
        def get(self):
            cars = Note.query.all()
            return [car.json() for car in cars]
            
    class Addnotes(Resource):
        def post(self,data,sno):
            car = Note(id=sno,data=data,user_id=10)
            db.session.add(car)
            db.session.commit()

            return car.json()



    api.add_resource(Notes,'/note/<int:sno>')
    api.add_resource(Allnotes, '/notes')
    api.add_resource(Addnotes,'/addnotes/<int:sno>,<string:data>')


   

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')