-- Create tv_show_genres, linking shows to genres: show_id and genre_id, both required and both real; each pair at most once.
CREATE TABLE IF NOT EXISTS tv_show_genres (
    show_id INT NOT NULL,
    genre_id INT NOT NULL,
    PRIMARY KEY (show_id, genre_id),
    FOREIGN KEY (show_id) REFERENCES tv_shows (id),
    FOREIGN KEY (genre_id) REFERENCES tv_genres (id)
);
