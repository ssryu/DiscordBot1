CREATE TABLE IF NOT EXISTS "取引所基準時刻" (
                                         "std_time" TIME NOT NULL,
                                         "created_at" TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                         PRIMARY KEY ("created_at"));
