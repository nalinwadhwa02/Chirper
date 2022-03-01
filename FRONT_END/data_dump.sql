--
-- PostgreSQL database dump
--

-- Dumped from database version 14.2 (Ubuntu 14.2-1.pgdg20.04+1)
-- Dumped by pg_dump version 14.2 (Ubuntu 14.2-1.pgdg20.04+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: like_nums; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.like_nums (
    tweetid integer,
    like_num bigint
);


ALTER TABLE public.like_nums OWNER TO postgres;

--
-- Name: likes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.likes (
    tweetid integer,
    userid integer
);


ALTER TABLE public.likes OWNER TO postgres;

--
-- Name: network; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.network (
    fr integer,
    fe integer
);


ALTER TABLE public.network OWNER TO postgres;

--
-- Name: tweets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tweets (
    tweetid integer NOT NULL,
    userid integer,
    tweettime timestamp without time zone NOT NULL,
    tweet text NOT NULL,
    response_tweets integer[],
    in_response_to_tweet integer[]
);


ALTER TABLE public.tweets OWNER TO postgres;

--
-- Name: tweets_tweetid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tweets_tweetid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tweets_tweetid_seq OWNER TO postgres;

--
-- Name: tweets_tweetid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tweets_tweetid_seq OWNED BY public.tweets.tweetid;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    userid integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_userid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_userid_seq OWNER TO postgres;

--
-- Name: users_userid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_userid_seq OWNED BY public.users.userid;


--
-- Name: tweets tweetid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets ALTER COLUMN tweetid SET DEFAULT nextval('public.tweets_tweetid_seq'::regclass);


--
-- Name: users userid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN userid SET DEFAULT nextval('public.users_userid_seq'::regclass);


--
-- Data for Name: like_nums; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.like_nums (tweetid, like_num) FROM stdin;
\.


--
-- Data for Name: likes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.likes (tweetid, userid) FROM stdin;
\.


--
-- Data for Name: network; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.network (fr, fe) FROM stdin;
\.


--
-- Data for Name: tweets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tweets (tweetid, userid, tweettime, tweet, response_tweets, in_response_to_tweet) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (userid, username, password) FROM stdin;
\.


--
-- Name: tweets_tweetid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tweets_tweetid_seq', 1, false);


--
-- Name: users_userid_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_userid_seq', 1, false);


--
-- Name: tweets tweets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_pkey PRIMARY KEY (tweetid);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (userid);


--
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- Name: likes likes_tweetid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_tweetid_fkey FOREIGN KEY (tweetid) REFERENCES public.tweets(tweetid);


--
-- Name: likes likes_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.likes
    ADD CONSTRAINT likes_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- Name: network network_fe_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.network
    ADD CONSTRAINT network_fe_fkey FOREIGN KEY (fe) REFERENCES public.users(userid);


--
-- Name: network network_fr_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.network
    ADD CONSTRAINT network_fr_fkey FOREIGN KEY (fr) REFERENCES public.users(userid);


--
-- Name: tweets tweets_userid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tweets
    ADD CONSTRAINT tweets_userid_fkey FOREIGN KEY (userid) REFERENCES public.users(userid);


--
-- PostgreSQL database dump complete
--

