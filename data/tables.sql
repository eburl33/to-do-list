CREATE TABLE to_do_lists (
    to_do_list_id SERIAL PRIMARY KEY,
    date_added DATE DEFAULT CURRENT_DATE
);

CREATE TABLE items (
    item_id SERIAL PRIMARY KEY,
    to_do_list_id INT NOT NULL REFERENCES to_do_lists(to_do_list_id),
    description VARCHAR(250),
    is_complete BOOLEAN DEFAULT FALSE
);

INSERT INTO to_do_lists DEFAULT VALUES;

INSERT INTO items (to_do_list_id, description, is_complete) VALUES
(1, 'Take out the trash', false),
(1, 'Walk the dogs', false),
(1, 'Join writing meeting', false),
(1, 'Finish react project', false),
(1, 'clean the kitchen', false),
(1, 'Do the laundry', false);
