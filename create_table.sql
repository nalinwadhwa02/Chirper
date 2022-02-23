drop table tweets;
drop table network;
drop table users;

create table if not exists users (
    userid serial primary key,
    username text not null unique,
    password text not null
);

create table if not exists network (
    fr serial references users (userid),
    fe serial references users (userid)
);

create table if not exists tweets (
    tweetid serial primary key,
    userid serial references users (userid),
    tweettime timestamp not null,
    tweet text not null,
    response_tweets integer[],
    in_response_to_tweet integer[]
);
