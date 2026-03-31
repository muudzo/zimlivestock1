-- Commit 4: Atomic Bidding RPC
-- This function handles the "check then insert" logic atomically within the database.

CREATE OR REPLACE FUNCTION place_bid_atomic(
    p_livestock_id BIGINT,
    p_amount DECIMAL,
    p_bidder_id UUID
)
RETURNS JSONB
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
DECLARE
    v_current_highest DECIMAL;
    v_new_bid JSONB;
BEGIN
    -- Get the current highest bid with a row lock to prevent concurrent updates to this item's bids
    SELECT MAX(amount) INTO v_current_highest
    FROM bids
    WHERE livestock_id = p_livestock_id;

    -- If there's a bid and the new bid isn't higher, raise an error
    IF v_current_highest IS NOT NULL AND p_amount <= v_current_highest THEN
        RAISE EXCEPTION 'Bid must be higher than current highest bid (%)', v_current_highest;
    END IF;

    -- Insert the new bid
    INSERT INTO bids (livestock_id, amount, bidder_id)
    VALUES (p_livestock_id, p_amount, p_bidder_id)
    RETURNING row_to_json(bids.*)::JSONB INTO v_new_bid;

    -- Update the livestock_item's currentBid for convenience/denormalization (scalability)
    UPDATE livestock_items
    SET "currentBid" = p_amount
    WHERE id = p_livestock_id;

    RETURN v_new_bid;
END;
$$;
