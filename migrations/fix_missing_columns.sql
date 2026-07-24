-- Falsky — Fix Missing Columns Migration
-- Run this in Supabase SQL Editor AFTER init.sql
-- These columns are referenced by engine code and RPC functions but were missing from init.sql

-- test_results: missing columns used by trust_engine.py
ALTER TABLE test_results ADD COLUMN IF NOT EXISTS score_confidence REAL DEFAULT 0;
ALTER TABLE test_results ADD COLUMN IF NOT EXISTS error_type VARCHAR(50);
ALTER TABLE test_results ADD COLUMN IF NOT EXISTS run_timestamp TIMESTAMPTZ DEFAULT NOW();

-- Rename 'timestamp' to be consistent — keep both for backward compat
-- (engine uses 'run_timestamp', init.sql used 'timestamp')

-- ci_runs: missing columns used by trust_engine.py
ALTER TABLE ci_runs ADD COLUMN IF NOT EXISTS skipped INTEGER DEFAULT 0;
ALTER TABLE ci_runs ADD COLUMN IF NOT EXISTS environment VARCHAR(255);

-- indexes for new columns
CREATE INDEX IF NOT EXISTS idx_test_results_confidence ON test_results(score_confidence);
CREATE INDEX IF NOT EXISTS idx_test_results_run_timestamp ON test_results(run_timestamp);
CREATE INDEX IF NOT EXISTS idx_ci_runs_environment ON ci_runs(environment);

SELECT 'Missing columns migration applied successfully!' as status;
