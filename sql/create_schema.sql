#TODO create index for twitter_id

CREATE TABLE `users` (
    `id` serial,
    `username` varchar(20) NOT NULL,
    `url` varchar(60) NULL,
    `twitter_id` bigint unsigned NOT NULL,
    `twitter_access_token_key` varchar(60),
    `twitter_access_token_secret` varchar(60),
    `twitter_display_icon` varchar(80),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY (`id`),
    CONSTRAINT uc_twitter_id UNIQUE (twitter_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


CREATE TABLE `twitterlogins` (
    `id` serial,
    `user_id` bigint unsigned NOT NULL, 
    `username` varchar(20) NOT NULL,
    `twitter_id` bigint unsigned NOT NULL,
    `protected` boolean NOT NULL,
    `following` boolean NOT NULL,
    `friends_count` int(11) unsigned NOT NULL,
    `followers_count` int(11) unsigned NOT NULL,
    `favourites_count` int(11) unsigned NOT NULL,
    `listed_count` int(9) unsigned NOT NULL,
    `status_count` int(9) unsigned NOT NULL,
    `geo_enabled` boolean NOT NULL,
    `location` varchar(20) NOT NULL,
    `coordinates` int(1) NOT NULL,
    `time_zone` varchar(10),
    `lang` varchar(5) NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `dojos` (
	`id` serial,
	`user_id` bigint unsigned NOT NULL,
	`language` varchar(10) NULL,
	`github_repo` varchar(10) NULL,
	`location` varchar(20) NOT NULL,
    `address` varchar(80) NOT NULL,
    `city` varchar(20) NOT NULL,
    `date_hour` DATETIME NULL,
    `slots` int(2) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `participants` (
    `id` serial,
    `user_id` int(11) NOT NULL,
    `dojo_id` int(11) NOT NULL,
    `confirmed` boolean NOT NULL DEFAULT FALSE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY(`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
