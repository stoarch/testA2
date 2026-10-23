Feature: Human review, conflicts, and failures

  @REQ-009 @must
  Scenario: SCN-014 Route an abstention
    Given the co-pilot cannot support a complete answer from approved sources
    When it abstains
    Then human_review_required is true
    And the route reason includes "insufficient_knowledge"

  @REQ-009 @must
  Scenario: SCN-015 Route a configured low-confidence result
    Given classification or grounding confidence is below the configured threshold
    When the result is finalized
    Then human_review_required is true
    And the configured threshold is recorded with the result

  @REQ-010 @must
  Scenario: SCN-016 Produce auditable output
    Given a ticket completes processing
    When the structured result is returned
    Then it includes classifications, answer status, citations, safety flags, review reasons, configuration ID, latency, and usage data when available

  @REQ-011 @must
  Scenario: SCN-017 Do not reconcile conflicting source language silently
    Given approved pages provide conflicting or misleading wording for the requested detail
    When that detail is needed in a draft
    Then the co-pilot abstains from the disputed claim
    And it exposes the relevant sources
    And human review is required with reason "source_conflict"

  @REQ-016 @must
  Scenario: SCN-021 Fail safely when retrieval is unavailable
    Given the retrieval dependency fails
    When a ticket is processed
    Then no customer answer is drafted from model memory
    And a typed error result requires human review

