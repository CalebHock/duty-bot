CREATE TABLE IF NOT EXISTS "discord_users" (
    "discord_id" TEXT,
    "name" TEXT,
    "complex" TEXT,
    PRIMARY KEY ("discord_id")
);

CREATE TABLE IF NOT EXISTS "schedule" (
    "name" TEXT NOT NULL,
    "complex" TEXT NOT NULL,
    "start_date" TEXT NOT NULL,
    "end_date" TEXT NOT NULL
);