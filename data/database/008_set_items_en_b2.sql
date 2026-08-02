/*==============================================================
  009_set_items_multilingual_b2.sql
  Set : English & Polish training B2 001
==============================================================*/

DECLARE @SetId INT =
(
    SELECT se_id
    FROM sets
    WHERE se_user = 3
      AND se_user_index = 1
);

DECLARE @RuLanguage INT =
(
    SELECT ln_id
    FROM language
    WHERE ln_locale = N'ru-RU'
);

DECLARE @RuVoice INT =
(
    SELECT vo_id
    FROM voice
    WHERE vo_short_name = N'ru-RU-SvetlanaNeural'
);

INSERT INTO set_items
(
      si_set
    , si_phrase
    , si_translate_language
    , si_phrase_voice
    , si_translate_voice
    , si_translate_text
    , si_order_index
)
SELECT
      @SetId
    , p.ph_id
    , @RuLanguage
    , pv.vo_id
    , @RuVoice
    , v.translate_text
    , v.item_order
FROM phrases p

JOIN language l
    ON l.ln_id = p.ph_language

JOIN language_level ll
    ON ll.ll_id = p.ph_lng_level

JOIN voice pv
    ON pv.vo_language = l.ln_id
   AND pv.vo_gender =
       CASE
           WHEN l.ln_locale IN (N'en-US', N'pl-PL', N'de-DE', N'ro-RO')
           THEN N'Female'
       END

JOIN
(
VALUES

( 1, N'en-US',
N'I would like to reserve a room for three nights.',
N'Я хотел(а) бы забронировать номер на три ночи.'),

( 2, N'en-US',
N'Could you tell me where the nearest railway station is?',
N'Не могли бы вы сказать, где находится ближайший железнодорожный вокзал?'),

( 3, N'en-US',
N'Our flight has been delayed because of the weather.',
N'Наш рейс был задержан из-за плохой погоды.'),

( 4, N'en-US',
N'Please let me know if there are any changes.',
N'Пожалуйста, сообщите мне, если появятся какие-либо изменения.'),

( 5, N'pl-PL',
N'Chcia?bym zarezerwowa? pok?j na trzy noce.',
N'Я хотел(а) бы забронировать номер на три ночи.'),

( 6, N'pl-PL',
N'Czy m?g?by Pan powiedzie?, gdzie znajduje si? najbli?szy dworzec kolejowy?',
N'Не могли бы вы сказать, где находится ближайший железнодорожный вокзал?'),

( 7, N'pl-PL',
N'Nasz lot zosta? op??niony z powodu z?ej pogody.',
N'Наш рейс был задержан из-за плохой погоды.'),

( 8, N'pl-PL',
N'Prosz? da? mi zna?, je?eli pojawi? si? jakie? zmiany.',
N'Пожалуйста, сообщите мне, если появятся какие-либо изменения.'),

( 9, N'de-DE',
N'Ich m?chte ein Zimmer f?r drei N?chte reservieren.',
N'Я хотел(а) бы забронировать номер на три ночи.'),

(10, N'de-DE',
N'K?nnten Sie mir sagen, wo sich der n?chste Bahnhof befindet?',
N'Не могли бы вы сказать, где находится ближайший железнодорожный вокзал?'),

(11, N'de-DE',
N'Unser Flug hat sich wegen des schlechten Wetters versp?tet.',
N'Наш рейс был задержан из-за плохой погоды.'),

(12, N'de-DE',
N'Bitte informieren Sie mich, falls sich etwas ?ndert.',
N'Пожалуйста, сообщите мне, если появятся какие-либо изменения.'),

(13, N'ro-RO',
N'A? dori s? rezerv o camer? pentru trei nop?i.',
N'Я хотел(а) бы забронировать номер на три ночи.'),

(14, N'ro-RO',
N'?mi pute?i spune unde se afl? cea mai apropiat? gar??',
N'Не могли бы вы сказать, где находится ближайший железнодорожный вокзал?'),

(15, N'ro-RO',
N'Zborul nostru a fost ?nt?rziat din cauza vremii nefavorabile.',
N'Наш рейс был задержан из-за плохой погоды.'),

(16, N'ro-RO',
N'V? rog s? m? anun?a?i dac? apar modific?ri.',
N'Пожалуйста, сообщите мне, если появятся какие-либо изменения.')

) AS v
(
      item_order
    , phrase_locale
    , phrase_text
    , translate_text
)
ON  p.ph_text = v.phrase_text
AND l.ln_locale = v.phrase_locale

WHERE ll.ll_code = N'B2'

ORDER BY
    v.item_order;