CREATE TABLE IF NOT EXISTS "地域マスタ" (
                                    "id" SERIAL NOT NULL,
                                    "地域名" VARCHAR(45) NOT NULL,
                                    PRIMARY KEY ("id"));

INSERT INTO "地域マスタ" ("id", "地域名") VALUES (1, 'バレノス自治領');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (2, 'セレンディア自治領');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (3, '中立国境地帯');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (4, 'カルフェオン北部直轄領');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (5, 'カルフェオン南東部直轄領');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (6, 'カルフェオン南西部直轄領');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (7, 'メディア北部地域');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (8, 'メディア南部地域');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (9, 'バレンシア西部地域');
INSERT INTO "地域マスタ" ("id", "地域名") VALUES (10, 'バレンシア北部地域');


CREATE TABLE IF NOT EXISTS "マップマスタ" (
                                        "id" SERIAL NOT NULL,
                                        "マップ名" VARCHAR(45) NOT NULL,
                                        PRIMARY KEY ("id"));

INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (1,'略奪の森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (2,'セレンディア北部平原');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (3,'デルニール農場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (4,'捨てられた地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (5,'忘却の地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (6,'オージェ峠');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (7,'ナマズマンキャンプ');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (8,'トレント街角');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (9,'サイクロプスの土地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (10,'アグリス祭壇');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (11,'ナーガ抽出場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (12,'南部警備キャンプ');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (13,'ギュントの丘');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (14,'採石場の洞窟');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (15,'サウニールキャンプ');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (16,'ジャイアント族駐屯地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (17,'マンシャの森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (18,'ルツム族駐屯地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (19,'フォニエールの山荘');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (20,'ベリア農場地帯');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (21,'アレハンドロ農場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (22,'中部警備キャンプ');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (23,'ナーガ沼地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (24,'フォガン湿地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (25,'北部大農場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (26,'ケプラン街角');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (27,'グラトニー洞窟');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (28,'ガビノ、コーエン農場地帯');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (29,'ベア川下流');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (30,'エワズの丘');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (31,'廃城跡入り口');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (32,'旧ダンデリオン');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (33,'ブリの木遺跡');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (34,'サウニール戦場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (35,'カイア渡し場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (36,'ルツム監視警戒所');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (37,'エントの森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (38,'カルフェオン寺院跡');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (39,'魔女の礼拝堂');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (40,'隠遁の森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (41,'リンチ農場廃墟');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (42,'プレディー砦');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (43,'カランダ尾根');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (44,'ディアス農場地帯');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (45,'トロル防御基地');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (46,'オージェの家');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (47,'隠された修道院');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (48,'クリオ村');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (49,'ロングリーフの木の森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (50,'アグリス平原');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (51,'北部採石場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (52,'モレッティ農場');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (53,'南西部関所');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (54,'オークキャンプ');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (55,'ハーピーの絶壁');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (56,'ブリの森');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (57,'ゲハク平原');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (58,'カイア湖');
INSERT INTO "マップマスタ" ("id", "マップ名") VALUES (59,'マンシャの森の奥');


CREATE TABLE IF NOT EXISTS "マップ地域" (
                                       "マップマスタ_id" INT NOT NULL,
                                       "地域マスタ_id" INT NOT NULL,
                                       PRIMARY KEY ("マップマスタ_id"),
                                       CONSTRAINT "fk_マップ地域_マップマスタ1"
                                           FOREIGN KEY ("マップマスタ_id")
                                               REFERENCES "マップマスタ" ("id")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                       CONSTRAINT "fk_マップ地域_地域マスタ1"
                                           FOREIGN KEY ("地域マスタ_id")
                                               REFERENCES "地域マスタ" ("id")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE);
CREATE INDEX "fk_マップ地域_地域1_idx" ON "マップ地域" ("地域マスタ_id");

INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (1, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (2, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (3, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (4, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (5, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (6, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (7, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (8, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (9, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (10, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (11, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (12, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (13, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (14, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (15, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (16, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (17, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (18, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (19, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (20, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (21, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (22, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (23, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (24, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (25, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (26, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (27, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (28, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (29, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (30, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (31, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (32, 3);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (33, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (34, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (35, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (36, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (37, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (38, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (39, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (40, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (41, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (42, 3);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (43, 3);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (44, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (45, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (46, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (47, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (48, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (49, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (50, 1);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (51, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (52, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (53, 2);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (54, 3);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (55, 3);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (56, 4);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (57, 5);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (58, 6);
INSERT INTO "マップ地域" ("マップマスタ_id", "地域マスタ_id") VALUES (59, 6);


CREATE TABLE IF NOT EXISTS "拠点マップ" (
                                       "マップマスタ_id" INT NOT NULL,
                                       "等級" INT NOT NULL,
                                       "曜日" INT NOT NULL,
                                       PRIMARY KEY ("マップマスタ_id"),
                                       CONSTRAINT "fk_拠点マップ_マップマスタ1"
                                           FOREIGN KEY ("マップマスタ_id")
                                               REFERENCES "マップマスタ" ("id")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE);

INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (1, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (2, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (3, 3, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (4, 1, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (5, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (6, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (7, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (8, 1, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (9, 2, 0);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (10, 3, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (11, 2, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (12, 2, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (13, 2, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (14, 2, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (15, 1, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (16, 2, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (17, 1, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (18, 3, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (19, 1, 1);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (20, 2, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (21, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (22, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (23, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (24, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (25, 3, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (26, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (27, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (28, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (29, 1, 2);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (30, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (31, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (32, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (33, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (34, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (35, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (36, 2, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (37, 1, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (38, 2, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (39, 3, 3);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (40, 1, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (41, 1, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (42, 1, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (43, 2, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (44, 2, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (45, 2, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (46, 3, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (47, 2, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (48, 1, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (49, 1, 4);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (50, 1, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (51, 1, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (52, 3, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (53, 1, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (54, 2, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (55, 1, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (56, 1, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (57, 2, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (58, 2, 5);
INSERT INTO "拠点マップ" ("マップマスタ_id", "等級", "曜日") VALUES (59, 1, 5);
