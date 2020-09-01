from app.pg_notify_service import PgListener

if __name__ == '__main__':
    # configs = Configurations()
    listener = PgListener()
    listener.run()

    # for notification in await_pg_notifications(
    #         f'postgres://{configs.postgres_string}',
    #         [f'{configs.configs["pg_notify_channel"]}']
    # ):
    #     payload = notification.payload
    #     tabela = payload['reg_tabela']
