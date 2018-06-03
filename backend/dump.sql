DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id integer NOT NULL,
    email character varying(128) NOT NULL,
    password character varying(128) NOT NULL,
    confirmed integer NOT NULL
);

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pk PRIMARY KEY (id);

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


DROP TABLE IF EXISTS confirm;

CREATE TABLE confirm (
  id integer NOT NULL,
  user_id integer NOT NULL,
  email_hash character varying(256) NOT NULL,
  confirm_hash character varying(256) NOT NULL
);

ALTER TABLE ONLY confirm
    ADD CONSTRAINT confirm_pk PRIMARY KEY (id);

CREATE SEQUENCE confirm_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY confirm ALTER COLUMN id SET DEFAULT nextval('confirm_id_seq'::regclass);

ALTER TABLE ONLY confirm
    ADD CONSTRAINT confirm_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;


DROP TABLE IF EXISTS forgot;

CREATE TABLE forgot (
  id integer NOT NULL,
  user_id integer NOT NULL,
  email_hash character varying(256) NOT NULL,
  reset_hash character varying(256) NOT NULL
);

ALTER TABLE ONLY forgot
    ADD CONSTRAINT forgot_pk PRIMARY KEY (id);

CREATE SEQUENCE forgot_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY forgot ALTER COLUMN id SET DEFAULT nextval('forgot_id_seq'::regclass);

ALTER TABLE ONLY forgot
    ADD CONSTRAINT  forgot_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;
