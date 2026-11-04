// Eight made-up secondary schools.
//   mongosh --quiet mongodb://127.0.0.1:27018/shule < phase-7-beyond-mysql/day-083-hello-mongodb/setup.js
db.schools.drop();
db.schools.insertMany([
  { _id: 1, name: "Mlima High School", county: "Nyeri", students: 1450, category: "national", clubs: ["chess", "drama"] },
  { _id: 2, name: "St. Faith Girls", county: "Kiambu", students: 980, category: "extra-county", clubs: ["music"] },
  { _id: 3, name: "Ziwa Boys", county: "Kisumu", students: 1210, category: "national" },
  { _id: 4, name: "Bahari Mixed Day", county: "Mombasa", students: 640, category: "sub-county", clubs: [] },
  { _id: 5, name: "St. Peter's Kapsabet", county: "Nandi", students: 1100, category: "extra-county", clubs: ["athletics"] },
  { _id: 6, name: "Jiji Academy", county: "Nairobi", students: 1630, category: "national", clubs: ["robotics", "chess"] },
  { _id: 7, name: "Kilima Day", county: "Kiambu", students: 450, category: "sub-county" },
  { _id: 8, name: "Stadi Technical", county: "Nairobi", students: 720, category: "county", clubs: ["robotics"] }
]);
