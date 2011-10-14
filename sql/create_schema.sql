CREATE TABLE `users` (
    `id` int(11) NOT NULL AUTO_INCREMENT,
    `username` varchar(20) NOT NULL,
    `twitter_id` int(11) NOT NULL,
    `twitter_access_token_key` varchar(60),
    `twitter_access_token_secret` varchar(60),
    `twitter_display_icon` varchar(80),
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,    
    PRIMARY KEY (`id`),
    CONSTRAINT uc_twitter_id UNIQUE (twitter_id)
) ENGINE=MyISAM AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

CREATE TABLE `dojos` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`user_id` int(11) NOT NULL,
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
