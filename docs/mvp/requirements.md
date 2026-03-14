# Requirements MVP - Plateforme eLearning

## 1. Objectif produit
Livrer une plateforme e-learning operationnelle basee sur Open edX pour transformer des contenus atelier en parcours numeriques interactifs, suivis et certifiants.

## 2. Perimetre fonctionnel
### 2.1 MVP (in scope)
- Comptes et roles: Apprenant, Formateur, Admin, Super-admin, Observateur.
- Parcours: learning paths, prerequis, deverrouillage progressif, cohortes.
- Contenus: pages, videos, PDF, ressources telechargeables, recherche simple.
- Interactivite: quiz, sondages, devoirs a rendre, cas guides.
- Evaluation: pre-test / post-test, tentatives parametrees, scoring fiable.
- Certificat: generation PDF avec identifiant unique; QR code si faisable sans custom lourd.
- Reporting: progression, scores, exports CSV.
- Communication: emails et annonces.
- Performance: experience mobile correcte, optimisation medias.
- Securite: HTTPS, controle d'acces, journalisation minimale, sauvegardes.

### 2.2 V2 (out of scope MVP)
- SSO Google/Microsoft.
- Multi-tenant pays avance.
- SCORM/xAPI complet.
- Analytics avances (drop-off detaille, comparatifs pays).
- Community features (forum, messagerie, integrations WhatsApp/Telegram).
- Integrations visio natives (Zoom/Teams/Jitsi).
- PWA/offline partiel.

## 3. Exigences non fonctionnelles
- Accessibilite de base et compatibilite navigateurs recents.
- Support FR/EN (contenus et interfaces cibles MVP).
- Conformite donnees personnelles: consentement, politique de confidentialite, retention, export/suppression sur demande.
- Stabilite en connectivite moyenne/faible via contenus optimises.

## 4. Criteres d'acceptation (recette)
- Acces et roles:
  - Connexion fonctionnelle.
  - Permissions conformes par role.
  - Observateur en lecture seule sur dashboards/rapports (aucun droit creation, edition, suppression, correction).
- Parcours:
  - Prerequis et deverrouillage operationnels.
  - Reprise de progression fiable.
- Quiz et devoirs:
  - Scoring correct.
  - Tentatives parametrables.
  - Soumission/correction utilisables.
- Certificat:
  - PDF genere automatiquement apres conditions validees.
  - Identifiant unique visible.
- Reporting:
  - Tableaux de bord lisibles.
  - Exports CSV exploitables.
- Technique:
  - HTTPS actif.
  - Logs et sauvegardes verifies.
  - Navigation mobile fluide sur parcours pilote.

## 5. Hypotheses et risques
- Le role Observateur peut demander un ajustement de permissions.
- QR code de certificat peut necessiter un developpement specifique.
- Le multi-pays sera traite en V2 pour eviter une dette de complexite prematuree.
- Les analytics avances necessitent une couche data dediee (hors MVP).

## 6. Livrables MVP
- Instance Open edX configuree.
- Un parcours pilote complet integre (avant / pendant / apres atelier).
- Configuration des roles et cohortes.
- Evaluations et certificats operationnels.
- Dashboards de base + exports.
- Documentation admin/formateur/apprenant.
