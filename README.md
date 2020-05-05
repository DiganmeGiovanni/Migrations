# Scriba

Manage your db versions with pure SQL in a framework/language agnostic way

Scriba allows you to write your migrations (up and down) scripts in pure sql and manage it no matter which languages or frameworks your application is build on

## How it works?

* You write your migration scripts in multiple sql files (One per migration)
* You write undo migration scripts (One per migration)
* You setup data access params in a configuration file
* Run `scriba` to do/undo/list you migrations

## Getting started

Create you first migration in a sql file, ensure to name the file like: `V<version_number>_<snake_case_name>.sql`

*Follow naming convention is essential in order to run migrations with right name and in appropriate order*
 
Let's say you have following file named `v1_create_tables.sql` (will be parsed as: `V1` `Create tables`)

```sql
CREATE TABLE user(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(500) NOT NULL
);

CREATE TABLE car(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id)
        REFERENCES user(id)
)
```

And the undo migration script named: `V<version_number>_snake_case_name>.sql`

*Version number should match exactly with migrate file, you can use whatever you want for the name part*
 
 `v1_undo_create_tables.sql`:
 ```sql
DROP TABLE car;
DROP TABLE user;
 ```

### Place scripts on right directories

Put all your *up* migrations in a dedicated directory, and all the *down* migrations into a different one, you should have a structure similar to:

```bash
|-migrations/
|- |- settings.yml 
|- |- up/
|- |- - v1_create_tables.sql
|- |- - v2_create_credentials_table.sql
|- |- down/
|- |- - v1_undo_create_tables.sql
|- |- - v2_destroy_credentials_table.sql
```

### Setup db connection and settings

Place the database connection settings into `settings.yml` file:

```yaml
datasource:
  host: 192.168.100.43
  username: developer
  password: d3v3lopm3nt
  database: cars
```

*Refer to [place_link_here](http://something.com) for a detailed list of possible settings

### And now run migrations:

```bash
<place docker command here> scriba migrate
```

## What does scriba means?

Scriba *Latin*: Person who registered history in ancient times

