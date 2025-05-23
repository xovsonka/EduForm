--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2
-- Dumped by pg_dump version 16.2

-- Started on 2025-05-10 15:01:13

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
-- TOC entry 216 (class 1259 OID 112059)
-- Name: categories; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.categories OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 112058)
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.categories_id_seq OWNER TO postgres;

--
-- TOC entry 4918 (class 0 OID 0)
-- Dependencies: 215
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- TOC entry 218 (class 1259 OID 112068)
-- Name: focuses; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.focuses (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    code character varying(50) NOT NULL
);


ALTER TABLE public.focuses OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 112067)
-- Name: focuses_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.focuses_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.focuses_id_seq OWNER TO postgres;

--
-- TOC entry 4919 (class 0 OID 0)
-- Dependencies: 217
-- Name: focuses_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.focuses_id_seq OWNED BY public.focuses.id;


--
-- TOC entry 220 (class 1259 OID 112079)
-- Name: grades; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.grades (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    code character varying(50) NOT NULL
);


ALTER TABLE public.grades OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 112078)
-- Name: grades_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.grades_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.grades_id_seq OWNER TO postgres;

--
-- TOC entry 4920 (class 0 OID 0)
-- Dependencies: 219
-- Name: grades_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.grades_id_seq OWNED BY public.grades.id;


--
-- TOC entry 221 (class 1259 OID 112089)
-- Name: material_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.material_tags (
    material_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.material_tags OWNER TO postgres;

--
-- TOC entry 223 (class 1259 OID 112095)
-- Name: materials; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.materials (
    id bigint NOT NULL,
    user_id bigint,
    title text NOT NULL,
    description text,
    file_path text NOT NULL,
    category_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    file_hash text,
    focus_id integer,
    grade_id integer
);


ALTER TABLE public.materials OWNER TO postgres;

--
-- TOC entry 222 (class 1259 OID 112094)
-- Name: materials_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.materials_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.materials_id_seq OWNER TO postgres;

--
-- TOC entry 4921 (class 0 OID 0)
-- Dependencies: 222
-- Name: materials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.materials_id_seq OWNED BY public.materials.id;


--
-- TOC entry 225 (class 1259 OID 112107)
-- Name: notifications; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.notifications (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    read boolean DEFAULT false
);


ALTER TABLE public.notifications OWNER TO postgres;

--
-- TOC entry 224 (class 1259 OID 112106)
-- Name: notifications_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.notifications_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notifications_id_seq OWNER TO postgres;

--
-- TOC entry 4922 (class 0 OID 0)
-- Dependencies: 224
-- Name: notifications_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.notifications_id_seq OWNED BY public.notifications.id;


--
-- TOC entry 227 (class 1259 OID 112118)
-- Name: problem_solutions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.problem_solutions (
    id bigint NOT NULL,
    problem_id bigint,
    user_id bigint,
    file_path text NOT NULL,
    description text NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    file_hash text
);


ALTER TABLE public.problem_solutions OWNER TO postgres;

--
-- TOC entry 226 (class 1259 OID 112117)
-- Name: problem_solutions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.problem_solutions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.problem_solutions_id_seq OWNER TO postgres;

--
-- TOC entry 4923 (class 0 OID 0)
-- Dependencies: 226
-- Name: problem_solutions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.problem_solutions_id_seq OWNED BY public.problem_solutions.id;


--
-- TOC entry 228 (class 1259 OID 112127)
-- Name: problem_tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.problem_tags (
    problem_id bigint NOT NULL,
    tag_id bigint NOT NULL
);


ALTER TABLE public.problem_tags OWNER TO postgres;

--
-- TOC entry 230 (class 1259 OID 112133)
-- Name: problems; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.problems (
    id bigint NOT NULL,
    user_id bigint,
    title text NOT NULL,
    description text NOT NULL,
    category_id integer,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.problems OWNER TO postgres;

--
-- TOC entry 229 (class 1259 OID 112132)
-- Name: problems_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.problems_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.problems_id_seq OWNER TO postgres;

--
-- TOC entry 4924 (class 0 OID 0)
-- Dependencies: 229
-- Name: problems_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.problems_id_seq OWNED BY public.problems.id;


--
-- TOC entry 232 (class 1259 OID 112143)
-- Name: tags; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.tags (
    id bigint NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.tags OWNER TO postgres;

--
-- TOC entry 231 (class 1259 OID 112142)
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.tags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO postgres;

--
-- TOC entry 4925 (class 0 OID 0)
-- Dependencies: 231
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- TOC entry 234 (class 1259 OID 112152)
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    username character varying(50) NOT NULL,
    email character varying(100) NOT NULL,
    password_hash character varying(255) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- TOC entry 233 (class 1259 OID 112151)
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO postgres;

--
-- TOC entry 4926 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- TOC entry 4682 (class 2604 OID 112062)
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- TOC entry 4683 (class 2604 OID 112071)
-- Name: focuses id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focuses ALTER COLUMN id SET DEFAULT nextval('public.focuses_id_seq'::regclass);


--
-- TOC entry 4684 (class 2604 OID 112082)
-- Name: grades id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades ALTER COLUMN id SET DEFAULT nextval('public.grades_id_seq'::regclass);


--
-- TOC entry 4685 (class 2604 OID 112098)
-- Name: materials id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials ALTER COLUMN id SET DEFAULT nextval('public.materials_id_seq'::regclass);


--
-- TOC entry 4687 (class 2604 OID 112110)
-- Name: notifications id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications ALTER COLUMN id SET DEFAULT nextval('public.notifications_id_seq'::regclass);


--
-- TOC entry 4690 (class 2604 OID 112121)
-- Name: problem_solutions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_solutions ALTER COLUMN id SET DEFAULT nextval('public.problem_solutions_id_seq'::regclass);


--
-- TOC entry 4692 (class 2604 OID 112136)
-- Name: problems id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems ALTER COLUMN id SET DEFAULT nextval('public.problems_id_seq'::regclass);


--
-- TOC entry 4694 (class 2604 OID 112146)
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- TOC entry 4695 (class 2604 OID 112155)
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- TOC entry 4894 (class 0 OID 112059)
-- Dependencies: 216
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.categories (id, name) FROM stdin;
1	ZŠ
2	SŠ
3	VŠ
\.


--
-- TOC entry 4896 (class 0 OID 112068)
-- Dependencies: 218
-- Data for Name: focuses; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.focuses (id, name, code) FROM stdin;
1	Matematika	MATH
2	Slovenský jazyk	SLOVAK
3	Fyzika	PHYSICS
4	Chémia	CHEMISTRY
5	Biológia	BIOLOGY
6	Anglický jazyk	ENGLISH
7	Dejepis	HISTORY
8	Geografia	GEOGRAPHY
\.


--
-- TOC entry 4898 (class 0 OID 112079)
-- Dependencies: 220
-- Data for Name: grades; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.grades (id, name, code) FROM stdin;
1	1. ročník	GRADE_1
2	2. ročník	GRADE_2
3	3. ročník	GRADE_3
4	4. ročník	GRADE_4
5	5. ročník	GRADE_5
6	6. ročník	GRADE_6
7	7. ročník	GRADE_7
8	8. ročník	GRADE_8
9	9. ročník	GRADE_9
10	1. ročník SŠ	GRADE_S1
11	2. ročník SŠ	GRADE_S2
12	3. ročník SŠ	GRADE_S3
13	4. ročník SŠ	GRADE_S4
\.


--
-- TOC entry 4899 (class 0 OID 112089)
-- Dependencies: 221
-- Data for Name: material_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.material_tags (material_id, tag_id) FROM stdin;
\.


--
-- TOC entry 4901 (class 0 OID 112095)
-- Dependencies: 223
-- Data for Name: materials; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.materials (id, user_id, title, description, file_path, category_id, created_at, file_hash, focus_id, grade_id) FROM stdin;
1	1	Časy v anglickom jazyku pre 3. ročník	Jednoduché poznámky pre študenta 3 ročníka, zamerané na časy v anglickom jazyku.	uploads/materials/Casy_v_anglickom_jazyku_pre_3._rocnik.pdf	1	2025-05-10 14:27:08.459151	a70b9b0b2af568389ae4e72865ede0de211bd349dedaf17329c76fac6b7d19e5	6	3
2	1	Bezpečné správanie na internete	Prezentácia, ktorá žiakom vysvetľuje zásady bezpečného používania internetu a sociálnych sietí.	uploads/materials/Bezpecne_spravanie_na_internete.pptx	1	2025-05-10 14:29:18.988279	d2ca28186d7f32e989e5e8f2a817bfbaf05fdf4823e783825614a63a61793ce9	\N	\N
3	1	Otázky na tému cloudove uložisko	Jednoduchý kvíz pre študentov na preopakovanie fungovania cloudového uložiska.	uploads/materials/Otazky_na_temu_cloudove_ulozisko.pdf	2	2025-05-10 14:30:57.89153	6673b43cc8372d3f41b23c2c0f2b81d66fc9a2c04c4668bc7ce12d5d6b7f1671	\N	\N
4	1	Kyberšikana – ako ju rozpoznať a brániť sa	Prezentácia ktorá slúži na upovedomenie o probléme akým je šikana	uploads/materials/Kybersikana_ako_ju_rozpoznat_a_branit_sa.pptx	1	2025-05-10 14:32:19.672395	7ec66f35bec0189d22d5014f4c0b5d13e2e853d2f779a9a45b72892609e33e31	\N	\N
5	1	Ako si vytvoriť prezentáciu v PowerPointe alebo Google Slides	Jednoduchá prezentácia pre žiakov 2.ročníka, pre úvod do informatiky	uploads/materials/Ako_si_vytvorit_prezentaciu_v_PowerPointe_alebo_Google_Slides.pdf	1	2025-05-10 14:33:43.686943	0e60aeccdc1542d83e1eb11414874123d4c34dc95b42561fa015133406c2bbe9	\N	1
6	1	Test zlomky	Krátka 5-minútovka na tému zlomky.	uploads/materials/Test_zlomky.pdf	1	2025-05-10 14:35:30.963893	c68f2fd4e6244d1e7c7c865171450bc49bca9198cee6341f5ee898c59b350fc3	1	6
7	1	Úvod do štatistiky	Poznámky je úvod do štatistiky	uploads/materials/Uvod_do_statistiky.pdf	2	2025-05-10 14:36:24.993226	12722895222af14e9d7e18ed868022645bdb76abac7caf846b4b298cb5e76139	1	11
8	1	Stavba atómu	Poznámky k téme stavba atómu	uploads/materials/Stavba_atomu.pdf	2	2025-05-10 14:39:32.565985	83932873122415a6fa6c69f838a896426e5504ca9fad560d0e4860c8101959bd	4	12
9	1	Periodická tabuľka-test	Krátky test k periodickej tabuľke, 5 otázok ABCD, 2 otvorené	uploads/materials/Periodicka_tabulka-test.pdf	2	2025-05-10 14:40:55.146737	62067256428fcf024823dd9e37429f1ff2a962afa3d4ec287eb731d56d971f71	4	10
10	1	Zásady bezpečnosti v chemickom laboratóriu	Poznámky pre študentov z úvodnej hodiny v chemickom laboratóriu	uploads/materials/Zasady_bezpecnosti_v_chemickom_laboratoriu.pdf	2	2025-05-10 14:41:56.066856	c5004c08a97c77bdd1c4426e1c6e9613ac1763ccd08b010b53f238108dabdd2d	4	10
\.


--
-- TOC entry 4903 (class 0 OID 112107)
-- Dependencies: 225
-- Data for Name: notifications; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.notifications (id, user_id, message, created_at, read) FROM stdin;
\.


--
-- TOC entry 4905 (class 0 OID 112118)
-- Dependencies: 227
-- Data for Name: problem_solutions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.problem_solutions (id, problem_id, user_id, file_path, description, created_at, file_hash) FROM stdin;
1	2	1	uploads/problems/skolenie_ucitelov.pdf	Na našej škole sme mali podobný problém s tým, že mnohí učitelia nevedeli\r\npoužívať MS Teams a Edupage. Zorganizovali sme si jednoduché interné školenie	2025-05-10 14:21:26.416927	83a813389428ae1fcea3272dc61b57336f58e74eac63a651b52d10e426e7b6d4
2	6	1	uploads/problems/lokalizacia_materialov.pdf	Naša škola chcela používať Khan Academy na ZŠ, ale žiaci nerozumeli\r\nangličtine. Tak sme si poradili po svojom.	2025-05-10 14:22:42.181795	f235feb18bb04f4899170f9770ebf02ce13268457595674cdc17168cc5c8b6c9
3	8	1	uploads/problems/data_privacy_school.pdf	Ako IT správca som videl, že mnohí učitelia posielajú známky a citlivé\r\ninformácie cez nešifrované e-maily. Preto sme pripravili jednoduché školské pravidlá\r\npre ochranu osobných údajov.	2025-05-10 14:25:26.592837	c71e31967134e211f304a003d29740399375572b5f07d2336492630d900bf17c
\.


--
-- TOC entry 4906 (class 0 OID 112127)
-- Dependencies: 228
-- Data for Name: problem_tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.problem_tags (problem_id, tag_id) FROM stdin;
1	1
1	2
1	3
1	4
1	5
1	6
1	7
1	8
1	9
1	10
2	11
2	12
2	13
2	14
2	15
2	16
2	17
2	18
2	19
2	20
3	21
3	22
3	23
3	24
3	25
3	26
3	27
3	28
3	29
3	30
4	31
4	32
4	33
4	34
4	1
4	35
4	21
4	13
4	36
4	37
5	2
5	38
5	39
5	40
5	41
5	42
5	43
5	44
5	45
5	46
6	47
6	48
6	49
6	50
6	8
6	51
6	52
6	53
6	54
6	55
7	21
7	56
7	57
7	58
7	59
7	60
7	61
7	62
7	63
7	8
8	2
8	64
8	26
8	65
8	66
8	67
8	68
8	69
8	46
8	38
9	70
9	21
9	37
9	42
9	71
9	72
9	73
9	74
9	75
9	76
10	77
10	78
10	68
10	4
10	79
10	70
10	37
10	80
10	81
10	82
\.


--
-- TOC entry 4908 (class 0 OID 112133)
-- Dependencies: 230
-- Data for Name: problems; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.problems (id, user_id, title, description, category_id, created_at) FROM stdin;
1	1	Nemáme v škole dostatočné digitálne vybavenie	V našej škole máme len 2 projektory na celú budovu a chýbajú nám notebooky či tablety pre žiakov. Moderné vyučovanie sa bez toho robí veľmi ťažko.	1	2025-05-10 14:11:29.693221
2	1	Mnohí kolegovia nevedia pracovať s digitálnymi nástrojmi	Učím informatiku a vidím, že viacerí učitelia sa boja používať MS Teams, Forms či Edupage nad rámec základov. Chýba im školenie alebo podpora.	2	2025-05-10 14:11:55.888976
3	1	Žiaci používajú 5 rôznych systémov a strácajú sa v tom	Každý učiteľ používa inú platformu – Google Classroom, Moodle, Edmodo, MS Teams. Žiaci často nevedia, kam majú ísť a čo im kde chýba.	2	2025-05-10 14:12:19.399866
4	1	Slabé Wi-Fi pripojenie v triedach	Internet v škole vypadáva, žiaci sa nevedia pripojiť na online cvičenia, učiteľský notebook vypadne počas prezentácie.	1	2025-05-10 14:12:41.523442
5	1	Nemáme jasné pravidlá používania technológií na hodinách	Niektorí učitelia mobil úplne zakazujú, iní ich nechávajú používať na vyučovanie. Chýba nám jednotná školská digitálna politika.	2	2025-05-10 14:13:01.388717
6	1	Väčšina moderných digitálnych materiálov je len v angličtine	Napríklad Khan Academy má skvelý obsah, ale žiaci (hlavne na ZŠ) nevedia dostatočne po anglicky. Preklad a lokalizácia sú slabé.	1	2025-05-10 14:13:21.982046
7	1	Nie všetci žiaci majú doma rovnaké technické možnosti	V niektorých rodinách je len jeden počítač, slabý internet alebo vôbec nič. Títo žiaci sú znevýhodnení najmä pri domácom vzdelávaní.	1	2025-05-10 14:13:42.575145
8	1	Nemáme prehľad o tom, ako bezpečne uchovávať údaje žiakov	Nie je nám úplne jasné, čo smieme ukladať do Google Disku alebo ako ochrániť dáta pred zneužitím. Chýba školenie o GDPR.	3	2025-05-10 14:13:58.793328
9	1	Žiaci pri online hodinách chýbajú alebo sú pasívni	Počas dištančného vzdelávania mnohí študenti len "sedia" pri zapnutom počítači, ale neinteragujú. Potrebujeme lepšie digitálne nástroje na zapojenie.	2	2025-05-10 14:14:13.216989
10	1	Nevieme hodnotiť žiakov digitálne spravodlivo	Pri online testovaní často nevieme zaručiť, že žiak nepodvádza. Chýbajú nám nástroje alebo pravidlá, ako hodnotiť férovo	3	2025-05-10 14:14:26.59203
\.


--
-- TOC entry 4910 (class 0 OID 112143)
-- Dependencies: 232
-- Data for Name: tags; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.tags (id, name) FROM stdin;
1	škole
2	nemáme
3	dostatočné
4	digitálne
5	vybavenie
6	našej
7	máme
8	len
9	projektory
10	celú
11	mnohí
12	kolegovia
13	nevedia
14	pracovať
15	digitálnymi
16	nástrojmi
17	učím
18	informatiku
19	vidím
20	viacerí
21	žiaci
22	používajú
23	rôznych
24	systémov
25	strácajú
26	tom
27	každý
28	učiteľ
29	používa
30	inú
31	slabé
32	pripojenie
33	triedach
34	internet
35	vypadáva
36	pripojiť
37	online
38	jasné
39	pravidlá
40	používania
41	technológií
42	hodinách
43	niektorí
44	učitelia
45	mobil
46	úplne
47	väčšina
48	moderných
49	digitálnych
50	materiálov
51	angličtine
52	napríklad
53	khan
54	academy
55	skvelý
56	všetci
57	majú
58	doma
59	rovnaké
60	technické
61	možnosti
62	niektorých
63	rodinách
64	prehľad
65	bezpečne
66	uchovávať
67	údaje
68	žiakov
69	nám
70	pri
71	chýbajú
72	alebo
73	pasívni
74	počas
75	dištančného
76	vzdelávania
77	nevieme
78	hodnotiť
79	spravodlivo
80	testovaní
81	často
82	zaručiť
\.


--
-- TOC entry 4912 (class 0 OID 112152)
-- Dependencies: 234
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, username, email, password_hash, created_at) FROM stdin;
1	xovsonka	aovsonka@gmail.com	scrypt:32768:8:1$O3vYPFpRGZp1AHls$aa4ad43196ae3dc5446f8195ad68d624b4ce9b1aed72ef8370a7b13c0a9f5861fc35bc7be1bb53ac78abd5ff0a359dc865e173d566a5334de2836ab4d4f88799	2025-05-10 14:07:00.973056
\.


--
-- TOC entry 4927 (class 0 OID 0)
-- Dependencies: 215
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.categories_id_seq', 3, true);


--
-- TOC entry 4928 (class 0 OID 0)
-- Dependencies: 217
-- Name: focuses_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.focuses_id_seq', 8, true);


--
-- TOC entry 4929 (class 0 OID 0)
-- Dependencies: 219
-- Name: grades_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.grades_id_seq', 13, true);


--
-- TOC entry 4930 (class 0 OID 0)
-- Dependencies: 222
-- Name: materials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.materials_id_seq', 10, true);


--
-- TOC entry 4931 (class 0 OID 0)
-- Dependencies: 224
-- Name: notifications_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.notifications_id_seq', 1, false);


--
-- TOC entry 4932 (class 0 OID 0)
-- Dependencies: 226
-- Name: problem_solutions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.problem_solutions_id_seq', 3, true);


--
-- TOC entry 4933 (class 0 OID 0)
-- Dependencies: 229
-- Name: problems_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.problems_id_seq', 10, true);


--
-- TOC entry 4934 (class 0 OID 0)
-- Dependencies: 231
-- Name: tags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.tags_id_seq', 82, true);


--
-- TOC entry 4935 (class 0 OID 0)
-- Dependencies: 233
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, true);


--
-- TOC entry 4698 (class 2606 OID 112066)
-- Name: categories categories_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_name_key UNIQUE (name);


--
-- TOC entry 4700 (class 2606 OID 112064)
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- TOC entry 4702 (class 2606 OID 112075)
-- Name: focuses focuses_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focuses
    ADD CONSTRAINT focuses_code_key UNIQUE (code);


--
-- TOC entry 4704 (class 2606 OID 112077)
-- Name: focuses focuses_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focuses
    ADD CONSTRAINT focuses_name_key UNIQUE (name);


--
-- TOC entry 4706 (class 2606 OID 112073)
-- Name: focuses focuses_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.focuses
    ADD CONSTRAINT focuses_pkey PRIMARY KEY (id);


--
-- TOC entry 4708 (class 2606 OID 112086)
-- Name: grades grades_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_code_key UNIQUE (code);


--
-- TOC entry 4710 (class 2606 OID 112088)
-- Name: grades grades_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_name_key UNIQUE (name);


--
-- TOC entry 4712 (class 2606 OID 112084)
-- Name: grades grades_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.grades
    ADD CONSTRAINT grades_pkey PRIMARY KEY (id);


--
-- TOC entry 4714 (class 2606 OID 112093)
-- Name: material_tags material_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_tags
    ADD CONSTRAINT material_tags_pkey PRIMARY KEY (material_id, tag_id);


--
-- TOC entry 4716 (class 2606 OID 112105)
-- Name: materials materials_file_hash_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_file_hash_key UNIQUE (file_hash);


--
-- TOC entry 4718 (class 2606 OID 112103)
-- Name: materials materials_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_pkey PRIMARY KEY (id);


--
-- TOC entry 4720 (class 2606 OID 112116)
-- Name: notifications notifications_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_pkey PRIMARY KEY (id);


--
-- TOC entry 4722 (class 2606 OID 112126)
-- Name: problem_solutions problem_solutions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_solutions
    ADD CONSTRAINT problem_solutions_pkey PRIMARY KEY (id);


--
-- TOC entry 4724 (class 2606 OID 112131)
-- Name: problem_tags problem_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_pkey PRIMARY KEY (problem_id, tag_id);


--
-- TOC entry 4726 (class 2606 OID 112141)
-- Name: problems problems_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_pkey PRIMARY KEY (id);


--
-- TOC entry 4728 (class 2606 OID 112150)
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- TOC entry 4730 (class 2606 OID 112148)
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- TOC entry 4732 (class 2606 OID 112160)
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- TOC entry 4734 (class 2606 OID 112158)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- TOC entry 4736 (class 2606 OID 112162)
-- Name: users users_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_username_key UNIQUE (username);


--
-- TOC entry 4737 (class 2606 OID 112163)
-- Name: material_tags material_tags_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_tags
    ADD CONSTRAINT material_tags_material_id_fkey FOREIGN KEY (material_id) REFERENCES public.materials(id) ON DELETE CASCADE;


--
-- TOC entry 4738 (class 2606 OID 112168)
-- Name: material_tags material_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.material_tags
    ADD CONSTRAINT material_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- TOC entry 4739 (class 2606 OID 112173)
-- Name: materials materials_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- TOC entry 4740 (class 2606 OID 112178)
-- Name: materials materials_focus_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_focus_id_fkey FOREIGN KEY (focus_id) REFERENCES public.focuses(id) ON DELETE SET NULL;


--
-- TOC entry 4741 (class 2606 OID 112183)
-- Name: materials materials_grade_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_grade_id_fkey FOREIGN KEY (grade_id) REFERENCES public.grades(id) ON DELETE SET NULL;


--
-- TOC entry 4742 (class 2606 OID 112188)
-- Name: materials materials_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.materials
    ADD CONSTRAINT materials_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 4743 (class 2606 OID 112193)
-- Name: notifications notifications_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.notifications
    ADD CONSTRAINT notifications_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- TOC entry 4744 (class 2606 OID 112198)
-- Name: problem_solutions problem_solutions_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_solutions
    ADD CONSTRAINT problem_solutions_problem_id_fkey FOREIGN KEY (problem_id) REFERENCES public.problems(id) ON DELETE CASCADE;


--
-- TOC entry 4745 (class 2606 OID 112203)
-- Name: problem_solutions problem_solutions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_solutions
    ADD CONSTRAINT problem_solutions_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


--
-- TOC entry 4746 (class 2606 OID 112208)
-- Name: problem_tags problem_tags_problem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_problem_id_fkey FOREIGN KEY (problem_id) REFERENCES public.problems(id) ON DELETE CASCADE;


--
-- TOC entry 4747 (class 2606 OID 112213)
-- Name: problem_tags problem_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problem_tags
    ADD CONSTRAINT problem_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- TOC entry 4748 (class 2606 OID 112218)
-- Name: problems problems_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id) ON DELETE SET NULL;


--
-- TOC entry 4749 (class 2606 OID 112223)
-- Name: problems problems_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.problems
    ADD CONSTRAINT problems_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id) ON DELETE SET NULL;


-- Completed on 2025-05-10 15:01:14

--
-- PostgreSQL database dump complete
--

