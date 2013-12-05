drop table if exists rsvp;
create table rsvp (
  id integer primary key autoincrement,
  user_id text not null,
  meetup_handle not null,
  name text not null,
  rsvp text not null,
  thumb text not null, 
  present integer default 0
); 
