drop table tweets;
drop table network;
drop table users;
drop table likes;

create table if not exists users (
    userid serial primary key,
    username text not null unique,
    password text not null
);

create table if not exists network (
    fr integer references users (userid),
    fe integer references users (userid)
);

create table if not exists tweets (
    tweetid serial primary key,
    userid integer references users (userid),
    tweettime timestamp not null,
    tweet text not null,
    response_tweets integer[],
    in_response_to_tweet integer[]
);

create table if not exists likes (
    tweetid integer references tweets (tweetid),
    num_likes integer
);
