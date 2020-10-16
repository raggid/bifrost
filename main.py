from app.resources.configurations import Configurations
from app.pg_notify_service import PgListener
from app.service.kafka_service import consumer

if __name__ == '__main__':

    configurations = Configurations().configs

    listener = PgListener(configurations)
    listener.run()


    def test_commit():
        pass




