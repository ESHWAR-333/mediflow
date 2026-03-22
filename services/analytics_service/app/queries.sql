-- Connect:
-- docker exec -it mediflow-timescaledb psql -U mediflow -d mediflow_analytics


-- All events (latest first)
SELECT time, event_type, source, booking_id, urgency_score
FROM analytics_events
ORDER BY time DESC
LIMIT 20;


-- Bookings per hour (last 24 hours)
SELECT
    time_bucket('1 hour', time) AS hour,
    COUNT(*) AS total_bookings
FROM analytics_events
WHERE event_type = 'booking.created'
  AND time > NOW() - INTERVAL '24 hours'
GROUP BY hour
ORDER BY hour DESC;


-- Average urgency score per doctor
SELECT
    doctor_id,
    ROUND(AVG(urgency_score), 2) AS avg_urgency,
    COUNT(*) AS total_bookings,
    MAX(urgency_score) AS max_urgency
FROM analytics_events
WHERE event_type = 'triage.scored'
  AND doctor_id IS NOT NULL
GROUP BY doctor_id
ORDER BY avg_urgency DESC;


-- Critical bookings (urgency = 5) in last 1 hour
SELECT time, booking_id, patient_id, doctor_id
FROM analytics_events
WHERE urgency_score = 5
  AND time > NOW() - INTERVAL '1 hour'
ORDER BY time DESC;


-- Event volume by type (last 24 hours)
SELECT
    event_type,
    COUNT(*) AS count
FROM analytics_events
WHERE time > NOW() - INTERVAL '24 hours'
GROUP BY event_type
ORDER BY count DESC;


-- End-to-end pipeline duration per booking
-- (time from booking.created to slot.updated)
SELECT
    a.booking_id,
    MIN(a.time) AS booking_time,
    MAX(b.time) AS slot_confirmed_time,
    EXTRACT(EPOCH FROM (MAX(b.time) - MIN(a.time))) AS duration_seconds
FROM analytics_events a
JOIN analytics_events b ON a.booking_id = b.booking_id
WHERE a.event_type = 'booking.created'
  AND b.event_type = 'slot.updated'
GROUP BY a.booking_id
ORDER BY booking_time DESC;