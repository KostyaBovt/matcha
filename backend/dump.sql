-- create user table

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


-- create user table

DROP TABLE IF EXISTS users_info;
CREATE TABLE users_info (
    id integer NOT NULL,
    user_id integer NOT NULL,
    username character varying(128),
    fname character varying(128),
    sname character varying(128),
    gender integer,
    sex_preference integer,
    phone  character varying(128),
    bio text,
    geo boolean DEFAULT false NOT NULL,
    geo_type integer DEFAULT 1 NOT NULL,
    geo_lat numeric(5,5),
    geo_lng numeric(5,5)
);

ALTER TABLE ONLY users_info
    ADD CONSTRAINT users_info_pk PRIMARY KEY (id);

CREATE SEQUENCE users_info_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY users_info ALTER COLUMN id SET DEFAULT nextval('users_info_id_seq'::regclass);

ALTER TABLE ONLY users_info
    ADD CONSTRAINT users_info_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;

-- create table for confirmation hash
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


-- crate table for reset hash if forgot password
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


-- crate table for register logged users and tokens
DROP TABLE IF EXISTS login;

CREATE TABLE login (
  id integer NOT NULL,
  user_id integer NOT NULL,
  token character varying(256) NOT NULL,
  last_seen timestamp(0) DEFAULT now() NOT NULL
);

ALTER TABLE ONLY login
    ADD CONSTRAINT login_pk PRIMARY KEY (id);

CREATE SEQUENCE login_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY login ALTER COLUMN id SET DEFAULT nextval('login_id_seq'::regclass);

ALTER TABLE ONLY login
    ADD CONSTRAINT  login_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;





-- DATA INSERT
insert into users_info (user_id, username, fname, sname, gender, sex_preference, phone, bio) values (48, 'Dobro', 'Kostia', 'Bovt', 1, 2, '+380997741343', 'Hello we can meet in the park and walk a dog');
