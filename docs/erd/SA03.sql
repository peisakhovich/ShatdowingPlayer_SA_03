CREATE TABLE language (
  ln_id           int IDENTITY NOT NULL, 
  ln_code         varchar(2) NOT NULL UNIQUE CHECK(LEN(ln_code)=2), 
  ln_name         nvarchar(10) NOT NULL, 
  ln_english_name nvarchar(100) NOT NULL, 
  ln_native_name  nvarchar(100) NULL, 
  PRIMARY KEY (ln_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'Some subset from world languages', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'language';
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'language Name', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'language', 
  @LEVEL2TYPE = N'Column', @LEVEL2NAME = N'ln_name';
CREATE TABLE voice (
  vo_id         int IDENTITY NOT NULL, 
  vo_language   int NOT NULL, 
  vo_short_name nvarchar(100) NOT NULL, 
  vo_gender     nvarchar(20) NOT NULL, 
  PRIMARY KEY (vo_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'The voices. Used format as in Edge TTS (Microsoft Edge Text-To-Speech)', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'voice';
CREATE TABLE phrases (
  ph_id         int IDENTITY NOT NULL, 
  ph_language   int NOT NULL, 
  ph_lng_level  int NOT NULL, 
  ph_text       nvarchar(500) NOT NULL, 
  ph_pause      int DEFAULT 2000 NOT NULL CHECK(ph_pause >= 0), 
  ph_difficulty int DEFAULT 1 NULL CHECK( ph_difficulty  BETWEEN 1 AND 5), 
  ph_active     bit DEFAULT 1 NOT NULL, 
  PRIMARY KEY (ph_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'One phrase in a specific language.', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'phrases';
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'Pause after the end of phrase. unit: milliseconds', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'phrases', 
  @LEVEL2TYPE = N'Column', @LEVEL2NAME = N'ph_pause';
CREATE TABLE language_level (
  ll_id    int IDENTITY NOT NULL, 
  ll_code  nvarchar(10) NOT NULL UNIQUE, 
  ll_name  nvarchar(50) NULL, 
  ll_order smallint NOT NULL CHECK(ll_order > 0), 
  PRIMARY KEY (ll_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'Language proficiency level (CEFR).', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'language_level';
CREATE TABLE users (
  us_id         int IDENTITY NOT NULL, 
  us_nicname    nvarchar(100) NOT NULL UNIQUE, 
  us_first_name nvarchar(255) NULL, 
  us_last_name  nvarchar(255) NULL, 
  PRIMARY KEY (us_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'The users. People who is studying some language', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'users';
CREATE TABLE sets (
  se_id          int IDENTITY NOT NULL, 
  se_user        int NOT NULL, 
  se_user_index  int NOT NULL, 
  se_name        nvarchar(100) NOT NULL, 
  se_description nvarchar(500) NULL, 
  se_active      bit DEFAULT 1 NOT NULL, 
  se_create_date datetime2(0) DEFAULT SYSDATETIME() NOT NULL, 
  se_update_date datetime2(0) NULL, 
  PRIMARY KEY (se_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'The metadata of user sessions.', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'sets';
CREATE TABLE set_items (
  si_id                 int IDENTITY NOT NULL, 
  si_set                int NOT NULL, 
  si_phrase             int NOT NULL, 
  si_translate_language int NULL, 
  si_phrase_voice       int NOT NULL, 
  si_translate_voice    int NOT NULL, 
  si_translate_text     nvarchar(500) NULL, 
  si_order_index        int NOT NULL, 
  si_speed              decimal(4, 2) DEFAULT 1 NOT NULL CHECK(si_speed >= 0.10 AND si_speed <= 2.00), 
  si_repeat             int DEFAULT 1 NOT NULL CHECK(si_repeat >= 1), 
  PRIMARY KEY (si_id));
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'The sets of parameterized items (phrases) combined into one session.', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'set_items';
EXEC sp_addextendedproperty 
  @NAME = N'MS_Description', @VALUE = N'Speed speaking. Relative units. Format TTS', 
  @LEVEL0TYPE = N'Schema', @LEVEL0NAME = N'dbo', 
  @LEVEL1TYPE = N'Table', @LEVEL1NAME = N'set_items', 
  @LEVEL2TYPE = N'Column', @LEVEL2NAME = N'si_speed';
GO
CREATE VIEW vw_set_plan
AS
SELECT

    -- Set
    s.se_id              AS set_id,
    s.se_name            AS set_name,

    -- Item
    si.si_id             AS item_id,
    si.si_order_index    AS item_order,

    -- Phrase
    p.ph_id              AS phrase_id,
    p.ph_text            AS phrase_text,
    p.ph_pause           AS pause_ms,
    p.ph_difficulty      AS difficulty,

    -- Phrase language
    pl.ln_code           AS phrase_language,

    -- Translation
    si.si_translate_text AS translate_text,
    tl.ln_code           AS translate_language,

    -- Voices
    pv.vo_short_name     AS phrase_voice,
    pv.vo_gender         AS phrase_voice_gender,

    tv.vo_short_name     AS translate_voice,
    tv.vo_gender         AS translate_voice_gender,

    -- Playback
    si.si_speed          AS speed,
    si.si_repeat         AS repeat_count

FROM sets s

JOIN set_items si
    ON si.si_set = s.se_id

JOIN phrases p
    ON p.ph_id = si.si_phrase

JOIN language pl
    ON pl.ln_id = p.ph_language

JOIN voice pv
    ON pv.vo_id = si.si_phrase_voice

JOIN voice tv
    ON tv.vo_id = si.si_translate_voice

JOIN language tl
    ON tl.ln_id = si.si_translate_language

WHERE s.se_active = 1
AND p.ph_active = 1;
GO
CREATE VIEW vw_sets
AS
SELECT
      se.se_id                AS set_id
    , us.us_id                AS user_id
    , us.us_nicname           AS user_nickname

    , se.se_user_index        AS set_index
    , se.se_name              AS set_name
    , se.se_description       AS set_description
    , se.se_active            AS set_active

    , se.se_create_date       AS set_create_date
    , se.se_update_date       AS set_update_date

    , COUNT(si.si_id)         AS items_count

FROM sets se

JOIN users us
    ON us.us_id = se.se_user

LEFT JOIN set_items si
    ON si.si_set = se.se_id

GROUP BY

      se.se_id
    , us.us_id
    , us.us_nicname

    , se.se_user_index
    , se.se_name
    , se.se_description
    , se.se_active

    , se.se_create_date
    , se.se_update_date;
GO;
GO
CREATE UNIQUE INDEX voice 
  ON voice (vo_language, vo_short_name);
CREATE UNIQUE INDEX sets 
  ON sets (se_user, se_user_index);
CREATE UNIQUE INDEX set_items 
  ON set_items (si_set, si_order_index);
ALTER TABLE voice ADD CONSTRAINT FKvoice221895 FOREIGN KEY (vo_language) REFERENCES language (ln_id);
ALTER TABLE set_items ADD CONSTRAINT FK_vo_si_translate FOREIGN KEY (si_translate_voice) REFERENCES voice (vo_id);
ALTER TABLE phrases ADD CONSTRAINT FK_ln_ph FOREIGN KEY (ph_language) REFERENCES language (ln_id);
ALTER TABLE phrases ADD CONSTRAINT FL_ll_ph FOREIGN KEY (ph_lng_level) REFERENCES language_level (ll_id);
ALTER TABLE sets ADD CONSTRAINT FK_us_se FOREIGN KEY (se_user) REFERENCES users (us_id);
ALTER TABLE set_items ADD CONSTRAINT FK_se_si FOREIGN KEY (si_set) REFERENCES sets (se_id);
ALTER TABLE set_items ADD CONSTRAINT FK_ph_si FOREIGN KEY (si_phrase) REFERENCES phrases (ph_id);
ALTER TABLE set_items ADD CONSTRAINT FK_ln_si FOREIGN KEY (si_translate_language) REFERENCES language (ln_id);
ALTER TABLE set_items ADD CONSTRAINT FK_vo_si_phrase FOREIGN KEY (si_phrase_voice) REFERENCES voice (vo_id);
