# Requirements Document - Open edX Simplification

## Introduction

Ce document définit les exigences pour simplifier l'architecture Open edX en retirant la dépendance à Tutor et en utilisant un setup Docker Compose natif minimal. L'objectif est de réduire la complexité opérationnelle tout en conservant les fonctionnalités essentielles du MVP e-learning.

## Glossary

- **Tutor**: Outil de déploiement et d'orchestration Docker pour Open edX développé par Overhang.io
- **LMS**: Learning Management System - interface apprenant d'Open edX
- **CMS**: Content Management System (Studio) - interface d'authoring d'Open edX
- **Docker_Compose**: Outil d'orchestration de conteneurs Docker via fichier YAML déclaratif
- **Native_Setup**: Configuration Docker Compose directe sans couche d'abstraction Tutor
- **MVP_Stack**: Ensemble minimal de services nécessaires au fonctionnement du MVP
- **Service_Container**: Conteneur Docker exécutant un service spécifique (LMS, MySQL, Redis, etc.)
- **Configuration_Layer**: Fichiers de configuration pour les services Open edX (settings Django, uwsgi, etc.)
- **Data_Volume**: Volume Docker persistant pour les données applicatives
- **Celery_Worker**: Processus asynchrone pour les tâches de fond (emails, certificats, etc.)

## Requirements

### Requirement 1: Retrait de la dépendance Tutor

**User Story:** En tant qu'administrateur système, je veux retirer Tutor de l'architecture, afin de simplifier le déploiement et réduire les couches d'abstraction.

#### Acceptance Criteria

1. THE Native_Setup SHALL NOT depend on Tutor binaries or Tutor CLI commands
2. THE Native_Setup SHALL NOT use Tutor-generated configuration files
3. THE Native_Setup SHALL NOT require Tutor plugins for core MVP functionality
4. WHEN deploying the platform, THE Native_Setup SHALL use only docker-compose commands
5. THE Configuration_Layer SHALL be directly editable without Tutor rebuild process

### Requirement 2: Configuration Docker Compose minimale

**User Story:** En tant qu'administrateur système, je veux une configuration Docker Compose simple et lisible, afin de faciliter la maintenance et le débogage.

#### Acceptance Criteria

1. THE Docker_Compose SHALL define exactly the MVP_Stack services (LMS, CMS, MySQL, Redis, MongoDB, Meilisearch, Caddy, Celery workers)
2. THE Docker_Compose SHALL use official or well-maintained Docker images
3. THE Docker_Compose SHALL expose only necessary ports for development and production
4. THE Docker_Compose SHALL define explicit service dependencies using depends_on
5. THE Docker_Compose SHALL use named volumes for data persistence
6. WHEN a service fails, THE Docker_Compose SHALL restart it automatically using restart policies

### Requirement 3: Services essentiels MVP

**User Story:** En tant qu'architecte, je veux conserver uniquement les services nécessaires au MVP, afin de réduire la surface d'attaque et la complexité opérationnelle.

#### Acceptance Criteria

1. THE MVP_Stack SHALL include LMS for learner experience
2. THE MVP_Stack SHALL include CMS for content authoring
3. THE MVP_Stack SHALL include MySQL 8.4 for application data
4. THE MVP_Stack SHALL include Redis 7.4 for caching and session storage
5. THE MVP_Stack SHALL include MongoDB 7.0 for content metadata
6. THE MVP_Stack SHALL include Meilisearch 1.8 for search functionality
7. THE MVP_Stack SHALL include Caddy as reverse proxy
8. THE MVP_Stack SHALL include Celery workers (lms-worker, cms-worker) for asynchronous tasks
9. THE MVP_Stack SHALL NOT include services for V2 features (forums, analytics, SSO providers)

### Requirement 4: Images Docker natives

**User Story:** En tant qu'administrateur système, je veux utiliser des images Docker standard, afin de faciliter les mises à jour et réduire la dépendance à des images custom.

#### Acceptance Criteria

1. WHEN selecting base images, THE Native_Setup SHALL prefer official Docker Hub images
2. THE Native_Setup SHALL use mysql:8.4 official image
3. THE Native_Setup SHALL use redis:7.4 official image
4. THE Native_Setup SHALL use mongo:7.0 official image
5. THE Native_Setup SHALL use getmeili/meilisearch:v1.8 official image
6. THE Native_Setup SHALL use caddy:2.7 official image
7. FOR Open edX services, THE Native_Setup SHALL use overhangio/openedx images OR build custom minimal images
8. THE Native_Setup SHALL document the rationale for any non-official image choice

### Requirement 5: Configuration directe des services

**User Story:** En tant qu'administrateur système, je veux configurer directement les services via fichiers de configuration, afin d'éviter les étapes de génération intermédiaires.

#### Acceptance Criteria

1. THE Configuration_Layer SHALL provide Django settings files directly mounted in containers
2. THE Configuration_Layer SHALL provide uwsgi.ini configuration directly mounted
3. THE Configuration_Layer SHALL provide Caddyfile directly mounted
4. WHEN modifying configuration, THE Native_Setup SHALL require only container restart (no rebuild)
5. THE Configuration_Layer SHALL use environment variables for secrets and environment-specific values
6. THE Configuration_Layer SHALL separate development and production settings clearly

### Requirement 6: Gestion des données persistantes

**User Story:** En tant qu'administrateur système, je veux une gestion claire des données persistantes, afin de garantir la sauvegarde et la restauration.

#### Acceptance Criteria

1. THE Data_Volume SHALL persist MySQL data across container restarts
2. THE Data_Volume SHALL persist MongoDB data across container restarts
3. THE Data_Volume SHALL persist Redis data across container restarts
4. THE Data_Volume SHALL persist Meilisearch index across container restarts
5. THE Data_Volume SHALL persist uploaded media files (videos, PDFs, images)
6. THE Data_Volume SHALL persist LMS and CMS application data
7. WHEN backing up, THE Native_Setup SHALL provide clear volume mapping documentation
8. THE Data_Volume SHALL use named volumes OR bind mounts with explicit paths

### Requirement 7: Fonctionnalités MVP préservées

**User Story:** En tant que product owner, je veux que toutes les fonctionnalités MVP restent opérationnelles, afin de garantir la valeur métier.

#### Acceptance Criteria

1. AFTER migration, THE Native_Setup SHALL support user authentication and role management (Apprenant, Formateur, Admin, Super-admin, Observateur)
2. AFTER migration, THE Native_Setup SHALL support learning paths with prerequisites and progressive unlocking
3. AFTER migration, THE Native_Setup SHALL support content types (pages, videos, PDFs, downloadable resources)
4. AFTER migration, THE Native_Setup SHALL support interactive elements (quizzes, polls, assignments)
5. AFTER migration, THE Native_Setup SHALL support pre-test/post-test evaluations with scoring
6. AFTER migration, THE Native_Setup SHALL generate PDF certificates with unique identifiers
7. AFTER migration, THE Native_Setup SHALL provide reporting dashboards and CSV exports
8. AFTER migration, THE Native_Setup SHALL send emails and announcements
9. AFTER migration, THE Native_Setup SHALL maintain mobile-first experience
10. AFTER migration, THE Native_Setup SHALL support FR/EN localization

### Requirement 8: Tâches asynchrones

**User Story:** En tant qu'administrateur système, je veux que les tâches asynchrones fonctionnent correctement, afin de garantir l'envoi d'emails et la génération de certificats.

#### Acceptance Criteria

1. THE Celery_Worker SHALL process LMS background tasks (email sending, certificate generation)
2. THE Celery_Worker SHALL process CMS background tasks (content indexing, export)
3. THE Celery_Worker SHALL connect to Redis as message broker
4. WHEN a task fails, THE Celery_Worker SHALL log the error with sufficient detail
5. THE Celery_Worker SHALL use the same Open edX image as LMS/CMS with different command
6. THE Celery_Worker SHALL have access to the same data volumes as LMS/CMS

### Requirement 9: Sécurité et secrets

**User Story:** En tant qu'administrateur sécurité, je veux une gestion sécurisée des secrets, afin de protéger les données sensibles.

#### Acceptance Criteria

1. THE Native_Setup SHALL NOT store secrets in docker-compose.yml file
2. THE Native_Setup SHALL use environment variables for database passwords
3. THE Native_Setup SHALL use environment variables for API keys (Meilisearch, OAuth2)
4. THE Native_Setup SHALL use environment variables for Django SECRET_KEY
5. THE Native_Setup SHALL provide .env.example template with placeholder values
6. THE Native_Setup SHALL document secret rotation procedures
7. WHEN deploying to production, THE Native_Setup SHALL enforce HTTPS via Caddy configuration

### Requirement 10: Migration depuis Tutor

**User Story:** En tant qu'administrateur système, je veux migrer depuis l'installation Tutor existante, afin de préserver les données et la configuration.

#### Acceptance Criteria

1. THE Native_Setup SHALL provide migration documentation from Tutor to native setup
2. THE Native_Setup SHALL document database export/import procedures
3. THE Native_Setup SHALL document media files migration procedures
4. THE Native_Setup SHALL document configuration mapping (Tutor config → native config)
5. THE Native_Setup SHALL provide rollback procedures in case of migration failure
6. WHEN migrating, THE Native_Setup SHALL preserve user accounts and enrollments
7. WHEN migrating, THE Native_Setup SHALL preserve course content and structure
8. WHEN migrating, THE Native_Setup SHALL preserve certificates and completion records

### Requirement 11: Simplification des modules Open edX

**User Story:** En tant qu'architecte, je veux désactiver les modules Open edX non nécessaires au MVP, afin de réduire la complexité et améliorer les performances.

**Contexte:** Open edX inclut de nombreuses fonctionnalités avancées qui ne sont pas requises pour le MVP. Ces fonctionnalités ajoutent de la complexité, consomment des ressources et ralentissent le déploiement. La désactivation se fait via la configuration Django (INSTALLED_APPS, FEATURES flags) sans modifier le code source.

**Features V2 à désactiver (hors scope MVP):**
- Forums et discussions communautaires (django_comment_client, forum)
- SSO externe (Google, Microsoft, SAML providers)
- Multi-tenant avancé (site-specific configurations complexes)
- SCORM/xAPI (standards e-learning avancés)
- Analytics avancés (insights, detailed drop-off tracking)
- Intégrations visio (Zoom, Teams, Jitsi plugins)
- Messagerie/chat (WhatsApp, Telegram integrations)
- PWA/offline capabilities

**Features MVP à conserver (in scope):**
- Authentification de base (username/password, email verification)
- Rôles et permissions (Student, Instructor, Staff, Admin, Observer custom role)
- Parcours et prérequis (course structure, prerequisites, gating)
- Contenus (HTML, Video, PDF, downloadable resources)
- Quiz et devoirs (problem types, assignments, submissions)
- Évaluations (pre-test/post-test, grading, attempts)
- Certificats PDF (certificate generation, unique IDs)
- Cohortes (cohort management, cohort-specific content)
- Reporting de base (progress tracking, grade exports CSV)
- Emails et annonces (bulk email, course announcements)
- Recherche simple (Meilisearch integration)

#### Acceptance Criteria

1. THE Configuration_Layer SHALL remove forum/discussion apps from INSTALLED_APPS (lms.djangoapps.discussion, django_comment_client)
2. THE Configuration_Layer SHALL disable SSO providers in AUTHENTICATION_BACKENDS (remove social_auth backends for Google, Microsoft, SAML)
3. THE Configuration_Layer SHALL disable SCORM/xAPI features via FEATURES flags (ENABLE_SCORM: false, ENABLE_XAPI: false)
4. THE Configuration_Layer SHALL disable advanced analytics apps from INSTALLED_APPS (edx_analytics_dashboard integrations)
5. THE Configuration_Layer SHALL disable video conferencing plugins (Zoom LTI, Teams integration)
6. THE Configuration_Layer SHALL disable community features not in MVP (teams app if not used, wiki if not needed)
7. THE Configuration_Layer SHALL keep enabled: lms.djangoapps.certificates, lms.djangoapps.grades, lms.djangoapps.instructor, lms.djangoapps.courseware, openedx.core.djangoapps.user_api
8. THE Configuration_Layer SHALL keep enabled: bulk_email, course_groups (cohorts), enrollments
9. THE Configuration_Layer SHALL document in a DISABLED_FEATURES.md file which apps/features are disabled and rationale
10. THE Configuration_Layer SHALL document in a DISABLED_FEATURES.md file how to re-enable each feature for V2
11. WHEN disabling a feature, THE Configuration_Layer SHALL verify no MVP functionality depends on it via dependency analysis
12. THE Native_Setup SHALL provide a minimal INSTALLED_APPS list with only MVP-required apps

### Requirement 12: Observabilité et débogage

**User Story:** En tant qu'administrateur système, je veux des logs clairs et accessibles, afin de faciliter le débogage et le monitoring.

#### Acceptance Criteria

1. THE Service_Container SHALL log to stdout/stderr for Docker logs collection
2. THE Service_Container SHALL use structured logging format when possible
3. THE Native_Setup SHALL provide log aggregation via docker-compose logs command
4. THE Native_Setup SHALL configure appropriate log levels (INFO for production, DEBUG for development)
5. WHEN an error occurs, THE Service_Container SHALL log sufficient context for debugging
6. THE Native_Setup SHALL document how to access logs for each service
7. THE Native_Setup SHALL provide health check endpoints for LMS and CMS

### Requirement 13: Performance et optimisation

**User Story:** En tant qu'administrateur système, je veux une configuration optimisée pour les performances MVP, afin de garantir une expérience utilisateur fluide.

#### Acceptance Criteria

1. THE Native_Setup SHALL configure Redis caching for session and application cache
2. THE Native_Setup SHALL configure MySQL query cache and connection pooling
3. THE Native_Setup SHALL configure Caddy compression for static assets
4. THE Native_Setup SHALL configure appropriate resource limits for containers
5. THE Native_Setup SHALL use persistent connections between services when possible
6. WHEN serving media files, THE Native_Setup SHALL use Caddy for efficient static file serving
7. THE Native_Setup SHALL document performance tuning parameters

### Requirement 14: Documentation opérationnelle

**User Story:** En tant qu'administrateur système, je veux une documentation complète, afin de pouvoir déployer et maintenir la plateforme sans dépendance externe.

#### Acceptance Criteria

1. THE Native_Setup SHALL provide README with quick start instructions
2. THE Native_Setup SHALL document all environment variables and their purpose
3. THE Native_Setup SHALL document deployment procedures (dev, integration, production)
4. THE Native_Setup SHALL document backup and restore procedures
5. THE Native_Setup SHALL document common troubleshooting scenarios
6. THE Native_Setup SHALL document how to add/remove services
7. THE Native_Setup SHALL document how to scale services (multiple workers, read replicas)
8. THE Native_Setup SHALL provide architecture diagrams showing service interactions

### Requirement 15: Tests et validation

**User Story:** En tant que développeur, je veux valider que le setup natif fonctionne correctement, afin de garantir la qualité avant déploiement.

#### Acceptance Criteria

1. THE Native_Setup SHALL provide smoke tests for service connectivity
2. THE Native_Setup SHALL provide functional tests for critical MVP features
3. THE Native_Setup SHALL validate database migrations run successfully
4. THE Native_Setup SHALL validate static assets are served correctly
5. THE Native_Setup SHALL validate email sending works via Celery
6. THE Native_Setup SHALL validate certificate generation works
7. THE Native_Setup SHALL validate user authentication and authorization
8. WHEN running tests, THE Native_Setup SHALL use isolated test database
9. THE Native_Setup SHALL document how to run the test suite

