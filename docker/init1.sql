create table IF NOT exists competitions(
	id INTEGER primary key,
	name VARCHAR not null,
	code VARCHAR unique not null,
	type VARCHAR not null,
	emblem TEXT
);

create table IF NOT exists teams(
	id INTEGER primary key, 
	name VARCHAR not null,
	short_name VARCHAR,
	tla CHAR(3), 
	crest TEXT 
);


create table IF NOT exists seasons(
	id INTEGER primary key,
	competition_id INTEGER references competitions(id) not null,
	start_date DATE not null,
	end_date DATE not null,
	winner_team_id INTEGER references teams(id)
);

create table matches(
	id INTEGER primary key,
	utc_date TIMESTAMPTZ not null,
	matchday INTEGER,
	home_team_id INTEGER references teams(id) not null,
	away_team_id INTEGER references teams(id) not null, 
	score_fulltime_home INTEGER,
	score_fulltime_away INTEGER,
	score_halftime_home INTEGER,
	score_halftime_away INTEGER,
	winner VARCHAR,
	season_id INTEGER references seasons(id) not null,
	status VARCHAR not null,
	last_updated TIMESTAMPTZ
);