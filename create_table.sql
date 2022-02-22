drop table tweets;
drop table network;
drop table users;

create table if not exists users (
    userid serial primary key,
    password varchar(20) not null,
    username varchar(20) not null unique
);

create table if not exists network (
    fr integer references users (userid),
    fe integer references users (userid)
);

create table if not exists tweets (
    tweetid serial primary key,
    tweettime timestamp not null,
    userid integer references users (userid),
    tweet varchar(50) not null,
    tweettype integer not null,
    referencetweetid integer
);