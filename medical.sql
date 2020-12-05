--
-- PostgreSQL database dump
--

-- Dumped from database version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.12 (Ubuntu 10.12-0ubuntu0.18.04.1)

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

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: doctors; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.doctors (
    doctor_id integer NOT NULL,
    full_name character varying(80) NOT NULL,
    spanish boolean NOT NULL,
    portuguese boolean NOT NULL,
    address text NOT NULL,
    longitude character varying(80),
    latitude character varying(80)
);


ALTER TABLE public.doctors OWNER TO vagrant;

--
-- Name: doctors_doctor_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.doctors_doctor_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.doctors_doctor_id_seq OWNER TO vagrant;

--
-- Name: doctors_doctor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.doctors_doctor_id_seq OWNED BY public.doctors.doctor_id;


--
-- Name: doctors_specialties; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.doctors_specialties (
    doctor_id integer NOT NULL,
    specialty_id integer NOT NULL
);


ALTER TABLE public.doctors_specialties OWNER TO vagrant;

--
-- Name: favorites; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.favorites (
    favorite_id integer NOT NULL,
    user_id integer,
    doctor_id integer
);


ALTER TABLE public.favorites OWNER TO vagrant;

--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.favorites_favorite_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.favorites_favorite_id_seq OWNER TO vagrant;

--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.favorites_favorite_id_seq OWNED BY public.favorites.favorite_id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.reviews (
    review_id integer NOT NULL,
    user_id integer,
    doctor_id integer,
    review_content text NOT NULL
);


ALTER TABLE public.reviews OWNER TO vagrant;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.reviews_review_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reviews_review_id_seq OWNER TO vagrant;

--
-- Name: reviews_review_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.reviews_review_id_seq OWNED BY public.reviews.review_id;


--
-- Name: specialties; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.specialties (
    specialty_id integer NOT NULL,
    specialty character varying(80) NOT NULL
);


ALTER TABLE public.specialties OWNER TO vagrant;

--
-- Name: specialties_specialty_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.specialties_specialty_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.specialties_specialty_id_seq OWNER TO vagrant;

--
-- Name: specialties_specialty_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.specialties_specialty_id_seq OWNED BY public.specialties.specialty_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: vagrant
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    username character varying(120) NOT NULL,
    email character varying(120) NOT NULL,
    password character varying(300) NOT NULL
);


ALTER TABLE public.users OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: vagrant
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO vagrant;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: vagrant
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: doctors doctor_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.doctors ALTER COLUMN doctor_id SET DEFAULT nextval('public.doctors_doctor_id_seq'::regclass);


--
-- Name: favorites favorite_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.favorites ALTER COLUMN favorite_id SET DEFAULT nextval('public.favorites_favorite_id_seq'::regclass);


--
-- Name: reviews review_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.reviews ALTER COLUMN review_id SET DEFAULT nextval('public.reviews_review_id_seq'::regclass);


--
-- Name: specialties specialty_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.specialties ALTER COLUMN specialty_id SET DEFAULT nextval('public.specialties_specialty_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: doctors; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.doctors (doctor_id, full_name, spanish, portuguese, address, longitude, latitude) FROM stdin;
9	Dr. Hyun Bang	t	f	2001 Van Ness Ave, Suite 401, San Francisco, CA 94109	-122.423346	37.794087
10	Dr. Son Le	t	f	909 Hyde St, Suite 541, San Francisco, CA 94109	-122.41761	37.789493
11	Dr. Linda Yip	t	f	735 Larkin St, San Francisco, CA 94109	-122.418102	37.784821
12	Dr. Leila Azad	t	f	180 Montgomery St, Suite 2440, San Francisco, CA 94104	-122.401969	37.790736
13	Dr. Inna Rostker	t	f	109 Stevenson St, Suite 200, San Francisco, CA 94105	-122.400958	37.788587
14	Dr. Justin Hall	t	f	450 Sutter St, Suite 1330, San Francisco, CA 94108	-122.407834	37.789657
15	Dr. Jarrod Cornehl	t	t	260 Stockton St, Fourth Floor, San Francisco, CA 94108	-122.406501	37.788319
16	Dr. Haleh Bafekr	t	f	490 Post St, Suite 549, San Francisco, CA 94102	-122.40983	37.78831
17	Dr. Kenneth Karamyan	t	f	3309 Fillmore St, San Francisco, CA 94123	-122.436413	37.800102
18	Dr. Annum Hassan	t	f	3210 Fillmore St, Suite 2, San Francisco, CA 94123	-122.435714	37.799169
19	Dr. Anisha Kahai	t	f	2100 Webster St, Suite 325, San Francisco, CA 94115	-122.43214	37.790526
20	Dr. Sheila Shahabi	t	f	345 California St, Ste 170, San Francisco, CA 94104	-122.400439	37.792602
22	Dr. Jasmine Bhuva	t	f	22 Battery St, Suite 910, San Francisco, CA 9411	-122.399363	37.791576
23	Dr. Ben Amini	t	f	120 Battery St, San Francisco, CA 94111	-122.399416	37.792525
33	Dr. George Markle	t	f	450 Sutter St, Suite 1919, San Francisco, CA 94108	-122.407834	37.789657
34	Dr. Derrick Chua	t	f	2489 Mission St, Suite 12, San Francisco, CA 94110	-122.418604	37.757258
35	Dr. Nathaniel Minami	t	f	2780 Mission St, San Francisco, CA 94110	-122.41882	37.752572
36	Dr. Joanne Jeng	t	f	380 20th Ave, Suite 102, San Francisco, CA 94121	-122.479162	37.780737
37	Dr. Victoria Tobar	t	f	800 Santiago St, San Francisco, CA 94116	-122.476357	37.744942
43	Dr. Elena Heredia	t	f	3210 Fillmore St, Suite 2,San Francisco, CA 94123	-122.435714	37.799169
2	Dr. Steven Sloan	t	f	1 Shrader St, Suite 578, San Francisco, CA 94117	-122.453308	37.77459
3	Dr. Azucena Arguelles	t	f	909 Hyde St, Suite 423, San Francisco, CA 94109	-122.41761	37.789493
4	Dr. Clifford Chew	t	f	929 Clay St, Suite 501, San Francisco, CA 94108	-122.408323	37.793851
5	Dr. Abraham Yu-Hong Law	t	f	450 Sutter St, Suite 1723, San Francisco, CA 94108	-122.407834	37.789657
6	Dr. Candice So	t	f	1237 Van Ness Ave, Suite 300, San Francisco, CA 94109	-122.42186	37.78712
7	Dr. Katherine Hipp	t	f	133 Kearny St, Suite 300, San Francisco, CA 94108	-122.404042	37.789235
8	Dr. Henry Oyharcabal	t	f	2305 Van Ness Ave, Suite B, San Francisco, CA 94109	-122.424025	37.79686
21	Dr. Matthew C. Keyser	t	f	115 Sansome St, Suite 1000, San Francisco, CA 94104	-122.401038	37.791427
24	Dr. Lucia Tuffanelli	t	f	450 Sutter St, Suite 1306, San Francisco, CA 94108	-122.407834	37.789657
25	Dr. David Stamper	t	f	2508 Mission St, San Francisco, CA 94110	-122.419142	37.756809
26	Dr. Aris Carcamo	t	f	1000 Valencia St, San Francisco, CA 94110	-122.421398	37.756692
27	Dr. Ruby Sanchez	t	f	2490 Mission St, San Francisco, CA 94110	-122.419213	37.757187
28	Dr. Mary Ann Banez	t	f	2186 Geary Blvd, Suite 312, San Francisco, CA 94115	-122.439293	37.783699
29	Dr. Amy Thich	t	f	1844 Divisadero St, San Francisco, CA 94115	-122.439978	37.786933
30	Dr. William Ellis	t	f	111 Maiden Lane, Suite 700, San Francisco, CA 94108	-122.405473	37.787987
31	Dr. Michelle Blas	t	f	2189 Union St, San Francisco, CA 94123	-122.435219	37.796997
32	Dr. Poornima Kaul	t	f	1375 Sutter St, Suite 105, San Francisco, CA 94109	-122.422866	37.787142
38	Dr. Camilo Riano	t	t	77 Van Ness Ave, Suite 303, San Francisco, CA 94102	-122.419685	37.776097
39	Dr. Jeffrey Halbrecht	t	f	2100 Webster St, Suite 33, San Francisco, CA 94115	-122.43214	37.790526
40	Dr. Evan Ransom	t	f	450 Sutter St, Suite 1212, San Francisco, CA 94108	-122.407834	37.789657
41	Dr. Jason Dudas	t	f	77 Van Ness Ave, Suite 302,San Francisco, CA 94102	-122.419685	37.776097
42	Dr. Susan Choe	t	f	490 Post St, Suite 336, San Francisco, CA 94102	-122.40983	37.78831
44	Dr. Kyle Bickel	t	f	601 Van Ness Ave, Suite 2018, San Francisco, CA 94102	-122.421406	37.781386
1	Dr. Man-Kit Leung	t	f	3838 California St, Suite 505, San Francisco, CA 94118	-122.457598	37.786186
\.


--
-- Data for Name: doctors_specialties; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.doctors_specialties (doctor_id, specialty_id) FROM stdin;
1	6
2	6
3	5
3	16
4	6
4	9
5	19
6	1
7	1
8	1
9	4
10	4
11	4
12	4
12	2
13	2
13	3
13	4
14	2
14	4
15	2
15	3
15	4
16	2
16	4
17	2
17	4
18	4
19	2
19	4
20	2
20	3
20	4
21	5
22	2
22	3
22	4
23	2
23	3
23	4
24	5
25	13
26	13
27	13
28	12
29	13
30	12
30	20
31	13
32	11
33	2
33	3
33	4
34	2
34	3
34	4
35	4
36	2
36	4
37	2
37	4
38	14
39	10
39	15
39	21
39	22
40	6
40	7
40	9
41	17
42	18
43	4
44	8
44	17
\.


--
-- Data for Name: favorites; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.favorites (favorite_id, user_id, doctor_id) FROM stdin;
65	2	24
128	2	4
135	6	4
28	2	41
149	2	36
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.reviews (review_id, user_id, doctor_id, review_content) FROM stdin;
5	2	4	Wonderful surgeon! Highly recommend!
6	2	40	Very professional! 
7	2	41	Amazing doctor! 
19	2	36	I had a great experience with Dr. Joanne! 
\.


--
-- Data for Name: specialties; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.specialties (specialty_id, specialty) FROM stdin;
1	Chiropractor
2	Cosmetic Dentist
3	Dental Pain Specialist
4	Dentist
5	Dermatologist
6	Ear, Nose & Throat
7	Facial Plastic & Reconstructive Surgeon
8	Hand Surgeon
9	Head & Neck Surgeon
10	Knee Surgeon
11	OB-GYN
12	Ophthalmologist
13	Optometrist
14	Orthodontist
15	Orthopedic Surgeon
16	Pathologist
17	Plastic Surgeon
18	Podiatrist
19	Primary Care Doctor
20	Refractive Surgeon
21	Shoulder Surgeon
22	Sports Medicine Specialist
23	Anesthesiologist 
24	Anesthesiologist 
25	Test
26	test1
27	test2
28	Chiropractor
29	Chiropractor
30	Chiropractor
31	Cosmetic Dentist
32	Chiropractor
33	test
34	Cosmetic Dentist
35	Chiropractor
36	Chiropractor
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: vagrant
--

COPY public.users (user_id, username, email, password) FROM stdin;
2	nicolas_s	n.schreier1@gmail.com	$2b$12$d2ffCYe.Ni0s7tihqYuBR.W6oRYsQ9ruT9InNWhz6jMe.ZUp5gS1.
6	lucianact	lu_terra@yahoo.com.br	$2b$12$ZmzXKDNZINRNEFcjN4p8PevjELChCzvYMAnvJgJj87Q7ogX5go3ua
\.


--
-- Name: doctors_doctor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.doctors_doctor_id_seq', 64, true);


--
-- Name: favorites_favorite_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.favorites_favorite_id_seq', 149, true);


--
-- Name: reviews_review_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.reviews_review_id_seq', 23, true);


--
-- Name: specialties_specialty_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.specialties_specialty_id_seq', 36, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: vagrant
--

SELECT pg_catalog.setval('public.users_user_id_seq', 6, true);


--
-- Name: doctors doctors_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.doctors
    ADD CONSTRAINT doctors_pkey PRIMARY KEY (doctor_id);


--
-- Name: favorites favorites_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_pkey PRIMARY KEY (favorite_id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (review_id);


--
-- Name: specialties specialties_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.specialties
    ADD CONSTRAINT specialties_pkey PRIMARY KEY (specialty_id);


--
-- Name: users uc_users; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT uc_users UNIQUE (username);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: doctors_specialties doctors_specialties_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.doctors_specialties
    ADD CONSTRAINT doctors_specialties_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(doctor_id);


--
-- Name: doctors_specialties doctors_specialties_specialty_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.doctors_specialties
    ADD CONSTRAINT doctors_specialties_specialty_id_fkey FOREIGN KEY (specialty_id) REFERENCES public.specialties(specialty_id);


--
-- Name: favorites favorites_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(doctor_id);


--
-- Name: favorites favorites_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.favorites
    ADD CONSTRAINT favorites_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: reviews reviews_doctor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_doctor_id_fkey FOREIGN KEY (doctor_id) REFERENCES public.doctors(doctor_id);


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: vagrant
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

