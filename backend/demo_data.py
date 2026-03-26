import psycopg2
import random

conn = psycopg2.connect(
    dbname="devops_db",
    user="postgres",
    password="1234",  # À remplacer
    host="localhost",
    port="5432"
)
cur = conn.cursor()

project_templates = ["Web", "Mobile", "API"]

tenants = [
    {"nom": "ClientA", "email": "contact@clienta.com"},
    {"nom": "ClientB", "email": "contact@clientb.com"},
    {"nom": "ClientC", "email": "contact@clientc.com"},
    {"nom": "ClientD", "email": "contact@clientd.com"},
    {"nom": "ClientE", "email": "contact@cliente.com"}
]

tenant_ids = []

# Création tenants
for t in tenants:
    cur.execute("INSERT INTO devops.tenants (nom, contact_email) VALUES (%s, %s) RETURNING tenant_id",
                (t["nom"], t["email"]))
    tenant_id = cur.fetchone()[0]
    tenant_ids.append(tenant_id)
conn.commit()

# Création projets + pipelines + logs + billing
for tenant_id in tenant_ids:
    for template in project_templates:
        cur.execute(
            "INSERT INTO devops.projects (tenant_id, nom, type_template) VALUES (%s, %s, %s) RETURNING project_id",
            (tenant_id, f"{template}_Project_{tenant_id}", template)
        )
        project_id = cur.fetchone()[0]

        # Pipeline
        cur.execute("INSERT INTO devops.pipelines (project_id, status) VALUES (%s, %s)", (project_id, "pending"))

        # Logs aléatoires
        for _ in range(3):
            cur.execute("INSERT INTO devops.logs (project_id, niveau, message) VALUES (%s, %s, %s)",
                        (project_id, random.choice(["INFO","WARN","ERROR"]), f"Log message for project {project_id}"))

    # Facturation
    cur.execute("INSERT INTO devops.billing (tenant_id, montant) VALUES (%s, %s)",
                (tenant_id, random.randint(100, 500)))
conn.commit()
cur.close()
conn.close()

print("Données de démonstration créées avec succès !")