from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from apscheduler.schedulers.background import BackgroundScheduler
import atexit
from environs import Env

env = Env()
env.read_env()

app = Flask(__name__)
app.config['SECRET_KEY'] = env.str('NT_SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def loader_user(user_id):
    """Função que cria uma instancia de um usuário da Class User."""
    return User.query.get(user_id)


from apps.logins import login as login_blueprint
app.register_blueprint(login_blueprint)

from apps.home import home as home_blueprint
app.register_blueprint(home_blueprint)

from apps.register import register
app.register_blueprint(register)

from apps.structure import coin as coin_blueprint
app.register_blueprint(coin_blueprint)

from apps.api import api as edit_blueprint
app.register_blueprint(edit_blueprint)

from apps.models import User
from apps.home.crud import call_api, monitor_data


@app.before_first_request
def init_scheduler():
    """Função que antes do primeiro request inicia a função call_api e monitor_data em background."""
    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(func=call_api, trigger='cron', second=30)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())

    scheduler1 = BackgroundScheduler(daemon=True)
    scheduler1.add_job(func=monitor_data, trigger='cron', second=40)
    scheduler1.start()
    atexit.register(lambda: scheduler1.shutdown())

    # scheduler2 = BackgroundScheduler(daemon=True)
    # scheduler2.add_job(func=oi, trigger='cron', minute='*')
    # scheduler2.start()
    # atexit.register(lambda: scheduler2.shutdown())


if __name__ == "__main__":
    app.run(debug=False)
