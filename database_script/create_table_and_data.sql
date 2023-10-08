create table airport
(
    id            INT         NULL,
    ident         VARCHAR(40) NOT NULL PRIMARY KEY,
    name          VARCHAR(40) NULL,
    latitude_deg  DOUBLE      NULL,
    longitude_deg DOUBLE      NULL,
    continent     VARCHAR(40) NULL,
    country       VARCHAR(40) NULL,
    gps_code      VARCHAR(40) NULL,
    iata_code     VARCHAR(40) NULL,
    local_code    VARCHAR(40) NULL
);

INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (123, 'BIKF', 'Keflavik International Airport', 63.985001, -22.6056, 'EU', 'Iceland', 'BIKF', 'KEF', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2155, 'EBBR', 'Brussels Airport', 50.901401519800004, 4.48443984985, 'EU', 'Belgium', 'EBBR', 'BRU', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (301881, 'EDDB', 'Berlin Brandenburg Airport', 52.351389, 13.493889, 'EU', 'Germany', 'EDDB', 'BER', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2301, 'EETN', 'Lennart Meri Tallinn Airport', 59.41329956049999, 24.832799911499997, 'EU', 'Estonia', 'EETN', 'TLL', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2307, 'EFHK', 'Helsinki Vantaa Airport', 60.3172, 24.963301, 'EU', 'Finland', 'EFHK', 'HEL', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2513, 'EHAM', 'Amsterdam Airport Schiphol', 52.308601, 4.76389, 'EU', 'Netherlands', 'EHAM', 'AMS', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2541, 'EKBI', 'Billund Airport', 55.7402992249, 9.15178012848, 'EU', 'Denmark', 'EKBI', 'BLL', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2563, 'ELLX', 'Luxembourg-Findel International Airport', 49.6233333, 6.2044444, 'EU', 'Luxembourg', 'ELLX', 'LUX', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2570, 'ENBR', 'Bergen Airport, Flesland', 60.2934, 5.21814, 'EU', 'Norway', 'ENBR', 'BGO', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2608, 'EPGD', 'Gdańsk Lech Wałęsa Airport', 54.377601623535156, 18.46619987487793, 'EU', 'Poland', 'EPGD', 'GDN', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2648, 'ESGG', 'Gothenburg-Landvetter Airport', 57.662799835205, 12.279800415039, 'EU', 'Sweden', 'ESGG', 'GOT', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2758, 'EVRA', 'Riga International Airport', 56.92359924316406, 23.971099853515625, 'EU', 'Latvia', 'EVRA', 'RIX', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (2766, 'EYVI', 'Vilnius International Airport', 54.634102, 25.285801, 'EU', 'Lithuania', 'EYVI', 'VNO', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (3077, 'GCFV', 'Fuerteventura Airport', 28.4527, -13.8638, 'EU', 'Spain', 'GCFV', 'FUE', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (3972, 'LATI', 'Tirana International Airport Mother Tere', 41.4146995544, 19.7206001282, 'EU', 'Albania', 'LATI', 'TIA', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (3993, 'LDZA', 'Zagreb Airport', 45.7429008484, 16.0687999725, 'EU', 'Croatia', 'LDZA', 'ZAG', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4060, 'LFBD', 'Bordeaux-Mérignac Airport', 44.8283, -0.715556, 'EU', 'Falkland Islands', 'LFBD', 'BOD', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4251, 'LGAV', 'Athens Eleftherios Venizelos Internation', 37.936401, 23.9445, 'EU', 'Greece', 'LGAV', 'ATH', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4296, 'LHBP', 'Budapest Liszt Ferenc International Airp', 47.42976, 19.261093, 'EU', 'Hungary', 'LHBP', 'BUD', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4318, 'LICC', 'Catania-Fontanarossa Airport', 37.466801, 15.0664, 'EU', 'Italy', 'LICC', 'CTA', 'CT03');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4386, 'LJLJ', 'Ljubljana Jože Pučnik Airport', 46.223701, 14.4576, 'EU', 'Slovenia', 'LJLJ', 'LJU', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4408, 'LKPR', 'Václav Havel Airport Prague', 50.1008, 14.26, 'EU', 'Czech Republic', 'LKPR', 'PRG', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4427, 'LMML', 'Malta International Airport', 35.857498, 14.4775, 'EU', 'Malta', 'LMML', 'MLA', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4434, 'LOWW', 'Vienna International Airport', 48.110298, 16.5697, 'EU', 'Austria', 'LOWW', 'VIE', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4448, 'LPFR', 'Faro Airport', 37.0144004822, -7.96590995789, 'EU', 'Portugal', 'LPFR', 'FAO', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4490, 'LSGG', 'Geneva Cointrin International Airport', 46.23809814453125, 6.108950138092041, 'EU', 'Switzerland', 'LSGG', 'GVA', '');
INSERT INTO airport (id, ident, name, latitude_deg, longitude_deg, continent, country, gps_code, iata_code, local_code) VALUES (4617, 'LZIB', 'M. R. Štefánik Airport', 48.17020034790039, 17.21269989013672, 'EU', 'Slovakia', 'LZIB', 'BTS', '');

CREATE TABLE reward (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(40) NOT NULL,
    min_amount INT NULL,
    max_amount INT NULL,
    difficult_level VARCHAR(40) NULL,
    passing_condition INT NUll
);

INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (1, 'money', 300, 500, 'easy', 50);
INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (2, 'money', 500, 700, 'normal', 150);
INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (3, 'money', 700, 2000, 'hard', 300);
INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (4, 'weapon', 50, 200, 'easy', 50);
INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (5, 'weapon', 200, 700, 'normal', 150);
INSERT INTO reward (id, name, min_amount, max_amount, difficult_level, passing_condition) VALUES (6, 'weapon', 700, 2500, 'hard', 300);

CREATE TABLE player (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL, 
    location VARCHAR(40)
);

CREATE TABLE ranking (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_id INT NOT NULL,
    score DOUBLE NULL,
    CONSTRAINT `ranking_player_id_fk` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`)
);
