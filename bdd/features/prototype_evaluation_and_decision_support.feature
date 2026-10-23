Feature: Prototype evaluation and decision support

  @REQ-012 @must
  Scenario: SCN-018 Process a ticket through the minimal interface
    Given the Phase 1 CLI or web page is running
    When an agent submits a ticket
    Then the interface displays the structured classification, draft or abstention, citations, and review decision

  @REQ-013 @must
  Scenario: SCN-019 Report evaluation results
    Given a labeled evaluation set contains normal, gap, conflict, and safety cases
    When a configuration is evaluated
    Then the report includes classification, safety, grounding, citation, review-rate, latency, and cost measurements

  @REQ-014 @must
  Scenario: SCN-020 Compare operating configurations at target volume
    Given measured configuration results and explicit staffing and cost assumptions
    When the one-page business case is generated
    Then it estimates monthly cost and benefit at 10,000 tickets
    And it identifies the recommended configuration or states that none is justified

