-- ============================================
-- Création de la base de données pour les grades
-- ============================================

CREATE DATABASE grades;

\c grades;

-- ============================================
-- Table: Étudiants
-- ============================================
CREATE TABLE students (
    id SERIAL PRIMARY KEY,
    gitea_id INTEGER UNIQUE,
    prenom VARCHAR(100) NOT NULL,
    nom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    groupe VARCHAR(50) NOT NULL,
    gitea_username VARCHAR(100) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_groupe ON students(groupe);
CREATE INDEX idx_students_email ON students(email);

-- ============================================
-- Table: TDs (Assignments)
-- ============================================
CREATE TABLE assignments (
    id SERIAL PRIMARY KEY,
    code VARCHAR(50) UNIQUE NOT NULL,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    deadline TIMESTAMP,
    max_points INTEGER DEFAULT 100,
    repository_template VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_assignments_code ON assignments(code);

-- ============================================
-- Table: Soumissions (Submissions)
-- ============================================
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
    commit_hash VARCHAR(40) NOT NULL,
    branch VARCHAR(100) DEFAULT 'main',
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'pending', -- pending, running, completed, failed
    UNIQUE(student_id, assignment_id, commit_hash)
);

CREATE INDEX idx_submissions_student ON submissions(student_id);
CREATE INDEX idx_submissions_assignment ON submissions(assignment_id);
CREATE INDEX idx_submissions_status ON submissions(status);

-- ============================================
-- Table: Notes et résultats
-- ============================================
CREATE TABLE grades (
    id SERIAL PRIMARY KEY,
    submission_id INTEGER REFERENCES submissions(id) ON DELETE CASCADE,
    note DECIMAL(5,2) NOT NULL,
    max_points INTEGER DEFAULT 100,
    rapport_html TEXT,
    logs TEXT,
    duree_execution INTEGER, -- en secondes
    tests_passed INTEGER DEFAULT 0,
    tests_total INTEGER DEFAULT 0,
    graded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_grades_submission ON grades(submission_id);

-- ============================================
-- Table: Métriques d'activité
-- ============================================
CREATE TABLE activity_metrics (
    id SERIAL PRIMARY KEY,
    student_id INTEGER REFERENCES students(id) ON DELETE CASCADE,
    assignment_id INTEGER REFERENCES assignments(id) ON DELETE CASCADE,
    nb_commits INTEGER DEFAULT 0,
    nb_pushs INTEGER DEFAULT 0,
    nb_tentatives INTEGER DEFAULT 0,
    premier_push TIMESTAMP,
    dernier_push TIMESTAMP,
    temps_travail_estime INTEGER, -- en minutes
    UNIQUE(student_id, assignment_id)
);

CREATE INDEX idx_metrics_student ON activity_metrics(student_id);
CREATE INDEX idx_metrics_assignment ON activity_metrics(assignment_id);

-- ============================================
-- Table: Tests détaillés
-- ============================================
CREATE TABLE test_results (
    id SERIAL PRIMARY KEY,
    grade_id INTEGER REFERENCES grades(id) ON DELETE CASCADE,
    test_name VARCHAR(255) NOT NULL,
    test_category VARCHAR(100), -- ex: "Docker", "Networking", "Security"
    passed BOOLEAN NOT NULL,
    points DECIMAL(5,2) DEFAULT 0,
    message TEXT,
    execution_time INTEGER, -- en millisecondes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_test_results_grade ON test_results(grade_id);

-- ============================================
-- Vue: Résumé des notes par étudiant
-- ============================================
CREATE VIEW student_grades_summary AS
SELECT 
    s.id as student_id,
    s.prenom,
    s.nom,
    s.email,
    s.groupe,
    a.code as assignment_code,
    a.nom as assignment_nom,
    MAX(g.note) as meilleure_note,
    AVG(g.note) as note_moyenne,
    COUNT(sub.id) as nb_tentatives,
    MAX(sub.submitted_at) as derniere_soumission,
    MAX(g.tests_passed) as tests_reussis,
    MAX(g.tests_total) as tests_total
FROM students s
LEFT JOIN submissions sub ON s.id = sub.student_id
LEFT JOIN assignments a ON sub.assignment_id = a.id
LEFT JOIN grades g ON sub.id = g.submission_id
GROUP BY s.id, s.prenom, s.nom, s.email, s.groupe, a.code, a.nom;

-- ============================================
-- Vue: Statistiques par groupe
-- ============================================
CREATE VIEW group_statistics AS
SELECT 
    s.groupe,
    a.code as assignment_code,
    COUNT(DISTINCT s.id) as nb_etudiants,
    COUNT(DISTINCT sub.student_id) as nb_etudiants_ayant_soumis,
    AVG(CASE WHEN g.note IS NOT NULL THEN g.note ELSE 0 END) as note_moyenne,
    MAX(g.note) as note_max,
    MIN(g.note) as note_min,
    COUNT(sub.id) as nb_soumissions_total
FROM students s
CROSS JOIN assignments a
LEFT JOIN submissions sub ON s.id = sub.student_id AND a.id = sub.assignment_id
LEFT JOIN grades g ON sub.id = g.submission_id
GROUP BY s.groupe, a.code;

-- ============================================
-- Fonction: Mise à jour des métriques
-- ============================================
CREATE OR REPLACE FUNCTION update_activity_metrics()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO activity_metrics (student_id, assignment_id, nb_tentatives, nb_pushs, dernier_push, premier_push)
    VALUES (NEW.student_id, NEW.assignment_id, 1, 1, NEW.submitted_at, NEW.submitted_at)
    ON CONFLICT (student_id, assignment_id) 
    DO UPDATE SET
        nb_tentatives = activity_metrics.nb_tentatives + 1,
        nb_pushs = activity_metrics.nb_pushs + 1,
        dernier_push = NEW.submitted_at;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_metrics
AFTER INSERT ON submissions
FOR EACH ROW
EXECUTE FUNCTION update_activity_metrics();

-- ============================================
-- Données de test (optionnel)
-- ============================================
INSERT INTO assignments (code, nom, description, max_points) VALUES
    ('TD1', 'Introduction à Docker', 'Création d''un premier conteneur Docker', 100),
    ('TD2', 'Docker Compose', 'Application multi-conteneurs', 100),
    ('TD3', 'Réseaux Docker', 'Configuration réseau avancée', 100);

-- ============================================
-- Permissions
-- ============================================
GRANT ALL PRIVILEGES ON DATABASE grades TO gitea;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO gitea;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO gitea;