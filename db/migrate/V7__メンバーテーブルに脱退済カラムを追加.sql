ALTER TABLE "メンバー"
    ADD 脱退済 boolean default false NOT NULL;

UPDATE "メンバー" SET "脱退済"=true WHERE "user_id" = '393216952706924554';
UPDATE "メンバー" SET "脱退済"=true WHERE "user_id" = '566919222643523619';
UPDATE "メンバー" SET "脱退済"=true WHERE "user_id" = '557482110685020162';
UPDATE "メンバー" SET "脱退済"=true WHERE "user_id" = '449589207913201668';
UPDATE "メンバー" SET "脱退済"=true WHERE "user_id" = '560294085735350282';
