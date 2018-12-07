CREATE TABLE cond.app_message  ( 
	app_message_id	serial NOT NULL,
	code          	char(5) NOT NULL,
	message       	text NOT NULL,
	dtm_ins       	timestamp with time zone NOT NULL,
	dtm_mod       	timestamp with time zone NULL,
	PRIMARY KEY(app_message_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.basf2_module  ( 
	basf2_module_id	serial NOT NULL,
	name           	text NOT NULL,
	next_revision  	integer NOT NULL,
	description    	text NULL,
	dtm_ins        	timestamp with time zone NOT NULL,
	dtm_mod        	timestamp with time zone NULL,
	modified_by    	text NOT NULL,
	PRIMARY KEY(basf2_module_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.global_tag  ( 
	global_tag_id       	serial NOT NULL,
	name                	text NOT NULL,
	is_default          	boolean NOT NULL,
	description         	text NULL,
	global_tag_status_id	integer NOT NULL,
	global_tag_type_id  	integer NOT NULL,
	dtm_ins             	timestamp with time zone NOT NULL,
	dtm_mod             	timestamp with time zone NULL,
	modified_by         	text NOT NULL,
	PRIMARY KEY(global_tag_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.global_tag_payload  ( 
	global_tag_payload_id	serial NOT NULL,
	global_tag_id        	integer NOT NULL,
	payload_id           	integer NOT NULL,
	dtm_ins              	timestamp with time zone NOT NULL,
	dtm_mod              	timestamp with time zone NULL,
	PRIMARY KEY(global_tag_payload_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.global_tag_status  ( 
	global_tag_status_id	serial NOT NULL,
	name                	text NOT NULL,
	description         	text NOT NULL,
	dtm_ins             	timestamp with time zone NOT NULL,
	dtm_mod             	timestamp with time zone NULL,
	PRIMARY KEY(global_tag_status_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.global_tag_type  ( 
	global_tag_type_id	serial NOT NULL,
	name              	text NULL,
	description       	text NULL,
	dtm_ins           	timestamp with time zone NOT NULL,
	dtm_mod           	timestamp with time zone NULL,
	PRIMARY KEY(global_tag_type_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.payload  ( 
	payload_id       	serial NOT NULL,
	basf2_module_id  	integer NOT NULL,
	revision         	integer NOT NULL,
	description      	text NULL,
	is_default       	boolean NOT NULL,
	base_url         	text NOT NULL,
	payload_url      	text NOT NULL,
	checksum         	text NOT NULL,
	payload_status_id	integer NOT NULL,
	deleted          	boolean NOT NULL,
	dtm_ins          	timestamp with time zone NOT NULL,
	dtm_mod          	timestamp with time zone NULL,
	modified_by      	text NOT NULL,
	PRIMARY KEY(payload_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.payload_content  ( 
	payload_content_id	serial NOT NULL,
	payload_id        	integer NULL,
	content           	bytea NOT NULL,
	PRIMARY KEY(payload_content_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.payload_iov  ( 
	payload_iov_id       	serial NOT NULL,
	global_tag_payload_id	integer NOT NULL,
	exp_start            	integer NOT NULL,
	run_start            	integer NOT NULL,
	exp_end              	integer NOT NULL,
	run_end              	integer NOT NULL,
	dtm_ins              	timestamp with time zone NOT NULL,
	dtm_mod              	timestamp with time zone NULL,
	modified_by          	text NOT NULL,
	PRIMARY KEY(payload_iov_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.payload_iov_rpt  ( 
	payload_iov_rpt_id   	serial NOT NULL,
	global_tag_payload_id	integer NULL,
	dtm_ins              	timestamp with time zone NULL,
	dtm_mod              	timestamp with time zone NULL,
	global_tag_id        	integer NULL,
	gt_name              	text NULL,
	b2m_name             	text NULL,
	exp_start            	integer NULL,
	exp_end              	integer NULL,
	run_start            	integer NULL,
	run_end              	integer NULL,
	payload_id           	integer NULL,
	payload_iov_id       	integer NULL,
	PRIMARY KEY(payload_iov_rpt_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
CREATE TABLE cond.payload_status  ( 
	payload_status_id	serial NOT NULL,
	name             	text NOT NULL,
	description      	text NOT NULL,
	dtm_ins          	timestamp with time zone NOT NULL,
	dtm_mod          	timestamp with time zone NULL,
	PRIMARY KEY(payload_status_id)
)
WITHOUT OIDS 
TABLESPACE pg_default;
ALTER TABLE cond.basf2_module
	ADD CONSTRAINT basf2_module_chk_name
	CHECK (name ~ '^[ -~]*$'::text);
ALTER TABLE cond.global_tag
	ADD CONSTRAINT global_tag_chk_name
	CHECK (name ~ '^[ -~]*$'::text);
ALTER TABLE cond.global_tag_status
	ADD CONSTRAINT global_tag_status_chk_name
	CHECK (name ~ '^[ -~]*$'::text);
ALTER TABLE cond.global_tag_type
	ADD CONSTRAINT global_tag_type_chk_name
	CHECK (name ~ '^[ -~]*$'::text);
ALTER TABLE cond.payload_iov
	ADD CONSTRAINT exp_run_check
	CHECK (((((exp_start >= 0) AND ((exp_end = (-1)) OR (exp_end >= 0))) AND (run_start >= 0)) AND ((run_end = (-1)) OR (run_end >= 0))) AND (((exp_start < exp_end) OR ((exp_start = exp_end) AND ((run_start <= run_end) OR (run_end = (-1))))) OR ((exp_end = (-1)) AND (run_end = (-1)))));
ALTER TABLE cond.payload_status
	ADD CONSTRAINT payload_status_chk_name
	CHECK (name ~ '^[ -~]*$'::text);
ALTER TABLE cond.payload
	ADD CONSTRAINT basf2_module_ref1
	FOREIGN KEY(basf2_module_id)
	REFERENCES cond.basf2_module(basf2_module_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.global_tag_payload
	ADD CONSTRAINT global_tag_ref1
	FOREIGN KEY(global_tag_id)
	REFERENCES cond.global_tag(global_tag_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.payload_iov
	ADD CONSTRAINT global_tag_payload_ref1
	FOREIGN KEY(global_tag_payload_id)
	REFERENCES cond.global_tag_payload(global_tag_payload_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.global_tag
	ADD CONSTRAINT global_tag_status_ref1
	FOREIGN KEY(global_tag_status_id)
	REFERENCES cond.global_tag_status(global_tag_status_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.global_tag
	ADD CONSTRAINT global_tag_type_ref1
	FOREIGN KEY(global_tag_type_id)
	REFERENCES cond.global_tag_type(global_tag_type_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.payload_content
	ADD CONSTRAINT payload_ref2
	FOREIGN KEY(payload_id)
	REFERENCES cond.payload(payload_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.global_tag_payload
	ADD CONSTRAINT payload_ref1
	FOREIGN KEY(payload_id)
	REFERENCES cond.payload(payload_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
ALTER TABLE cond.payload
	ADD CONSTRAINT payload_status_ref1
	FOREIGN KEY(payload_status_id)
	REFERENCES cond.payload_status(payload_status_id)
	ON DELETE NO ACTION 
	ON UPDATE NO ACTION ;
