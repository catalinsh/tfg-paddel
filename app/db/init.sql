CREATE TABLE public.users (
    id integer NOT NULL,
    username character varying NOT NULL,
    password character varying NOT NULL,
    removable boolean NOT NULL DEFAULT TRUE
);

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);

CREATE INDEX ix_users_id ON public.users USING btree (id);

CREATE UNIQUE INDEX ix_users_username ON public.users USING btree (username);

-- pass: secret
INSERT INTO users (username, password, removable) VALUES ('test', '$2b$12$vnsrvn1IFh2ZFGjBPRABYuQz/gg/0rfKm55ocs6H8/q5xuM7U60Se', FALSE);

-- pass: 1234
INSERT INTO users (username, password) VALUES ('abcd', '$2b$12$E0PJHV9G8k4DTF/sZSQIGuk2FVKhbpv.8EBtDKTdfTgRWrZLLt9Mq');
