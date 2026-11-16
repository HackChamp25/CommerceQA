# Performance Testing – Locust

## Objective
Evaluate API performance under simulated concurrent users.

## Target API
Restful Booker API

## Tool
Locust

## Test Scenario
- Authenticate simulated users.
- Retrieve booking IDs.
- Retrieve individual booking details.
- Use weighted tasks to simulate different request frequencies.

## Test Configuration
- Simulated users: 2
- Spawn rate: 1 user/second
- Duration: 1 minute

## Acceptance Criteria
- Failure rate <= 1%
- P95 response time <= 1500 ms

## Results
- Failure rate: 0.00%
- P95 response time: 460 ms
- Overall result: PASSED

## Conclusion
The API met the defined performance acceptance criteria
during this test run.