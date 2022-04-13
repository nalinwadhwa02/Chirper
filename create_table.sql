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
    tweetid integer references tweets(tweetid),
    userid integer references users(userid)
);

\copy users from users.csv delimiter ',' csv header;
\copy tweets from tweets.csv delimiter ',' csv header;
\copy network from network.csv delimiter ',' csv header;
\copy likes from likes.csv delimiter ',' csv header;

select setval('users_userid_seq',(select max(userid) from users));
select setval('tweets_tweetid_seq',(select max(tweetid) from tweets));

create table like_nums as 
select t.tweetid, count(l.tweetid) as like_num 
from likes l right join tweets t on t.tweetid = l.tweetid 
group by t.tweetid;

