CREATE TABLE credentials(
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    token VARCHAR(255) NOT NULL,
    user_id INTEGER NOT NULL,

    CONSTRAINT fk_credentials_user FOREIGN KEY (user_id)
        REFERENCES user(id)
);
