create table users(
    userid bigint,
    username varchar(20) not null,
    constraint user_key primary key (userid),
);

create table tweets(
    tweetid bigint,
    userid bigint,
    tweet varchar(50) not null,
    constraint tweet_key primary key (tweetid),
    constraint user_fkey foreign key (userid) references users (userid)
);