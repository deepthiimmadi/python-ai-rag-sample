# Synthetic API design notes

Keep APIs thin and versioned. Validate input at the edge, return consistent
errors, and keep state transitions explicit so they can be audited later.
