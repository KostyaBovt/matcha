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
    birth date,
    gender integer,
    sex_preference integer,
    phone  character varying(128),
    bio text,
    geo boolean DEFAULT false NOT NULL,
    geo_type integer DEFAULT 1 NOT NULL,
    geo_lat numeric(10,5),
    geo_lng numeric(10,5),
    rating numeric(5,4) DEFAULT 0.5 NOT NULL
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


-- crate table for registering logged users and tokens
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


-- crate table list all ineterests used in system
DROP TABLE IF EXISTS interests;

CREATE TABLE interests (
  id integer NOT NULL,
  interest character varying(256) NOT NULL
);

ALTER TABLE ONLY interests
    ADD CONSTRAINT interests_pk PRIMARY KEY (id);

CREATE SEQUENCE interests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE ONLY interests ALTER COLUMN id SET DEFAULT nextval('interests_id_seq'::regclass);


-- crate table for store interests per each user
DROP TABLE IF EXISTS users_interests;

CREATE TABLE users_interests (
  user_id integer NOT NULL,
  interest_id integer NOT NULL
);

ALTER TABLE ONLY users_interests
    ADD CONSTRAINT users_interests_pk PRIMARY KEY (user_id, interest_id);

ALTER TABLE ONLY users_interests
    ADD CONSTRAINT users_interests_user_id_fkey FOREIGN KEY (user_id) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY users_interests
    ADD CONSTRAINT users_interests_interest_id_fkey FOREIGN KEY (interest_id) REFERENCES interests(id) ON UPDATE CASCADE ON DELETE CASCADE;



-- crate table to store likes and dislikes
DROP TABLE IF EXISTS likes;

CREATE TABLE likes (
  user_id_1 integer NOT NULL,
  user_id_2 integer NOT NULL,
  action integer NOT NULL
);

ALTER TABLE ONLY likes
    ADD CONSTRAINT likes_pk PRIMARY KEY (user_id_1, user_id_2);

ALTER TABLE ONLY likes
    ADD CONSTRAINT likes_user_id_1_fkey FOREIGN KEY (user_id_1) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY likes
    ADD CONSTRAINT likes_user_id_2_fkey FOREIGN KEY (user_id_2) REFERENCES users(id) ON UPDATE CASCADE ON DELETE CASCADE;



-- DATA INSERT
insert into users (id, email, password, confirmed) values (48, 'kostya.bovt@gmail.com', 'c4ca4238a0b923820dcc509a6f75849b', 1);
insert into users (id, email, password, confirmed) values (100, 'some.email@gmail.com', 'c4ca4238a0b923820dcc509a6f75849b', 1);

insert into users_info (user_id, username, fname, sname, birth, gender, sex_preference, phone, bio) values (48, 'Dobro', 'Kostia', 'Bovt', '1990-12-16', 1, 2, '+380997741343', 'Hello we can meet in the park and walk a dog');
insert into users_info (user_id, username, fname, sname, birth, gender, sex_preference, phone, bio) values (100, 'Sweety', 'Angela', 'Maldini', '1996-04-23', 2, 3, '+380937776655', 'I am pretty girl and wnat to mmet my boy');

insert into interests (interest) values ('football');
insert into interests (interest) values ('dogs');
insert into interests (interest) values ('science');
insert into interests (interest) values ('food');
insert into interests (interest) values ('FIFA');
insert into interests (interest) values ('flowers');
insert into interests (interest) values ('fun');
insert into interests (interest) values ('cars');

insert into users_interests (user_id, interest_id) values (48, 1);
insert into users_interests (user_id, interest_id) values (48, 2);
insert into users_interests (user_id, interest_id) values (48, 3);
insert into users_interests (user_id, interest_id) values (48, 4);
insert into users_interests (user_id, interest_id) values (48, 5);
insert into users_interests (user_id, interest_id) values (48, 6);
insert into users_interests (user_id, interest_id) values (100, 7);
insert into users_interests (user_id, interest_id) values (100, 8);
insert into users_interests (user_id, interest_id) values (100, 9);
insert into users_interests (user_id, interest_id) values (100, 1);
insert into users_interests (user_id, interest_id) values (100, 4);

insert into likes (user_id_1, user_id_2, action) values (48, 100, 1);
insert into likes (user_id_1, user_id_2, action) values (100, 48, 1);


