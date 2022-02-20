create table if not exists users (
    userid serial primary key,
    username varchar(20) not null unique
);

create table if not exists tweets (
    tweetid serial primary key,
    userid integer references users (userid ),
    tweet varchar(50) not null
);