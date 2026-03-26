# DevOps Central - Installation et exécution

1. Créer la base PostgreSQL :
   - Ouvrir pgAdmin4
   - Exécuter db/init.sql

2. Installer les dépendances Python :
   cd backend
   pip install -r requirements.txt

3. Lancer le backend Flask :
   python app.py

4. Créer les données de démonstration :
   python demo_data.py

5. Ouvrir frontend/index.html dans un navigateur pour voir le dashboard

6. Tester déploiement avec :
   ./scripts/deploy.sh Web_Project_1 production