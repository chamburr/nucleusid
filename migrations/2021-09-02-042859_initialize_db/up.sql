CREATE TABLE person
(
    id         bigint    NOT NULL PRIMARY KEY,
    name       text      NOT NULL,
    email      text      NOT NULL UNIQUE,
    password   text      NOT NULL,
    public_key text      NOT NULL,
    secret     text      NOT NULL,
    verified   boolean   NOT NULL,
    updated_at timestamp NOT NULL
);

CREATE TABLE device
(
    id         bigint    NOT NULL PRIMARY KEY,
    person     bigint    NOT NULL REFERENCES person(id),
    name       text      NOT NULL,
    ip_address text      NOT NULL,
    location   text      NOT NULL,
    token_iat  bigint    NOT NULL,
    last_login timestamp NOT NULL
);

CREATE TABLE folder
(
    id       bigint  NOT NULL PRIMARY KEY,
    person   bigint  NOT NULL REFERENCES person(id),
    name     text    NOT NULL,
    sharing  boolean NOT NULL,
    built_in boolean NOT NULL
);

CREATE TABLE share
(
    folder     bigint    NOT NULL REFERENCES folder(id),
    person     bigint    NOT NULL REFERENCES person(id),
    owner      boolean   NOT NULL,
    view_only  boolean   NOT NULL,
    secret     text      NOT NULL,
    confirmed  boolean   NOT NULL,
    created_at timestamp NOT NULL,
    PRIMARY KEY(folder, person)
);

CREATE TABLE account
(
    id          bigint    NOT NULL PRIMARY KEY,
    person      bigint    NOT NULL REFERENCES person(id),
    folder      bigint    NOT NULL REFERENCES folder(id),
    name        text      NOT NULL,
    username    text      NOT NULL,
    password    text      NOT NULL,
    totp        text      NOT NULL,
    note        text      NOT NULL
);

CREATE FUNCTION update_timestamp() RETURNS TRIGGER AS
$$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql strict
                    immutable;

CREATE TRIGGER t_update_timestamp
    BEFORE UPDATE
    OF password ON person
    FOR EACH ROW
EXECUTE PROCEDURE update_timestamp();
