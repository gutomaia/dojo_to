INSERT INTO users (username, twitter_display_icon, twitter_id) values ('gutomaia', 'http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg', 13818022);
INSERT INTO users (username, twitter_id) values ('thiagoalz', 2);
INSERT INTO users (username, twitter_id) values ('gabriel.ozeas', 3);

INSERT INTO dojos (user_id, language, location, city) values (1, 'python', 'Google', 'São Paulo');
INSERT INTO dojos (user_id, language, location, city) values (1, 'php', 'SetTech', 'Salvador');
INSERT INTO dojos (user_id, language, location, city) values (1, 'java', 'Ruy Barbosa', 'Salvador');

INSERT INTO participants (user_id, dojo_id) values (1, 1);
INSERT INTO participants (user_id, dojo_id) values (2, 1);
INSERT INTO participants (user_id, dojo_id) values (3, 1);

INSERT INTO participants (user_id, dojo_id) values (1, 2);
INSERT INTO participants (user_id, dojo_id) values (1, 3);
