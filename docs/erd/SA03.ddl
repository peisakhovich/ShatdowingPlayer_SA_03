CREATE TABLE language (ln_id int IDENTITY NOT NULL, ln_code varchar(2) NOT NULL UNIQUE, ln_name varchar(10) NOT NULL, ln_english_name varchar(100) NULL, ln_native_name varchar(100) NULL, voicevo_id int NOT NULL, PRIMARY KEY (ln_id));
EXEC sp_addextendedproperty @NAME = N'MS_Description', @VALUE = N'language Name', @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'language', @LEVEL2TYPE = N'Column', @LEVEL2NAME = N'ln_name';
CREATE TABLE voice (vo_id int IDENTITY NOT NULL, vo_language int NOT NULL, vo_sort_name varchar(100) NOT NULL, vo_gender varchar(20) NOT NULL, PRIMARY KEY (vo_id));
ALTER TABLE voice ADD CONSTRAINT FKvoice221895 FOREIGN KEY (vo_language) REFERENCES language (ln_id);
