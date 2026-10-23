Feature: Ticket intake and classification

  @REQ-001 @must
  Scenario: SCN-001 Preserve the ticket identity
    Given a ticket has an identifier and text
    When the co-pilot processes it
    Then the result contains the same ticket identifier

  @REQ-002 @must
  Scenario: SCN-002 Classify a supported topic
    Given a ticket asks how to withdraw funds
    When it is classified
    Then the category is "withdrawal"

  @REQ-002 @must
  Scenario: SCN-003 Preserve an unsupported topic
    Given a ticket does not match deposit, withdrawal, account opening, or verification
    When it is classified
    Then the category is "other" or "unknown"
    And the category is not forced into a supported topic

  @REQ-003 @must
  Scenario: SCN-004 Return all required classifications
    Given a ticket is written in a detectable language and expresses frustration
    When it is classified
    Then category, urgency, language, and sentiment are all present

  @REQ-018 @must
  Scenario: SCN-026 Route an unsupported language
    Given a valid ticket is written in a language unsupported by the active configuration
    When the ticket is processed
    Then the co-pilot does not fabricate a classification or draft
    And human review is required with reason "unsupported_language"

  @REQ-018 @must
  Scenario: SCN-027 Reject invalid ticket input
    Given a ticket has a missing identifier or empty text
    When the ticket is submitted
    Then a typed validation error is returned
    And no retrieval or provider call is attempted

