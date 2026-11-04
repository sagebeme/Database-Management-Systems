-- Create the view jamii_shows (id, title, first_aired, channel) of Jamii TV's shows only, which refuses inserts and updates that would leave Jamii TV.
CREATE VIEW jamii_shows AS
SELECT id, title, first_aired, channel
FROM tv_shows
WHERE channel = 'Jamii TV'
WITH CHECK OPTION;
