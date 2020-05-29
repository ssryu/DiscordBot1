CREATE TABLE IF NOT EXISTS "拠点戦資材" (
                                       "user_id" VARCHAR(32) NOT NULL,
                                       "生命の粉" INT NOT NULL,
                                       "頑丈な原木" INT NOT NULL,
                                       "黒い水晶の原石" INT NOT NULL,
                                       PRIMARY KEY ("user_id"),
                                       CONSTRAINT "fk_拠点戦資材_メンバー"
                                           FOREIGN KEY ("user_id")
                                               REFERENCES "メンバー" ("user_id")
                                                ON DELETE RESTRICT
                                                ON UPDATE RESTRICT);
