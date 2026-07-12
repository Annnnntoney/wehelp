-- WeHelp 第五週 — 所有 SQL 語句（可直接 source 這個檔重跑）
-- 用法：mysql -u root -p 連進去後，執行  source /path/to/queries.sql
-- 或逐段複製到 mysql> 裡跑並截圖。

-- ========== Task 2：建立資料庫與資料表 ==========
CREATE DATABASE website;
USE website;

CREATE TABLE member (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL,
    follower_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- ========== Task 3：SQL CRUD ==========
-- 1. INSERT test + 額外 4 筆
INSERT INTO member (name, email, password, follower_count, time) VALUES
('test',    'test@test.com',      'test',      100, '2026-07-01 10:00:00'),
('Jessica', 'jessica@example.com','pw_jessica',300, '2026-07-02 11:00:00'),
('Bob',     'bob@example.com',    'pw_bob',     50, '2026-07-03 12:00:00'),
('Cassie',  'cassie@example.com', 'pw_cassie', 250, '2026-07-04 13:00:00'),
('Dave',    'dave@example.com',   'pw_dave',     0, '2026-07-05 14:00:00');

-- 2. SELECT 全部
SELECT * FROM member;

-- 3. SELECT 全部，依 time 遞減
SELECT * FROM member ORDER BY time DESC;

-- 4. SELECT 第 2~4 筆（依 time 遞減）
SELECT * FROM member ORDER BY time DESC LIMIT 3 OFFSET 1;

-- 5. SELECT email = test@test.com
SELECT * FROM member WHERE email = 'test@test.com';

-- 6. SELECT name 包含 es
SELECT * FROM member WHERE name LIKE '%es%';

-- 7. SELECT email 且 password 皆符合
SELECT * FROM member WHERE email = 'test@test.com' AND password = 'test';

-- 8. UPDATE name 改為 test2
UPDATE member SET name = 'test2' WHERE email = 'test@test.com';

-- ========== Task 4：SQL 聚合函數 ==========
-- 1. 共幾筆
SELECT COUNT(*) FROM member;

-- 2. follower 總和
SELECT SUM(follower_count) FROM member;

-- 3. follower 平均
SELECT AVG(follower_count) FROM member;

-- 4. follower 前 2 高的平均（子查詢）
SELECT AVG(follower_count) FROM (
    SELECT follower_count FROM member ORDER BY follower_count DESC LIMIT 2
) AS top2;

-- ========== Task 5：SQL JOIN ==========
-- 建立 message 表（含外鍵）
CREATE TABLE message (
    id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
    member_id INT UNSIGNED NOT NULL,
    content TEXT NOT NULL,
    like_count INT UNSIGNED NOT NULL DEFAULT 0,
    time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (member_id) REFERENCES member(id)
);

-- 塞測試訊息
INSERT INTO message (member_id, content, like_count, time) VALUES
(1, '這是 test 的第一則留言', 10, '2026-07-06 09:00:00'),
(1, '這是 test 的第二則留言', 20, '2026-07-06 09:05:00'),
(2, 'Jessica 的留言',        30, '2026-07-06 10:00:00'),
(3, 'Bob 的留言',             5, '2026-07-06 11:00:00');

-- 1. 所有訊息 + 發訊者名稱
SELECT message.*, member.name
FROM message
JOIN member ON message.member_id = member.id;

-- 2. 篩選發訊者 email = test@test.com
SELECT message.*, member.name
FROM message
JOIN member ON message.member_id = member.id
WHERE member.email = 'test@test.com';

-- 3. 該 email 訊息的平均按讚數
SELECT AVG(message.like_count)
FROM message
JOIN member ON message.member_id = member.id
WHERE member.email = 'test@test.com';

-- 4. 依發訊者 email 分組，各組平均按讚數
SELECT member.email, AVG(message.like_count)
FROM message
JOIN member ON message.member_id = member.id
GROUP BY member.email;
