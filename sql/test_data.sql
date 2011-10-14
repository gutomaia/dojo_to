INSERT INTO users (username, twitter_id) values ('gutomaia', 13818022);
INSERT INTO users (username, twitter_id) values ('thiagoalz', 2);
INSERT INTO users (username, twitter_id) values ('gabriel.ozeas', 3);

INSERT INTO dojos (user_id, language) values (1, 'python');
INSERT INTO dojos (user_id, language) values (1, 'php');
INSERT INTO dojos (user_id, language) values (1, 'java');

INSERT INTO participants (user_id, dojo_id) values (1, 1);
INSERT INTO participants (user_id, dojo_id) values (2, 1);
INSERT INTO participants (user_id, dojo_id) values (3, 1);

INSERT INTO participants (user_id, dojo_id) values (1, 2);
INSERT INTO participants (user_id, dojo_id) values (1, 3);
