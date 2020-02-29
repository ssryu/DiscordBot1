create table replace_word
(
    id         bigserial not null
        constraint replace_word_pkey
            primary key,
    keyword    text      not null
        constraint replace_word_keyword_key
            unique,
    replace_to text      not null
);

INSERT INTO replace_word (id, keyword, replace_to) VALUES (14, '中2', 'ちゅうに');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (15, 'falspi', 'ふぁる');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (16, '錬金石', 'れんきんせき');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (4, 'ｗ', 'わら');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (5, 'w', 'わら');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (6, '？', 'ふぁっ');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (7, '！', 'んっ');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (8, 'gen＠5963', 'げん');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (9, '純零式', 'じゅんれいしき');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (10, '藍川和(vc)', 'なごみん');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (11, 'ジルスチュアート', 'じる');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (12, 'ω', 'きゃんたま');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (13, '闇闇', '闇ちゃん');
INSERT INTO replace_word (id, keyword, replace_to) VALUES (17, 'NARLION', 'なー');

