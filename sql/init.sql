CREATE TABLE "user"(
  id SERIAL NOT NULL,
  username text NOT NULL,
  "password" text NOT NULL,
  CONSTRAINT user_pkey PRIMARY KEY(id)
);

CREATE TABLE user_ids (
    user_id text NOT NULL,
    assigned_id text NOT NULL,
    PRIMARY KEY (user_id, assigned_id)
);

CREATE OR REPLACE FUNCTION toggle_assigned_id(p_user_id text, p_assigned_id character varying)
RETURNS void AS $$
BEGIN
    -- Check if the user_id and assigned_id already exist
    IF EXISTS (SELECT 1 FROM user_ids WHERE user_id = p_user_id AND assigned_id = p_assigned_id) THEN
        -- If they exist, delete the entry (unassign)
        DELETE FROM user_ids WHERE user_id = p_user_id AND assigned_id = p_assigned_id;
        RAISE NOTICE 'Entry for user_id % and assigned_id % deleted.', p_user_id, p_assigned_id;
    ELSE
        -- If they do not exist, insert a new entry (assign)
        INSERT INTO user_ids (user_id, assigned_id) VALUES (p_user_id, p_assigned_id);
        RAISE NOTICE 'Entry for user_id % and assigned_id % added.', p_user_id, p_assigned_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

