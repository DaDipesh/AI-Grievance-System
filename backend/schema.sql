-- Reference schema for PostgreSQL. The application startup migration also upgrades older SQLite/PostgreSQL databases.

CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY, mobile VARCHAR(16) NOT NULL UNIQUE, password_hash VARCHAR(255), role VARCHAR(16) NOT NULL DEFAULT 'citizen',
    department VARCHAR(120), preferred_language VARCHAR(12) NOT NULL DEFAULT 'en', name VARCHAR(120),
    gender VARCHAR(20), email VARCHAR(254), city VARCHAR(120), state VARCHAR(120), district VARCHAR(120), village VARCHAR(120),
    pincode VARCHAR(12), address VARCHAR(500), latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, profile_photo_data TEXT,
    profile_complete BOOLEAN NOT NULL DEFAULT FALSE, active BOOLEAN NOT NULL DEFAULT TRUE, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS complaints (
    id SERIAL PRIMARY KEY, ticket_number VARCHAR(32) NOT NULL UNIQUE, citizen_id INTEGER NOT NULL REFERENCES users(id), complaint_text TEXT NOT NULL,
    category_predicted VARCHAR(80), category_verified VARCHAR(120), category_source VARCHAR(32), ml_confidence DOUBLE PRECISION,
    severity VARCHAR(32), priority VARCHAR(32), department VARCHAR(120), team VARCHAR(120), routing_status VARCHAR(32),
    city VARCHAR(120), district VARCHAR(120), area VARCHAR(120), state VARCHAR(120), latitude DOUBLE PRECISION, longitude DOUBLE PRECISION, location_source VARCHAR(20),
    language VARCHAR(12), estimated_resolution_hours DOUBLE PRECISION, estimated_resolution_days DOUBLE PRECISION, evidence_path VARCHAR(500),
    duplicate_flag BOOLEAN NOT NULL DEFAULT FALSE, duplicate_similarity DOUBLE PRECISION, duplicate_existing_id VARCHAR(120),
    assigned_department VARCHAR(120), assigned_officer_id INTEGER REFERENCES users(id), status VARCHAR(32) NOT NULL DEFAULT 'pending',
    status_note VARCHAR(1000), resolution_hours_actual DOUBLE PRECISION, resolved_at TIMESTAMPTZ, sla_due_at TIMESTAMPTZ,
    escalated_at TIMESTAMPTZ, escalation_level INTEGER NOT NULL DEFAULT 0, updated_at TIMESTAMPTZ NOT NULL DEFAULT now(), created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS complaint_status_history (
    id SERIAL PRIMARY KEY, complaint_id INTEGER NOT NULL REFERENCES complaints(id) ON DELETE CASCADE, old_status VARCHAR(32),
    new_status VARCHAR(32) NOT NULL, note VARCHAR(1000), changed_by_user_id INTEGER REFERENCES users(id), created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE, complaint_id INTEGER REFERENCES complaints(id) ON DELETE SET NULL,
    title VARCHAR(200) NOT NULL, message VARCHAR(1000) NOT NULL, is_read BOOLEAN NOT NULL DEFAULT FALSE, created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY, complaint_id INTEGER NOT NULL UNIQUE REFERENCES complaints(id) ON DELETE CASCADE, citizen_id INTEGER NOT NULL REFERENCES users(id),
    rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5), comment VARCHAR(1000), created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
