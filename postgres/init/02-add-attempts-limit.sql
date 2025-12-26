-- ============================================
-- Ajout de la limitation à 5 tentatives par TD
-- ============================================

\c grades;

-- Ajouter une colonne pour compter les tentatives
ALTER TABLE activity_metrics ADD COLUMN IF NOT EXISTS max_attempts INTEGER DEFAULT 5;

-- Fonction pour vérifier le nombre de tentatives
CREATE OR REPLACE FUNCTION check_attempts_limit()
RETURNS TRIGGER AS $$
DECLARE
    attempt_count INTEGER;
    max_attempts_allowed INTEGER := 5;
BEGIN
    -- Compter les tentatives pour cet étudiant et ce TD
    SELECT COUNT(*) INTO attempt_count
    FROM submissions
    WHERE student_id = NEW.student_id 
    AND assignment_id = NEW.assignment_id;
    
    -- Si le nombre de tentatives dépasse la limite
    IF attempt_count >= max_attempts_allowed THEN
        RAISE EXCEPTION 'Maximum attempts reached: % of % attempts used for this assignment', 
            attempt_count, max_attempts_allowed;
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger pour vérifier avant insertion
DROP TRIGGER IF EXISTS trigger_check_attempts ON submissions;
CREATE TRIGGER trigger_check_attempts
BEFORE INSERT ON submissions
FOR EACH ROW
EXECUTE FUNCTION check_attempts_limit();

-- Vue pour voir les tentatives restantes par étudiant et TD
CREATE OR REPLACE VIEW student_attempts_summary AS
SELECT 
    s.id as student_id,
    s.prenom,
    s.nom,
    s.email,
    a.id as assignment_id,
    a.code as assignment_code,
    COUNT(sub.id) as attempts_used,
    5 - COUNT(sub.id) as attempts_remaining,
    CASE 
        WHEN COUNT(sub.id) >= 5 THEN true 
        ELSE false 
    END as max_attempts_reached
FROM students s
CROSS JOIN assignments a
LEFT JOIN submissions sub ON s.id = sub.student_id AND a.id = sub.assignment_id
GROUP BY s.id, s.prenom, s.nom, s.email, a.id, a.code;

-- Fonction pour obtenir le nombre de tentatives restantes
CREATE OR REPLACE FUNCTION get_remaining_attempts(p_student_id INTEGER, p_assignment_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    used_attempts INTEGER;
BEGIN
    SELECT COUNT(*) INTO used_attempts
    FROM submissions
    WHERE student_id = p_student_id 
    AND assignment_id = p_assignment_id;
    
    RETURN 5 - used_attempts;
END;
$$ LANGUAGE plpgsql;

-- Index pour optimiser les requêtes de comptage
CREATE INDEX IF NOT EXISTS idx_submissions_student_assignment 
ON submissions(student_id, assignment_id);

-- Commentaires
COMMENT ON FUNCTION check_attempts_limit() IS 'Vérifie que l étudiant n a pas dépassé 5 tentatives pour un TD';
COMMENT ON FUNCTION get_remaining_attempts(INTEGER, INTEGER) IS 'Retourne le nombre de tentatives restantes pour un étudiant et un TD';
COMMENT ON VIEW student_attempts_summary IS 'Vue résumant les tentatives utilisées et restantes par étudiant et TD';