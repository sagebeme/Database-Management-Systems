"""Day 40: Capstone, Design a Hospital.

Your schema.sql is tested on its own: it must hold data.sql and refuse every row the brief
forbids. The queries run on the reference schema, so a mistake in one doesn't sink the other.
"""

import pytest

from coursekit import er

CONTRACT = {
    "departments": {"id", "name"},
    "doctors": {"id", "name", "licence_no", "department_id"},
    "patients": {"id", "name", "national_id", "born_on", "phone"},
    "next_of_kin": {"patient_id", "name", "relationship", "phone"},
    "visits": {"id", "patient_id", "doctor_id", "visited_at", "diagnosis"},
    "drugs": {"id", "name", "unit_price"},
    "prescriptions": {"visit_id", "drug_id", "quantity"},
}
QUERIES = ["0-doctors_per_department", "1-busiest_doctors", "2-patient_history", "3-visit_bills",
           "4-never_visited", "5-seen_by_every_outpatient_doctor"]
# A new Outpatient doctor, Njeri's first visit, a newly registered patient, and more prescriptions.
SHAKE_UP = """INSERT INTO doctors (id, name, licence_no, department_id) VALUES (6, 'Dr Faith Odera', 'A10006', 1);
INSERT INTO visits (id, patient_id, doctor_id, visited_at, diagnosis) VALUES
    (10, 1, 6, '2026-10-08 09:00:00', 'Malaria cleared'), (11, 5, 5, '2026-10-08 10:00:00', 'Check-up');
INSERT INTO prescriptions (visit_id, drug_id, quantity) VALUES (9, 2, 6), (11, 7, 1);
INSERT INTO patients (id, name, national_id, born_on, phone) VALUES (7, 'Zuhura Ali', '31234567', '2001-03-03', NULL);"""


@pytest.fixture
def yours(mysql, day, target):
    mysql.run_file(target / "schema.sql").check()
    mysql.load(day / "data.sql")
    return mysql


@pytest.fixture
def reference(mysql, day):
    mysql.load(day / "solution" / "schema.sql")
    mysql.load(day / "data.sql")
    return mysql


def refused(db, sql):
    return not db.run(sql).ok


def test_schema_matches_the_contract(yours):
    rows = yours.run("SELECT table_name, column_name FROM information_schema.columns "
                     "WHERE table_schema = DATABASE();").check().rows
    found = {}
    for table, column in rows:
        found.setdefault(table.lower(), set()).add(column.lower())
    assert found == CONTRACT


def test_departments_and_doctors(yours):
    assert refused(yours, "INSERT INTO departments (name) VALUES ('Dental');"), "department names are unique"
    assert refused(yours, "INSERT INTO doctors (name, licence_no, department_id) VALUES ('Dr X', 'A19999', 99);")
    assert refused(yours, "INSERT INTO doctors (name, licence_no, department_id) VALUES ('Dr X', 'A19999', NULL);"), \
        "every doctor works in a department"
    assert refused(yours, "INSERT INTO doctors (name, licence_no, department_id) VALUES ('Dr X', 'A10001', 1);"), \
        "licence numbers are unique"


def test_patients(yours):
    yours.run("INSERT INTO patients (name, national_id, born_on) VALUES ('Baby Two', NULL, '2025-01-01');").check()
    assert refused(yours, "INSERT INTO patients (name, national_id, born_on) VALUES ('Copy', '23456781', '1990-01-01');")
    assert refused(yours, "INSERT INTO patients (name, born_on) VALUES (NULL, '1990-01-01');")
    assert refused(yours, "INSERT INTO patients (name, born_on, phone) VALUES ('Bad Phone', '1990-01-01', '0711000101');")


def test_next_of_kin(yours):
    assert refused(yours, "INSERT INTO next_of_kin VALUES (1, 'James Kamau', 'brother', '254700000000');"), \
        "a patient names each next of kin once"
    assert refused(yours, "INSERT INTO next_of_kin VALUES (99, 'Nobody', 'spouse', '254700000000');")
    yours.run("INSERT INTO next_of_kin VALUES (5, 'Ann Mwangi', 'sister', '254700000001');").check()
    yours.run("DELETE FROM patients WHERE id = 5;").check()
    assert yours.run("SELECT COUNT(*) FROM next_of_kin WHERE patient_id = 5;").check().rows == [("0",)], \
        "next of kin go with their patient"


def test_medical_records_stay(yours):
    assert refused(yours, "DELETE FROM patients WHERE id = 1;"), "a patient with visits can't be deleted"
    assert refused(yours, "DELETE FROM doctors WHERE id = 1;"), "a doctor who has seen patients can't be deleted"
    assert refused(yours, "INSERT INTO visits (patient_id, doctor_id, visited_at) VALUES (99, 1, NOW());")
    assert refused(yours, "INSERT INTO visits (patient_id, doctor_id, visited_at) VALUES (1, NULL, NOW());")
    assert refused(yours, "INSERT INTO visits (patient_id, doctor_id, visited_at) VALUES (1, 1, NULL);")


def test_drugs_and_prescriptions(yours):
    assert refused(yours, "INSERT INTO drugs (name, unit_price) VALUES ('Paracetamol', 6.00);")
    assert refused(yours, "INSERT INTO drugs (name, unit_price) VALUES ('Free Money', -1.00);")
    assert refused(yours, "INSERT INTO prescriptions VALUES (9, 2, 0);"), "a quantity is at least 1"
    assert refused(yours, "INSERT INTO prescriptions VALUES (1, 1, 5);"), "a drug appears once per visit"
    assert refused(yours, "INSERT INTO prescriptions VALUES (99, 1, 5);")
    assert refused(yours, "INSERT INTO prescriptions VALUES (9, 99, 5);")
    yours.run("INSERT INTO prescriptions VALUES (9, 7, 1);").check()
    assert yours.run("SELECT unit_price FROM drugs WHERE id = 1;").check().rows == [("120.00",)], "prices keep cents"


def test_diagram(target):
    d = er.load(target / "hospital.mmd")
    for name in ("DEPARTMENT", "DOCTOR", "PATIENT", "NEXT_OF_KIN", "VISIT", "DRUG", "PRESCRIPTION"):
        assert d.has_entity(name) and d.keys(name), f"{name}, with a primary key"
    assert d.how_many("DEPARTMENT", per="DOCTOR") == (1, 1)
    assert d.how_many("PATIENT", per="VISIT") == (1, 1) and d.how_many("DOCTOR", per="VISIT") == (1, 1)
    assert d.how_many("VISIT", per="PATIENT")[0] == 0, "a registered patient may not have visited yet"
    kin = d.between("PATIENT", "NEXT_OF_KIN")
    assert len(kin) == 1 and kin[0].identifying, "NEXT_OF_KIN is a weak entity of PATIENT"
    assert d.keys("NEXT_OF_KIN") == {"patient_id", "name"}
    assert d.how_many("VISIT", per="PRESCRIPTION") == (1, 1) and d.how_many("DRUG", per="PRESCRIPTION") == (1, 1)
    assert not d.between("VISIT", "DRUG"), "visits and drugs meet through PRESCRIPTION, not directly"


@pytest.mark.parametrize("name", QUERIES)
@pytest.mark.parametrize("shaken", [False, True], ids=["data", "shake-up"])
def test_queries_against_reference(reference, day, target, name, shaken):
    if shaken:
        reference.run(SHAKE_UP).check()
    got = reference.run_file(target / f"{name}.sql").check()
    want = reference.run_file(day / "solution" / f"{name}.sql").check()
    assert got.columns == want.columns
    assert got.rows == want.rows


def test_known_answers(reference, target):
    def rows(name):
        return reference.run_file(target / f"{name}.sql").check().rows

    assert rows("0-doctors_per_department")[0] == ("Outpatient", "2") and rows("0-doctors_per_department")[-1] == ("Eye", "0")
    assert rows("1-busiest_doctors")[0] == ("Dr Brian Mutua", "3")
    history = rows("2-patient_history")
    assert [h[3] for h in history] == ["Malaria", "Antenatal check", "Malaria follow-up"]
    assert history[1][2] == "Maternity"
    bills = rows("3-visit_bills")
    assert bills[0] == ("1", "Wanjiru Kamau", "2970.00") and bills[8] == ("9", "Omondi Otieno", "0.00")
    assert rows("4-never_visited") == [("Njeri Mwangi",)]
    assert rows("5-seen_by_every_outpatient_doctor") == [("Omondi Otieno",), ("Wanjiru Kamau",)]


def test_kata_the_pharmacy_board(reference, target):
    reference.run_file(target / "kata.sql").check()
    kind = reference.run("SELECT table_type FROM information_schema.tables "
                         "WHERE table_schema = DATABASE() AND table_name = 'drug_usage';").check().rows
    assert kind == [("VIEW",)]
    got = reference.run("SELECT * FROM drug_usage ORDER BY drug;").check()
    assert got.columns == ["drug", "prescriptions", "units"]
    usage = {r[0]: r[1:] for r in got.rows}
    assert usage["Paracetamol"] == ("4", "50") and usage["Insulin"] == ("0", "0")
    reference.run("INSERT INTO prescriptions VALUES (9, 7, 2);").check()
    assert reference.run("SELECT units FROM drug_usage WHERE drug = 'Insulin';").check().rows == [("2",)]
