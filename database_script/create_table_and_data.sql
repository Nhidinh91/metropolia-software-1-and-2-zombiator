create table airport
(
    id            INT         NULL,
    ident         VARCHAR(40) NOT NULL PRIMARY KEY,
    name          VARCHAR(40) NULL,
    latitude_deg  DOUBLE      NULL,
    longitude_deg DOUBLE      NULL,
    continent     VARCHAR(40) NULL,
    country       VARCHAR(40) NULL,
    stage         INT         NULL DEFAULT 0
);

INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (11, 'BIKF', 'Keflavik International Airport', 63.985001, -22.6056, 'EU', 'Iceland', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (2, 'EBBR', 'Brussels Airport', 50.901401519800004, 4.48443984985, 'EU', 'Belgium', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (8, 'EDDB', 'Frankfurt am Main Airport', 50.036249, 8.559294, 'EU', 'Germany', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (5, 'EETN', 'Lennart Meri Tallinn Airport', 59.41329956049999, 24.832799911499997, 'EU', 'Estonia', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (6, 'EFHK', 'Helsinki Vantaa Airport', 60.3172, 24.963301, 'EU', 'Finland', 1);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (17, 'EHAM', 'Amsterdam Airport Schiphol', 52.308601, 4.76389, 'EU', 'Netherlands', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (4, 'EKBI', 'Copenhagen Airport', 55.617900848389, 12.656000137329, 'EU', 'Denmark', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (15, 'ELLX', 'Luxembourg-Findel International Airport', 49.6233333, 6.2044444, 'EU', 'Luxembourg', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (18, 'ENBR', 'Oslo Airport, Gardermoen', 60.193901, 11.1004, 'EU', 'Norway', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (19, 'EPGD', 'Warsaw Chopin Airport', 52.1656990051, 20.967100143399996, 'EU', 'Poland', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (24, 'ESGG', 'Stockholm-Arlanda Airport', 59.651901245117, 17.918600082397, 'EU', 'Sweden', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (13, 'EVRA', 'Riga International Airport', 56.92359924316406, 23.971099853515625, 'EU', 'Latvia', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (14, 'EYVI', 'Vilnius International Airport', 54.634102, 25.285801, 'EU', 'Lithuania', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (23, 'GCFV', 'Adolfo Suárez Madrid–Barajas Airport', 40.471926, -3.56264, 'EU', 'Spain', 2);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (7, 'LFPG', 'Charles de Gaulle International Airport', 49.012798, 2.55, 'EU', 'France', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (9, 'LGAV', 'Athens Eleftherios Venizelos Internation', 37.936401, 23.9445, 'EU', 'Greece', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (10, 'LHBP', 'Budapest Liszt Ferenc International Airp', 47.42976, 19.261093, 'EU', 'Hungary', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (12, 'LICC', 'Leonardo da Vinci-Fiumicino Airport', 41.804532, 12.251998, 'EU', 'Italy', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (22, 'LJLJ', 'Ljubljana Joze Pucnik Airport', 46.223701, 14.4576, 'EU', 'Slovenia', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (3, 'LKPR', 'Václav Havel Airport Prague', 50.1008, 14.26, 'EU', 'Czech Republic', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (16, 'LMML', 'Malta International Airport', 35.857498, 14.4775, 'EU', 'Malta', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (1, 'LOWW', 'Vienna International Airport', 48.110298, 16.5697, 'EU', 'Austria', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (20, 'LPFR', 'Humberto Delgado Airport (Lisbon Portela', 38.7813, -9.13592, 'EU', 'Portugal', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (25, 'LSGG', 'Zürich Airport', 47.458056, 8.548056, 'EU', 'Switzerland', 0);
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, stage) VALUES (21, 'LZIB', 'M. R. Štefánik Airport', 48.17020034790039, 17.21269989013672, 'EU', 'Slovakia', 0);

CREATE TABLE reward (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    amount INT NULL,
    difficult_level VARCHAR(40) NULL,
    passing_condition INT NUll
);

INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (1, 'energy', 500, 'easy', 50);
INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (2, 'energy', 700, 'normal', 150);
INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (3, 'energy', 1000, 'hard', 300);
INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (4, 'weapon', 200, 'easy', 50);
INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (5, 'weapon', 700, 'normal', 150);
INSERT INTO reward (id, name, amount, difficult_level, passing_condition) VALUES (6, 'weapon', 1000, 'hard', 300);

CREATE TABLE player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    location VARCHAR(40) DEFAULT 'Finland',
    inventory_weapon INT NOT NULL DEFAULT 0,
    inventory_energy INT NOT NULL DEFAULT 0,
    game_status VARCHAR(40) NOT NULL DEFAULT 'not_started',
    game_master_password VARCHAR(255) NULL,
    game_master_password_retry_times INT NOT NULL DEFAULT 0,
    game_start_at DATETIME NULL,
    game_end_at DATETIME NULL,
    game_actual_end_at DATETIME NULL,
    game_paused_at DATETIME NULL,
    game_password_collected VARCHAR(255) NULL,
    game_completed_airports VARCHAR(255) NULL
);

CREATE TABLE ranking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    score INT NOT NULL,
    duration VARCHAR(255) NULL,
    weapon_remaining INT NULL,
    energy_remaining INT NULL,
    CONSTRAINT `ranking_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`)
);

