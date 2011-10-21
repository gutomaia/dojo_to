INSERT INTO users (username, twitter_display_icon, twitter_id) values ('gutomaia', 'http://a2.twimg.com/profile_images/652584720/avatar_normal.jpg', 13818022);
INSERT INTO users (username, twitter_id) values ('thiagoalz', 2);
INSERT INTO users (username, twitter_id) values ('gabriel.ozeas', 3);

INSERT INTO dojos (user_id, language, location, address, city, date_hour) values (1, 'python', 'Google', 'a','São Paulo', now());
INSERT INTO dojos (user_id, language, location, address, city, date_hour) values (1, 'php', 'SetTech', 'b','Salvador', now());
INSERT INTO dojos (user_id, language, location, address, city, date_hour) values (1, 'java', 'Ruy Barbosa', 'c', 'Salvador', now());

INSERT INTO participants (user_id, dojo_id) values (1, 1);
INSERT INTO participants (user_id, dojo_id) values (2, 1);
INSERT INTO participants (user_id, dojo_id) values (3, 1);

INSERT INTO participants (user_id, dojo_id) values (1, 2);
INSERT INTO participants (user_id, dojo_id) values (1, 3);

INSERT INTO twitterlogins (user_id, username, twitter_id, protected, following, friends_count, followers_count, favourites_count, listed_count, status_count, geo_enabled, location, coordinates, time_zone, lang) VALUES (1, 'gutomaia',13818022, 0, true, 0,0,0,0,0,true,'brazil',1,'a','a');