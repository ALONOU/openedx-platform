# Tasks MVP - Backlog d'execution

## 1. Regles de priorisation
- P0: bloque la mise en production MVP.
- P1: important pour la qualite MVP.
- P2: utile mais reportable.

## 2. Plan de travail (6 semaines)

## Epic A - Cadrage et setup (S1)
- [ ] A1 (P0) Valider le scope MVP/V2 et figer les exclusions V2.
- [ ] A2 (P0) Valider architecture cible Open edX (Tutor ou bare metal).
- [ ] A3 (P0) Configurer environnements dev/integration.
- [ ] A4 (P1) Definir modeles de roles et matrice de permissions.
- [ ] A5 (P1) Definir template certificat MVP.

## Epic B - Plateforme et securite (S2-S3)
- [ ] B1 (P0) Installer/configurer LMS + CMS.
- [ ] B2 (P0) Configurer HTTPS, sauvegardes et logs.
- [ ] B3 (P0) Configurer roles de base et cohortes.
- [ ] B4 (P1) Creer procedure d'administration utilisateurs.
- [ ] B5 (P1) Valider politique de retention/export donnees personnelles.

## Epic C - Parcours pilote et contenus (S3-S5)
- [ ] C1 (P0) Mapper contenus source vers modules e-learning.
- [ ] C2 (P0) Integrer le parcours pilote complet.
- [ ] C3 (P0) Implementer quiz, devoirs et pre/post tests.
- [ ] C4 (P1) Ajouter ressources telechargeables et pages de support.
- [ ] C5 (P1) Optimiser medias (taille, format, chargement).

## Epic D - Certificats et reporting (S4-S5)
- [ ] D1 (P0) Configurer generation certificat PDF.
- [ ] D2 (P1) Ajouter identifiant unique visible sur certificat.
- [ ] D3 (P1) Evaluer et implementer QR code sans dette excessive.
- [ ] D4 (P0) Configurer tableaux de bord progression/scores.
- [ ] D5 (P0) Activer exports CSV pour suivi cohortes.

## Epic E - QA, recette, go-live (S6)
- [ ] E1 (P0) Ecrire et executer tests de non-regression critiques.
- [ ] E2 (P0) Recette fonctionnelle sur criteres `requirements.md`.
- [ ] E3 (P0) Corriger defects bloquants.
- [ ] E4 (P1) Former admin/formateurs.
- [ ] E5 (P1) Livrer documentation d'exploitation.

## 3. Dependencies critiques
- A1 -> toutes les epics.
- B1 -> C2/C3/D1/D4.
- C2 -> E2.
- D1 + D4 -> E2.

## 4. Tracking recommande
- Statuts: `todo`, `in_progress`, `blocked`, `done`.
- Definition of ready:
  - besoin clarifie,
  - critere d'acceptation ecrit,
  - dependances identifiees.
- Definition of done:
  - implementation terminee,
  - tests passes,
  - documentation mise a jour.
