# Design Technique MVP - Open edX

## 1. Objectif technique
Mettre en place une architecture Open edX stable et configurable pour livrer rapidement le MVP sans customisation lourde.

## 2. Architecture cible
- Services coeur:
  - LMS: experience apprenant, suivi progression, evaluations.
  - CMS (Studio): authoring et gestion des parcours.
- Services data:
  - MySQL (donnees applicatives),
  - MongoDB (certains contenus/metadata),
  - Memcached (cache).
- Frontend:
  - UI Open edX native, MFEs selon disponibilite environnement.

## 3. Principes de design MVP
- Configuration-first: privilegier les capacites natives Open edX.
- Custom minimal: seulement pour combler un gap P0 de recette.
- Separation claire MVP/V2: pas d'implementation anticipee des fonctions V2.
- Traçabilite: toute deviation au design doit etre documentee.

## 4. Modelisation fonctionnelle
### 4.1 Roles et permissions
- Apprenant: suit parcours, rend activites, passe evaluations, obtient certificat.
- Formateur: suit cohortes, corrige devoirs, publie annonces, exporte resultats.
- Admin: gere cours, cohortes, utilisateurs, certificats, reporting operationnel.
- Super-admin: gouvernance globale, parametres plateforme, securite, sauvegardes.
- Observateur: lecture seule des dashboards et rapports selon perimetre autorise, sans droits d'edition, de correction ou de gestion.

### 4.2 Parcours pedagogique
- Structure type module:
  - objectifs (3-5),
  - lecons (pages/video/PDF),
  - activite pratique,
  - quiz de validation,
  - ressources.
- Progression:
  - prerequis de module,
  - deverrouillage conditionnel,
  - reprise de progression.

## 5. Certificats et verification
- MVP:
  - certificat PDF natif Open edX,
  - identifiant unique.
- Option MVP+:
  - QR code si integration faible complexite.
- V2:
  - verification publique avancee/micro-certifications.

## 6. Reporting et KPIs
- Donnees minimales MVP:
  - inscriptions/activation,
  - completion,
  - scores pre/post tests,
  - progression par cohorte.
- Sorties:
  - dashboards standards,
  - export CSV.
- V2:
  - analytics comportementales avancees.

## 7. Securite et conformite
- HTTPS obligatoire.
- Controle d'acces par role.
- Logs d'audit operationnels.
- Sauvegardes periodiques testees.
- Politique donnees personnelles: consentement + retention + droits d'export/suppression.

## 8. Limites MVP assumees
- Pas de multi-tenant pays complet.
- Pas de SSO externe.
- Pas de SCORM/xAPI complet.
- Pas d'integration visio native.

## 9. Decisions d'implementation
- Toute demande non couverte par MVP doit etre taggee `V2-candidate`.
- Toute customisation back-end doit inclure:
  - justification business,
  - impact maintenance,
  - test associe.
