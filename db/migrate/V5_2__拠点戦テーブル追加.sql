CREATE TABLE IF NOT EXISTS "拠点戦" (
                                     "日付" DATE NOT NULL,
                                     "拠点マップ_マップマスタ_id" INT NOT NULL,
                                     "参加申請受付可否" BOOLEAN NOT NULL,
                                     PRIMARY KEY ("日付"),
                                     CONSTRAINT "fk_拠点戦_拠点マップ1"
                                         FOREIGN KEY ("拠点マップ_マップマスタ_id")
                                             REFERENCES "拠点マップ" ("マップマスタ_id")
                                             ON DELETE RESTRICT
                                             ON UPDATE CASCADE);

CREATE INDEX "fk_拠点戦_拠点マップ1_idx" ON "拠点戦" ("拠点マップ_マップマスタ_id" ASC);


CREATE TABLE IF NOT EXISTS "参加種別マスタ" (
                                         "id" VARCHAR(10) NOT NULL,
                                         PRIMARY KEY ("id"));
INSERT INTO "参加種別マスタ" ("id") VALUES ('参加');
INSERT INTO "参加種別マスタ" ("id") VALUES ('欠席');
INSERT INTO "参加種別マスタ" ("id") VALUES ('遅刻');


CREATE TABLE IF NOT EXISTS "参加VC状況マスタ" (
                                           "id" VARCHAR(10) NOT NULL,
                                           PRIMARY KEY ("id"));
INSERT INTO "参加VC状況マスタ" ("id") VALUES ('VC可');
INSERT INTO "参加VC状況マスタ" ("id") VALUES ('VC不可');
INSERT INTO "参加VC状況マスタ" ("id") VALUES ('聞き専');


CREATE TABLE IF NOT EXISTS "拠点戦参加" (
                                       "拠点戦_日付" DATE NOT NULL,
                                       "メンバー_user_id" VARCHAR(32) NOT NULL,
                                       "参加種別マスタ_id" VARCHAR(10) NOT NULL,
                                       "参加VC状況マスタ_id" VARCHAR(10) NOT NULL,
                                       PRIMARY KEY ("拠点戦_日付", "メンバー_user_id"),
                                       CONSTRAINT "fk_拠点戦参加_メンバー1"
                                           FOREIGN KEY ("メンバー_user_id")
                                               REFERENCES "メンバー" ("user_id")
                                               ON DELETE NO ACTION
                                               ON UPDATE CASCADE,
                                       CONSTRAINT "fk_拠点戦参加_拠点戦1"
                                           FOREIGN KEY ("拠点戦_日付")
                                               REFERENCES "拠点戦" ("日付")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                       CONSTRAINT "fk_拠点戦参加_参加種別マスタ1"
                                           FOREIGN KEY ("参加種別マスタ_id")
                                               REFERENCES "参加種別マスタ" ("id")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE,
                                       CONSTRAINT "fk_拠点戦参加_参加VC状況マスタ1"
                                           FOREIGN KEY ("参加VC状況マスタ_id")
                                               REFERENCES "参加VC状況マスタ" ("id")
                                               ON DELETE CASCADE
                                               ON UPDATE CASCADE);
CREATE INDEX "fk_拠点戦参加_メンバー1_idx" ON "拠点戦参加" ("メンバー_user_id" ASC);
CREATE INDEX "fk_拠点戦参加_参加種別マスタ1_idx" ON "拠点戦参加" ("参加種別マスタ_id" ASC);
CREATE INDEX "fk_拠点戦参加_参加VC状況マスタ1_idx" ON "拠点戦参加" ("参加VC状況マスタ_id" ASC);
