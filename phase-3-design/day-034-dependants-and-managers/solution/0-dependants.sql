-- Create dependants, a weak entity owned by employees: employee_id, name (VARCHAR(40)), relationship ('spouse' or 'child')
-- and born_on (DATE), all required. A dependant is identified by its employee and its name. Deleting an employee deletes their dependants.
CREATE TABLE IF NOT EXISTS dependants (
    employee_id INT NOT NULL,
    name VARCHAR(40) NOT NULL,
    relationship VARCHAR(10) NOT NULL CHECK (relationship IN ('spouse', 'child')),
    born_on DATE NOT NULL,
    PRIMARY KEY (employee_id, name),
    FOREIGN KEY (employee_id) REFERENCES employees (id) ON DELETE CASCADE
);
