#  Chess AI Agent - POC

##  Description

Ce projet est un Proof of Concept (POC) d’un agent IA développé pour la Fédération Française des Échecs (FFE).

L’objectif est de créer un système capable d’aider les joueurs à apprendre les ouvertures en :

* analysant une position d’échecs
* proposant le meilleur coup
* évaluant la position avec un moteur professionnel (Stockfish)
* recommandant du contenu pédagogique

---

##  Fonctionnalités

*  Analyse de position (FEN)
*  Évaluation avec Stockfish
*  Recherche vectorielle (simulée)
*  Recommandation de vidéos YouTube
*  Intégration API Lichess

---

##  Lancer le projet

### 1. Cloner le repository

```
git clone https://github.com/TON_USERNAME/chess-ai-agent.git
cd chess-ai-agent
```

---

### 2. Lancer avec Docker

```
docker-compose up --build
```

 Le backend sera disponible sur :
http://localhost:8000

---

##  Documentation API

Swagger (interface de test) :
http://localhost:8000/docs

---

##  Endpoints

###  Vérifier que l’API fonctionne

```
GET /api/v1/healthcheck
```

Réponse :

```json
{
  "status": "ok"
}
```

---

###  Évaluer une position d’échecs

```
POST /api/v1/evaluate
```

Exemple de requête :

```json
{
  "fen": "rnbqkb1r/pppppppp/5n2/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
}
```

Exemple de réponse :

```json
{
  "best_move": "d2d4",
  "evaluation": {
    "type": "cp",
    "value": -20
  }
}
```

---

###  Obtenir les coups théoriques

```
GET /api/v1/moves?fen=
```

---

###  Recherche vectorielle (Étape 3)

```
GET /vector-search?query=
```

Exemple :

```
/vector-search?query=sicilian
```

---

###  Recommandation de vidéos (Étape 4)

```
GET /api/v1/videos/{opening}
```

Exemple :

```
/api/v1/videos/sicilian
```

---

##  Sécurité

 Important :

* La clé YouTube ne doit **jamais** être exposée
* Utiliser un fichier `.env` :

```
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

* Le fichier `.env` ne doit pas être versionné

---

##  Prérequis

* Docker
* Docker Compose

---

##  Choix techniques

* FastAPI pour la création rapide d’API performantes
* Stockfish pour l’évaluation des positions
* Simulation du vector search pour éviter des dépendances lourdes
* Architecture modulaire (services séparés)

---

##  Arrêter le projet

```
docker-compose down
```

---

##  Auteur

Selma JBILOU

