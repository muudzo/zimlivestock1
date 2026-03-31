-- Commit 6: Database Indexing Migration
-- Optimizes performance for high-traffic queries.

-- 1. Optimization for Bid History and Highest Bid Lookup
-- Standard index on livestock_id for filtering, and amount for sorting.
CREATE INDEX IF NOT EXISTS idx_bids_livestock_amount ON bids (livestock_id, amount DESC);

-- 2. Optimization for Webhook Lookups (Scalability)
-- Payment status updates are frequent and look up by merchant_reference.
CREATE UNIQUE INDEX IF NOT EXISTS idx_payments_merchant_reference ON payments (merchant_reference);

-- 3. Optimization for User History (Scalability)
CREATE INDEX IF NOT EXISTS idx_payments_payer_id ON payments (payer_id);

-- 4. Optimization for Livestock Listings
-- Filtering by category is a primary user action.
CREATE INDEX IF NOT EXISTS idx_livestock_category ON livestock_items (category);
-- Filtering for seller's own items.
CREATE INDEX IF NOT EXISTS idx_livestock_seller_id ON livestock_items (seller_id);

-- 5. Optimization for Idempotency Checks (Commit 3 & 5)
CREATE INDEX IF NOT EXISTS idx_livestock_idempotency ON livestock_items (seller_id, idempotency_key) WHERE idempotency_key IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_payments_idempotency ON payments (idempotency_key) WHERE idempotency_key IS NOT NULL;
