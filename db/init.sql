CREATE SCHEMA IF NOT EXISTS devops;

-- Tenants
CREATE TABLE devops.tenants (
    tenant_id SERIAL PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    contact_email VARCHAR(100),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Projects
CREATE TABLE devops.projects (
    project_id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES devops.tenants(tenant_id),
    nom VARCHAR(100) NOT NULL,
    type_template VARCHAR(50),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users
CREATE TABLE devops.users (
    user_id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES devops.tenants(tenant_id),
    nom VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    role VARCHAR(50)
);

-- Pipelines
CREATE TABLE devops.pipelines (
    pipeline_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES devops.projects(project_id),
    status VARCHAR(20),
    last_run TIMESTAMP
);

-- Logs
CREATE TABLE devops.logs (
    log_id SERIAL PRIMARY KEY,
    project_id INT REFERENCES devops.projects(project_id),
    niveau VARCHAR(10),
    message TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Facturation
CREATE TABLE devops.billing (
    billing_id SERIAL PRIMARY KEY,
    tenant_id INT REFERENCES devops.tenants(tenant_id),
    montant NUMERIC(10,2),
    date_facturation DATE DEFAULT CURRENT_DATE
);

-- Audit logs
CREATE TABLE devops.audit_logs (
    audit_id SERIAL PRIMARY KEY,
    action VARCHAR(200),
    user_email VARCHAR(100),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);