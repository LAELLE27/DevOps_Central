from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'ton_secret_jwt_ici'  # à remplacer par un vrai secret

# Connexion PostgreSQL
conn = psycopg2.connect(
    dbname="devops_db",
    user="postgres",
    password="1234",
    host="localhost",
    port="5432"
)

# --- Décorateur JWT ---
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('x-access-token')
        if not token:
            return jsonify({"message":"Token manquant"}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            request.user_id = data['user_id']
            request.tenant_id = data['tenant_id']
            request.role = data['role']
        except:
            return jsonify({"message":"Token invalide"}), 401
        return f(*args, **kwargs)
    return decorated

# --- Users / Auth ---
@app.route("/users/register", methods=["POST"])
def register_user():
    data = request.json
    cur = conn.cursor()
    cur.execute("SELECT user_id FROM devops.users WHERE email=%s", (data["email"],))
    if cur.fetchone():
        cur.close()
        return jsonify({"status":"error","message":"Email déjà utilisé"}), 400

    hashed_password = generate_password_hash(data["password"])
    cur.execute(
        "INSERT INTO devops.users (email, password, tenant_id, nom, role) VALUES (%s,%s,%s,%s,%s) RETURNING user_id",
        (data["email"], hashed_password, data["tenant_id"], data.get("nom",""), data.get("role","user"))
    )
    user_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"status":"success","user_id": user_id})

@app.route("/users/login", methods=["POST"])
def login_user():
    data = request.json
    cur = conn.cursor()
    cur.execute("SELECT user_id, password, tenant_id, role, nom FROM devops.users WHERE email=%s", (data["email"],))
    row = cur.fetchone()
    cur.close()
    if row and check_password_hash(row[1], data["password"]):
        token = jwt.encode({
            "user_id": row[0],
            "tenant_id": row[2],
            "role": row[3],
            "exp": datetime.utcnow() + timedelta(hours=8)
        }, app.config['SECRET_KEY'], algorithm="HS256")
        return jsonify({
            "status":"success",
            "token": token,
            "user_id": row[0],
            "tenant_id": row[2],
            "nom": row[4],
            "role": row[3]
        })
    return jsonify({"status":"error","message":"Email ou mot de passe incorrect"}), 401

# --- Tenants ---
@app.route("/tenants", methods=["POST"])
@token_required
def create_tenant():
    if request.role != 'admin':
        return jsonify({"message":"Non autorisé"}), 403
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devops.tenants (nom, contact_email) VALUES (%s, %s) RETURNING tenant_id",
        (data["nom"], data["contact_email"])
    )
    tenant_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"tenant_id": tenant_id})

@app.route("/tenants", methods=["GET"])
@token_required
def list_tenants():
    cur = conn.cursor()
    cur.execute("SELECT tenant_id, nom, contact_email, date_creation FROM devops.tenants")
    rows = cur.fetchall()
    cur.close()
    tenants = [{"tenant_id": r[0], "nom": r[1], "contact_email": r[2], "date_creation": str(r[3])} for r in rows]
    return jsonify(tenants)

# --- Projects ---
@app.route("/projects", methods=["POST"])
@token_required
def create_project():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devops.projects (tenant_id, nom, type_template, date_creation) VALUES (%s, %s, %s, now()) RETURNING project_id",
        (request.tenant_id, data["nom"], data["type_template"])
    )
    project_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"project_id": project_id}), 201

@app.route("/projects", methods=["GET"])
@token_required
def list_projects():
    cur = conn.cursor()
    cur.execute(
        "SELECT project_id, tenant_id, nom, type_template, date_creation FROM devops.projects WHERE tenant_id=%s ORDER BY project_id",
        (request.tenant_id,)
    )
    rows = cur.fetchall()
    cur.close()
    projects = [{"project_id": r[0], "tenant_id": r[1], "nom": r[2], "type_template": r[3], "date_creation": str(r[4])} for r in rows]
    return jsonify(projects)

@app.route("/projects/<int:pid>", methods=["DELETE"])
@token_required
def delete_project(pid):
    cur = conn.cursor()
    cur.execute("DELETE FROM devops.projects WHERE project_id=%s AND tenant_id=%s", (pid, request.tenant_id))
    conn.commit()
    cur.close()
    return '', 204

# --- Pipelines ---
@app.route("/pipelines", methods=["POST"])
@token_required
def create_pipeline():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devops.pipelines (project_id, status) VALUES (%s, %s) RETURNING pipeline_id",
        (data["project_id"], "pending")
    )
    pipeline_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"pipeline_id": pipeline_id})

@app.route("/pipelines", methods=["GET"])
@token_required
def list_pipelines():
    cur = conn.cursor()
    cur.execute("""
        SELECT p.pipeline_id, p.project_id, p.status, p.last_run
        FROM devops.pipelines p
        JOIN devops.projects pr ON pr.project_id = p.project_id
        WHERE pr.tenant_id=%s
    """, (request.tenant_id,))
    rows = cur.fetchall()
    cur.close()
    pipelines = [{"pipeline_id": r[0], "project_id": r[1], "status": r[2], "last_run": str(r[3])} for r in rows]
    return jsonify(pipelines)

# --- Logs ---
@app.route("/logs", methods=["POST"])
@token_required
def create_log():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devops.logs (project_id, niveau, message) VALUES (%s, %s, %s) RETURNING log_id",
        (data["project_id"], data["niveau"], data["message"])
    )
    log_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"log_id": log_id})

@app.route("/logs", methods=["GET"])
@token_required
def list_logs():
    cur = conn.cursor()
    cur.execute("""
        SELECT l.log_id, l.project_id, l.niveau, l.message, l.timestamp
        FROM devops.logs l
        JOIN devops.projects p ON p.project_id = l.project_id
        WHERE p.tenant_id=%s
    """, (request.tenant_id,))
    rows = cur.fetchall()
    cur.close()
    logs = [{"log_id": r[0], "project_id": r[1], "niveau": r[2], "message": r[3], "timestamp": str(r[4])} for r in rows]
    return jsonify(logs)

# --- Facturation ---
@app.route("/billing", methods=["POST"])
@token_required
def create_billing():
    data = request.json
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO devops.billing (tenant_id, montant) VALUES (%s, %s) RETURNING billing_id",
        (request.tenant_id, data["montant"])
    )
    billing_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    return jsonify({"billing_id": billing_id})

@app.route("/billing", methods=["GET"])
@token_required
def list_billing():
    cur = conn.cursor()
    cur.execute("SELECT billing_id, tenant_id, montant, date_facturation FROM devops.billing WHERE tenant_id=%s", (request.tenant_id,))
    rows = cur.fetchall()
    cur.close()
    billing = [{"billing_id": r[0], "tenant_id": r[1], "montant": float(r[2]), "date_facturation": str(r[3])} for r in rows]
    return jsonify(billing)

# --- Gestion utilisateurs (admin tenant) ---
@app.route("/users", methods=["GET"])
@token_required
def list_users():
    if request.role != 'admin':
        return jsonify({"message":"Non autorisé"}), 403
    cur = conn.cursor()
    cur.execute("SELECT user_id, email, nom, role FROM devops.users WHERE tenant_id=%s", (request.tenant_id,))
    rows = cur.fetchall()
    cur.close()
    users = [{"user_id": r[0], "email": r[1], "nom": r[2], "role": r[3]} for r in rows]
    return jsonify(users)

@app.route("/users/<int:uid>", methods=["DELETE"])
@token_required
def delete_user(uid):
    if request.role != 'admin':
        return jsonify({"message":"Non autorisé"}), 403
    cur = conn.cursor()
    cur.execute("DELETE FROM devops.users WHERE user_id=%s AND tenant_id=%s", (uid, request.tenant_id))
    conn.commit()
    cur.close()
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)