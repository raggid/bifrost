select * from public.cfma017 c
where recnum in (1, 3)
order by recnum;

select * from public.contrexp c where 1=1
and reg_tabela = 'NFA057'
--and reg_log_data = current_date
--and reg_evento not in ('A', 'I')
and reg_recnum in (1, 2, 10000001);

SELECT * FROM NFA057 WHERE RECNUM  = 737467;

select * from cfma017 c2
where recnum in (1, 2, 11,10000001);

INSERT INTO public.cfma017 (recnum, id_conferencia, id_produto, id_palete, id_coleta, filial_origem, filial_destino, chave_nfe, qtd_conferida, qtd_palete, situacao, log, log_hora, log_data)
VALUES(10000002, 28900000007227, 28000000014682, 2800005499, 28000000002077, 28, 34, '2800381646', 1, 1, 'FC', 'daniel', 10.40, '2016-10-19');

begin;

create or replace function notify_contrexp ()
 returns trigger
 language plpgsql
as $$
declare
  channel text := TG_ARGV[0];
begin
  PERFORM (
     with payload(recnum,reg_tabela,reg_recnum,reg_evento,reg_cols_pk,reg_dados_pk,
         reg_status,reg_log,reg_log_data,reg_log_hora,reg_fil_orige) as
     (
       select NEW.recnum ,
			NEW.reg_tabela ,
			NEW.reg_recnum ,
			NEW.reg_evento ,
			NEW.reg_cols_pk ,
			NEW.reg_dados_pk ,
			NEW.reg_status ,
			NEW.reg_log ,
			NEW.reg_log_data ,
			NEW.reg_log_hora ,
			NEW.reg_fil_origem
     )
     select pg_notify(channel, row_to_json(payload)::text)
       from payload
  );
  RETURN NULL;
end;
$$;


create TRIGGER tg_notify_contrexp
    AFTER insert or update
        ON PUBLIC.contrexp
    FOR EACH ROW
        EXECUTE PROCEDURE notify_contrexp('notifyContrexp');

commit;

