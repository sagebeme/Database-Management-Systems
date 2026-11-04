-- Name, grade and points of everyone with an A or A-, best first, ties alphabetical.
SELECT name, grade, points FROM results WHERE grade IN ('A', 'A-') ORDER BY points DESC, name;
