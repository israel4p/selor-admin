CREATE TABLE IF NOT EXISTS `adomain` (
  `alias` varchar(128) NOT NULL DEFAULT '',
  `domain` varchar(128) DEFAULT NULL,
  KEY `alias` (`alias`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `aliases` (
  `alias` varchar(255) NOT NULL DEFAULT '',
  `rcpt` varchar(255) DEFAULT NULL,
  KEY `alias` (`alias`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `domain` (
  `name` char(128) NOT NULL DEFAULT '',
  `company` varchar(255) NOT NULL,
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `users` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `mail` varchar(128) NOT NULL DEFAULT '',
  `password` varchar(128) DEFAULT NULL,
  `uid` int(10) unsigned DEFAULT '105',
  `gid` int(10) unsigned DEFAULT '105',
  `home` varchar(255) DEFAULT NULL,
  `maildir` varchar(255) DEFAULT 'Maildir',
  `date_add` date DEFAULT NULL,
  `time_add` time DEFAULT NULL,
  `domain` varchar(128) DEFAULT NULL,
  `name` varchar(150) DEFAULT NULL,
  `ok` tinyint(3) unsigned DEFAULT '1',
  `quota` varchar(20) DEFAULT '100000000',
  `dlocal` varchar(255) NOT NULL,
  PRIMARY KEY (`mail`),
  KEY `id` (`id`)
) ENGINE=MyISAM  DEFAULT CHARSET=latin1 AUTO_INCREMENT=5 ;

CREATE TABLE IF NOT EXISTS `administrator` (
  `id` int(32) unsigned NOT NULL AUTO_INCREMENT,
  `user` varchar(15) NOT NULL,
  `password` varchar(128) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `id` (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1 AUTO_INCREMENT=1;
