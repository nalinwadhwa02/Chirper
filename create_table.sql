drop table tweets;
drop table network;
drop table users;

create table if not exists users (
    userid text primary key,
    firstname text not null,
    lastname text not null,
    password text not null
);

create table if not exists network (
    fr text references users (userid),
    fe text references users (userid)
);

create table if not exists tweets (
    tweetid serial primary key,
    userid text references users (userid),
    tweettime timestamp not null,
    tweet text not null,
    response_tweets text[],
    in_response_to_tweet text
);
