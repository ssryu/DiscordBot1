CREATE TABLE IF NOT EXISTS "錬金石マスタ" (
  "id" INT NOT NULL,
  "名称" VARCHAR(45) NOT NULL,
  PRIMARY KEY ("id"),
  UNIQUE("名称"));

INSERT INTO "錬金石マスタ" ("id", "名称") VALUES (1, '団結された万能の錬金石');
INSERT INTO "錬金石マスタ" ("id", "名称") VALUES (2, '団結された明晰の錬金石');
INSERT INTO "錬金石マスタ" ("id", "名称") VALUES (3, '団結された調教の錬金石');
INSERT INTO "錬金石マスタ" ("id", "名称") VALUES (4, '団結された技術の錬金石');
INSERT INTO "錬金石マスタ" ("id", "名称") VALUES (5, '勇猛なハンターの錬金石');
