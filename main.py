from app.flask_app import application
from app.service.pg_notify_service import listener
import signal

if __name__ == '__main__':
    application.run()

    #
    # def listen_kill_server():
    #     signal.signal(signal.SIGTERM, listener.interrupted_process)
    #     signal.signal(signal.SIGINT, listener.interrupted_process)
    #     signal.signal(signal.SIGQUIT, listener.interrupted_process)
    #     signal.signal(signal.SIGHUP, listener.interrupted_process)

    listener.run()
