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

