CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL,
    `twitter_id` int(11) NOT NULL,
    `twitter_token_access` varchar(10),
    `twitter_display_icon` varchar(20), 
    PRIMARY KEY (`id`),
    CONSTRAINT uc_username UNIQUE (username),
    CONSTRAINT uc_twitter_id UNIQUE (twitter_id)

) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `dojos` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`user_id` int(11) NOT NULL,
	`language` varchar(10) NULL,
	`github_repo` varchar(10) NULL,
	`location` varchar(10) NULL,
	`date` datetime NULL,
	PRIMARY KEY(`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1
