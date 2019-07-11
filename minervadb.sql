--
-- PostgreSQL database dump
--

-- Dumped from database version 10.9 (Ubuntu 10.9-1.pgdg18.04+1)
-- Dumped by pg_dump version 10.9 (Ubuntu 10.9-1.pgdg18.04+1)

-- Started on 2019-07-11 15:08:55 BST

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
-- TOC entry 2958 (class 1262 OID 1230233464)
-- Name: minervacustomer; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE minervacustomer WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_GB.UTF-8' LC_CTYPE = 'en_GB.UTF-8';


\connect minervacustomer

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
-- TOC entry 1 (class 3079 OID 13039)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2960 (class 0 OID 0)
-- Dependencies: 1
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 196 (class 1259 OID 1230233465)
-- Name: company; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.company (
    companyid bigint NOT NULL,
    companyname character varying(200) NOT NULL,
    cik character(10) NOT NULL
);


--
-- TOC entry 199 (class 1259 OID 1230233483)
-- Name: event; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.event (
    eventid bigint NOT NULL,
    companyid bigint NOT NULL,
    eventtypeid integer NOT NULL,
    eventdate timestamp without time zone NOT NULL,
    address character varying(1000) NOT NULL,
    instructions text,
    edgartext text
);


--
-- TOC entry 198 (class 1259 OID 1230233478)
-- Name: eventtype; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.eventtype (
    eventtypeid bigint NOT NULL,
    description character varying(20) NOT NULL
);


--
-- TOC entry 197 (class 1259 OID 1230233470)
-- Name: processlog; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.processlog (
    processlogid bigint NOT NULL,
    processedat timestamp without time zone NOT NULL,
    edgarurl character varying(1000) NOT NULL,
    eventid bigint
);


--
-- TOC entry 200 (class 1259 OID 1230233501)
-- Name: resolution; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.resolution (
    resolutionid bigint NOT NULL,
    eventid bigint NOT NULL,
    title character varying(10) NOT NULL,
    narrative text NOT NULL
);


--
-- TOC entry 2948 (class 0 OID 1230233465)
-- Dependencies: 196
-- Data for Name: company; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.company (companyid, companyname, cik) FROM stdin;
\.


--
-- TOC entry 2951 (class 0 OID 1230233483)
-- Dependencies: 199
-- Data for Name: event; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.event (eventid, companyid, eventtypeid, eventdate, address, instructions, edgartext) FROM stdin;
\.


--
-- TOC entry 2950 (class 0 OID 1230233478)
-- Dependencies: 198
-- Data for Name: eventtype; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.eventtype (eventtypeid, description) FROM stdin;
\.


--
-- TOC entry 2949 (class 0 OID 1230233470)
-- Dependencies: 197
-- Data for Name: processlog; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.processlog (processlogid, processedat, edgarurl, eventid) FROM stdin;
\.


--
-- TOC entry 2952 (class 0 OID 1230233501)
-- Dependencies: 200
-- Data for Name: resolution; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.resolution (resolutionid, eventid, title, narrative) FROM stdin;
\.


--
-- TOC entry 2804 (class 2606 OID 1230233469)
-- Name: company company_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.company
    ADD CONSTRAINT company_pk PRIMARY KEY (companyid);


--
-- TOC entry 2815 (class 2606 OID 1230233490)
-- Name: event event_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_pk PRIMARY KEY (eventid);


--
-- TOC entry 2817 (class 2606 OID 1230233517)
-- Name: event event_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_uq UNIQUE (companyid, eventtypeid, eventdate);


--
-- TOC entry 2808 (class 2606 OID 1230233482)
-- Name: eventtype eventtype_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eventtype
    ADD CONSTRAINT eventtype_pk PRIMARY KEY (eventtypeid);


--
-- TOC entry 2810 (class 2606 OID 1230233521)
-- Name: eventtype eventtype_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.eventtype
    ADD CONSTRAINT eventtype_uq UNIQUE (description);


--
-- TOC entry 2806 (class 2606 OID 1230233477)
-- Name: processlog processlog_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.processlog
    ADD CONSTRAINT processlog_pk PRIMARY KEY (processlogid);


--
-- TOC entry 2821 (class 2606 OID 1230233508)
-- Name: resolution resolution_pk; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolution
    ADD CONSTRAINT resolution_pk PRIMARY KEY (resolutionid);


--
-- TOC entry 2823 (class 2606 OID 1230233510)
-- Name: resolution resolution_uq; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolution
    ADD CONSTRAINT resolution_uq UNIQUE (eventid, title);


--
-- TOC entry 2801 (class 1259 OID 1230233525)
-- Name: company_ix1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX company_ix1 ON public.company USING btree (companyid);


--
-- TOC entry 2802 (class 1259 OID 1230233526)
-- Name: company_ix2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX company_ix2 ON public.company USING btree (cik);


--
-- TOC entry 2811 (class 1259 OID 1230233522)
-- Name: event_ix1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_ix1 ON public.event USING btree (eventid);


--
-- TOC entry 2812 (class 1259 OID 1230233523)
-- Name: event_ix2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_ix2 ON public.event USING btree (companyid);


--
-- TOC entry 2813 (class 1259 OID 1230233524)
-- Name: event_ix3; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX event_ix3 ON public.event USING btree (eventdate);


--
-- TOC entry 2818 (class 1259 OID 1230233518)
-- Name: resolution_ix1; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX resolution_ix1 ON public.resolution USING btree (resolutionid);


--
-- TOC entry 2819 (class 1259 OID 1230233519)
-- Name: resolution_ix2; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX resolution_ix2 ON public.resolution USING btree (eventid);


--
-- TOC entry 2824 (class 2606 OID 1230233491)
-- Name: event event_companyid_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_companyid_fk FOREIGN KEY (companyid) REFERENCES public.company(companyid);


--
-- TOC entry 2825 (class 2606 OID 1230233496)
-- Name: event event_eventtypeid_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.event
    ADD CONSTRAINT event_eventtypeid_fk FOREIGN KEY (eventtypeid) REFERENCES public.eventtype(eventtypeid);


--
-- TOC entry 2826 (class 2606 OID 1230233511)
-- Name: resolution resolution_eventid_fk; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.resolution
    ADD CONSTRAINT resolution_eventid_fk FOREIGN KEY (resolutionid) REFERENCES public.event(eventid);


-- Completed on 2019-07-11 15:08:55 BST

--
-- PostgreSQL database dump complete
--

