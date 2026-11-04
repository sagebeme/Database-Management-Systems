-- Kata: Channels Without Laughs. Channels none of whose shows is a comedy: channel, alphabetical.
SELECT DISTINCT s.channel
FROM tv_shows AS s
WHERE NOT EXISTS (
    SELECT 1
    FROM tv_shows AS s2
    JOIN tv_show_genres AS sg ON sg.show_id = s2.id
    JOIN tv_genres AS g ON g.id = sg.genre_id
    WHERE s2.channel = s.channel AND g.name = 'Comedy'
)
ORDER BY s.channel;
