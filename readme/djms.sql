--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE alembic_version OWNER TO dbuser;

--
-- Name: category; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE category (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    name character varying(32),
    description character varying(256)
);


ALTER TABLE category OWNER TO dbuser;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE category_id_seq OWNER TO dbuser;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: in_stock; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE in_stock (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    product_id integer,
    serial_no character varying(32),
    date_instock date
);


ALTER TABLE in_stock OWNER TO dbuser;

--
-- Name: in_stock_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE in_stock_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE in_stock_id_seq OWNER TO dbuser;

--
-- Name: in_stock_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE in_stock_id_seq OWNED BY in_stock.id;


--
-- Name: material; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE material (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    name character varying(32),
    description character varying(256)
);


ALTER TABLE material OWNER TO dbuser;

--
-- Name: material_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE material_id_seq OWNER TO dbuser;

--
-- Name: material_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE material_id_seq OWNED BY material.id;


--
-- Name: material_inventory; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE material_inventory (
    material_id integer NOT NULL,
    amount numeric(9,2) NOT NULL,
    amount_out numeric(9,2) NOT NULL,
    _version_id integer NOT NULL
);


ALTER TABLE material_inventory OWNER TO dbuser;

--
-- Name: material_order; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE material_order (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    sp_id integer,
    material_id integer,
    unit character varying(32),
    amount_buy numeric(8,2),
    unit_price numeric(8,2),
    amount_price numeric(8,2),
    date_buy date NOT NULL,
    memo character varying(512)
);


ALTER TABLE material_order OWNER TO dbuser;

--
-- Name: material_order_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE material_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE material_order_id_seq OWNER TO dbuser;

--
-- Name: material_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE material_order_id_seq OWNED BY material_order.id;


--
-- Name: out_stock_item; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE out_stock_item (
    serial_no character varying(32) NOT NULL,
    date_outstock date NOT NULL,
    product_order_item_id integer NOT NULL
);


ALTER TABLE out_stock_item OWNER TO dbuser;

--
-- Name: product; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE product (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    name character varying(64),
    drawing character varying(256) NOT NULL,
    attachment character varying(256) NOT NULL,
    man_hours numeric(8,1) NOT NULL,
    serial_number character varying(32) NOT NULL,
    price numeric(10,2),
    reed smallint,
    memo character varying(512),
    category_id integer
);


ALTER TABLE product OWNER TO dbuser;

--
-- Name: product_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE product_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_id_seq OWNER TO dbuser;

--
-- Name: product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE product_id_seq OWNED BY product.id;


--
-- Name: product_material; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE product_material (
    product_id integer NOT NULL,
    material_id integer NOT NULL
);


ALTER TABLE product_material OWNER TO dbuser;

--
-- Name: product_order; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE product_order (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    order_no character varying(32),
    source character varying(8),
    date_submitted date NOT NULL,
    memo character varying(512),
    _version_id integer NOT NULL,
    status smallint NOT NULL
);


ALTER TABLE product_order OWNER TO dbuser;

--
-- Name: product_order_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE product_order_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_order_id_seq OWNER TO dbuser;

--
-- Name: product_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE product_order_id_seq OWNED BY product_order.id;


--
-- Name: product_order_item; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE product_order_item (
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    product_order_id integer,
    product_id integer NOT NULL,
    quantity integer,
    unit_price numeric(8,2),
    amount numeric(8,2),
    date_delivered date NOT NULL,
    memo character varying(512)
);


ALTER TABLE product_order_item OWNER TO dbuser;

--
-- Name: product_order_item_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE product_order_item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_order_item_id_seq OWNER TO dbuser;

--
-- Name: product_order_item_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE product_order_item_id_seq OWNED BY product_order_item.id;


--
-- Name: product_sequence; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE product_sequence (
    id integer NOT NULL,
    seq integer,
    _version_id integer NOT NULL
);


ALTER TABLE product_sequence OWNER TO dbuser;

--
-- Name: service_provider; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE service_provider (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    name character varying(128) NOT NULL,
    contact_name character varying(64) NOT NULL,
    contact_address character varying(128) NOT NULL,
    contact_tel character varying(128) NOT NULL,
    shop_address character varying(256) NOT NULL,
    memo character varying(512)
);


ALTER TABLE service_provider OWNER TO dbuser;

--
-- Name: service_provider_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE service_provider_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE service_provider_id_seq OWNER TO dbuser;

--
-- Name: service_provider_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE service_provider_id_seq OWNED BY service_provider.id;


--
-- Name: sp_material; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE sp_material (
    sp_id integer NOT NULL,
    material_id integer NOT NULL
);


ALTER TABLE sp_material OWNER TO dbuser;

--
-- Name: task; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE task (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    textile_worker_id integer,
    product_id integer,
    date_started date NOT NULL,
    quantity_expected integer NOT NULL,
    date_expected date NOT NULL,
    memo character varying(512),
    finished boolean,
    _version_id integer NOT NULL
);


ALTER TABLE task OWNER TO dbuser;

--
-- Name: task_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE task_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE task_id_seq OWNER TO dbuser;

--
-- Name: task_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE task_id_seq OWNED BY task.id;


--
-- Name: task_material; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE task_material (
    id integer NOT NULL,
    amount numeric(8,2),
    unit character varying(32),
    task_id integer,
    material_id integer
);


ALTER TABLE task_material OWNER TO dbuser;

--
-- Name: task_material_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE task_material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE task_material_id_seq OWNER TO dbuser;

--
-- Name: task_material_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE task_material_id_seq OWNED BY task_material.id;


--
-- Name: task_result; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE task_result (
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    task_id integer,
    date_finished date NOT NULL,
    quantity_qualified integer,
    quantity_defective integer,
    level character varying(8),
    _version_id integer NOT NULL
);


ALTER TABLE task_result OWNER TO dbuser;

--
-- Name: task_result_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE task_result_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE task_result_id_seq OWNER TO dbuser;

--
-- Name: task_result_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE task_result_id_seq OWNED BY task_result.id;


--
-- Name: textile_worker; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE textile_worker (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    fullname character varying(32),
    tel character varying(20),
    idcard character varying(20) NOT NULL,
    address character varying(128) NOT NULL,
    manager_id integer,
    is_manager boolean NOT NULL,
    memo character varying(512)
);


ALTER TABLE textile_worker OWNER TO dbuser;

--
-- Name: textile_worker_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE textile_worker_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE textile_worker_id_seq OWNER TO dbuser;

--
-- Name: textile_worker_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE textile_worker_id_seq OWNED BY textile_worker.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: dbuser; Tablespace: 
--

CREATE TABLE "user" (
    deleted boolean NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    id integer NOT NULL,
    email character varying(128) NOT NULL,
    fullname character varying(32),
    tel character varying(20),
    password character varying(128),
    active boolean,
    role character varying(16)
);


ALTER TABLE "user" OWNER TO dbuser;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: dbuser
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO dbuser;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: dbuser
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY in_stock ALTER COLUMN id SET DEFAULT nextval('in_stock_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY material ALTER COLUMN id SET DEFAULT nextval('material_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY material_order ALTER COLUMN id SET DEFAULT nextval('material_order_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product ALTER COLUMN id SET DEFAULT nextval('product_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_order ALTER COLUMN id SET DEFAULT nextval('product_order_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_order_item ALTER COLUMN id SET DEFAULT nextval('product_order_item_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY service_provider ALTER COLUMN id SET DEFAULT nextval('service_provider_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task ALTER COLUMN id SET DEFAULT nextval('task_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task_material ALTER COLUMN id SET DEFAULT nextval('task_material_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task_result ALTER COLUMN id SET DEFAULT nextval('task_result_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY textile_worker ALTER COLUMN id SET DEFAULT nextval('textile_worker_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: category_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_name_key UNIQUE (name);


--
-- Name: category_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: in_stock_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY in_stock
    ADD CONSTRAINT in_stock_pkey PRIMARY KEY (id);


--
-- Name: in_stock_serial_no_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY in_stock
    ADD CONSTRAINT in_stock_serial_no_key UNIQUE (serial_no);


--
-- Name: material_inventory_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY material_inventory
    ADD CONSTRAINT material_inventory_pkey PRIMARY KEY (material_id);


--
-- Name: material_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY material
    ADD CONSTRAINT material_name_key UNIQUE (name);


--
-- Name: material_order_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY material_order
    ADD CONSTRAINT material_order_pkey PRIMARY KEY (id);


--
-- Name: material_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY material
    ADD CONSTRAINT material_pkey PRIMARY KEY (id);


--
-- Name: out_stock_item_serial_no_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY out_stock_item
    ADD CONSTRAINT out_stock_item_serial_no_key UNIQUE (serial_no);


--
-- Name: product_material_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_material
    ADD CONSTRAINT product_material_pkey PRIMARY KEY (product_id, material_id);


--
-- Name: product_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_name_key UNIQUE (name);


--
-- Name: product_order_item_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_order_item
    ADD CONSTRAINT product_order_item_pkey PRIMARY KEY (id);


--
-- Name: product_order_item_uk; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_order_item
    ADD CONSTRAINT product_order_item_uk UNIQUE (product_order_id, product_id);


--
-- Name: product_order_order_no_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_order
    ADD CONSTRAINT product_order_order_no_key UNIQUE (order_no);


--
-- Name: product_order_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_order
    ADD CONSTRAINT product_order_pkey PRIMARY KEY (id);


--
-- Name: product_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_pkey PRIMARY KEY (id);


--
-- Name: product_sequence_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product_sequence
    ADD CONSTRAINT product_sequence_pkey PRIMARY KEY (id);


--
-- Name: product_serial_number_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_serial_number_key UNIQUE (serial_number);


--
-- Name: service_provider_name_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY service_provider
    ADD CONSTRAINT service_provider_name_key UNIQUE (name);


--
-- Name: service_provider_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY service_provider
    ADD CONSTRAINT service_provider_pkey PRIMARY KEY (id);


--
-- Name: sp_material_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY sp_material
    ADD CONSTRAINT sp_material_pkey PRIMARY KEY (sp_id, material_id);


--
-- Name: task_material_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY task_material
    ADD CONSTRAINT task_material_pkey PRIMARY KEY (id);


--
-- Name: task_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY task
    ADD CONSTRAINT task_pkey PRIMARY KEY (id);


--
-- Name: task_result_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY task_result
    ADD CONSTRAINT task_result_pkey PRIMARY KEY (id);


--
-- Name: textile_worker_idcard_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY textile_worker
    ADD CONSTRAINT textile_worker_idcard_key UNIQUE (idcard);


--
-- Name: textile_worker_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY textile_worker
    ADD CONSTRAINT textile_worker_pkey PRIMARY KEY (id);


--
-- Name: user_email_key; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: public; Owner: dbuser; Tablespace: 
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: in_stock_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY in_stock
    ADD CONSTRAINT in_stock_product_id_fkey FOREIGN KEY (product_id) REFERENCES product(id);


--
-- Name: material_inventory_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY material_inventory
    ADD CONSTRAINT material_inventory_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id);


--
-- Name: material_order_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY material_order
    ADD CONSTRAINT material_order_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id);


--
-- Name: material_order_sp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY material_order
    ADD CONSTRAINT material_order_sp_id_fkey FOREIGN KEY (sp_id) REFERENCES service_provider(id);


--
-- Name: out_stock_item_serial_no_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY out_stock_item
    ADD CONSTRAINT out_stock_item_serial_no_fkey FOREIGN KEY (serial_no) REFERENCES in_stock(serial_no);


--
-- Name: product_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product
    ADD CONSTRAINT product_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: product_material_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_material
    ADD CONSTRAINT product_material_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE;


--
-- Name: product_material_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_material
    ADD CONSTRAINT product_material_product_id_fkey FOREIGN KEY (product_id) REFERENCES product(id) ON DELETE CASCADE;


--
-- Name: product_order_item_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_order_item
    ADD CONSTRAINT product_order_item_product_id_fkey FOREIGN KEY (product_id) REFERENCES product(id);


--
-- Name: product_order_item_product_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_order_item
    ADD CONSTRAINT product_order_item_product_order_id_fkey FOREIGN KEY (product_order_id) REFERENCES product_order(id) ON DELETE CASCADE;


--
-- Name: product_sequence_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY product_sequence
    ADD CONSTRAINT product_sequence_id_fkey FOREIGN KEY (id) REFERENCES product(id);


--
-- Name: sp_material_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY sp_material
    ADD CONSTRAINT sp_material_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id) ON DELETE CASCADE;


--
-- Name: sp_material_sp_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY sp_material
    ADD CONSTRAINT sp_material_sp_id_fkey FOREIGN KEY (sp_id) REFERENCES service_provider(id) ON DELETE CASCADE;


--
-- Name: task_material_material_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task_material
    ADD CONSTRAINT task_material_material_id_fkey FOREIGN KEY (material_id) REFERENCES material(id);


--
-- Name: task_material_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task_material
    ADD CONSTRAINT task_material_task_id_fkey FOREIGN KEY (task_id) REFERENCES task(id);


--
-- Name: task_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task
    ADD CONSTRAINT task_product_id_fkey FOREIGN KEY (product_id) REFERENCES product(id);


--
-- Name: task_result_task_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task_result
    ADD CONSTRAINT task_result_task_id_fkey FOREIGN KEY (task_id) REFERENCES task(id);


--
-- Name: task_textile_worker_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY task
    ADD CONSTRAINT task_textile_worker_id_fkey FOREIGN KEY (textile_worker_id) REFERENCES textile_worker(id);


--
-- Name: textile_worker_manager_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: dbuser
--

ALTER TABLE ONLY textile_worker
    ADD CONSTRAINT textile_worker_manager_id_fkey FOREIGN KEY (manager_id) REFERENCES textile_worker(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

