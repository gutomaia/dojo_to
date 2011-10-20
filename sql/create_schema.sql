CREATE TABLE `users` (
    `id` serial,
    `username` varchar(20) NOT NULL,
    `url` varchar(20) NULL,
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
    `username` varchar(10) NOT NULL,
    `twitter_id` bigint unsigned NOT NULL,
    `protected` int(1) NOT NULL,
    `following` int(1) NOT NULL,
    `friends_count` int(11) unsigned NOT NULL,
    `followers_count` int(11) unsigned NOT NULL,
    `favourites_count` int(11) unsigned NOT NULL,
    `listed_count` int(9) unsigned NOT NULL,
    `status_count` int(9) unsigned NOT NULL,
    `geo_enabled` int(1) NOT NULL,
    `location` varchar(20) NOT NULL,
    coordinates int(1) NOT NULL,
    time_zone varchar(10),
    lang varchar(10) NOT NULL,
    created_at varchar(10) NOT NULL,
    PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `dojos` (
	`id` serial,
	`user_id` bigint unsigned NOT NULL,
	`language` varchar(10) NULL,
	`github_repo` varchar(10) NULL,
	`location` varchar(10) NULL,
    `address` varchar(10) NULL,
    `city` varchar(20) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `participants` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `user_id` int(11) NOT NULL,
    `dojo_id` int(11) NOT NULL,
    `confirmed` int(1) NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY(`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;
