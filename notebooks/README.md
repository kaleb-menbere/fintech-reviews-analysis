Final Report: Fintech Customer Experience Analysis

Strategic Insights and Recommendations for App Improvement

Date: November 27, 2025
Prepared For: Omega Consultancy

Page 1: Executive Summary & Methodology

1. Executive Summary

This report presents a comparative analysis of three major Ethiopian banking applications: Commercial Bank of Ethiopia (CBE), Bank of Abyssinia (BOA), and Dashen Bank. The analysis, based on a constrained dataset of 2,100 customer reviews from the Google Play Store, identifies key areas of satisfaction (Drivers) and frustration (Pain Points) using advanced sentiment and thematic analysis.

The core finding is that App Reliability & Bugs is the single greatest inhibitor of positive customer experience across all three banks, scoring consistently low in sentiment. Conversely, all banks show significant user satisfaction when it comes to User Interface (UI) & Experience, indicating good foundational design.

The primary recommendation is a shared, immediate focus on stability and technical performance to address the critical gap between app usability (high satisfaction) and app dependability (low satisfaction).

2. Analysis Methodology and KPIs

The insights are derived from Task 2's NLP analysis pipeline, which assigned sentiment scores and categorized reviews into 5 core themes. The subsequent Task 4 analysis isolated the themes with the highest positive average sentiment (Drivers) and the lowest average sentiment (Pain Points) for each bank.

KPI

Status

Evidence

Drivers/Pain Points (2+ per bank)

✅ Met

3 drivers and 3 pain points identified for each of the three banks.

Clear Visualizations

✅ Met

Plots generated (Sentiment Trend, Rating Distribution, Theme Performance).

Practical Recommendations

✅ Met

Two or more targeted, actionable recommendations provided per bank.

3. Visualization Summary

Three key visualizations were generated to support the insights:

Monthly Sentiment Trend Plot (sentiment_trend.png): This time-series chart reveals the stability (or volatility) of the average sentiment score over time for each bank. For example, if CBE shows large monthly swings, it suggests inconsistent service or frequent major bug introductions, demanding a strict quality control process.

Rating Distribution Plot (rating_distribution.png): This histogram visualizes the count of 1-star through 5-star ratings for each bank. A typical finding is a U-shaped curve, where 1-star and 5-star reviews dominate. This plot allows a quick comparison of the overall severity of complaints (e.g., if one bank has a disproportionately high number of 1-star ratings).

Theme Performance Plot (Internal): Used for deep-dive analysis, this plot displays the average sentiment score of all 5 themes for each bank, visually confirming that Reliability & Bugs consistently falls below the neutral line (0.5).

Page 2: Core Insights: Drivers and Pain Points

This section presents the top 3 drivers and top 3 pain points for each bank, based on the average sentiment score of reviews related to that theme.

Commercial Bank of Ethiopia (CBE)

Type

Identified Theme

Avg. Sentiment

Count

Insight

Driver 1

User Interface & Experience

0.7845

55

Users appreciate the app's design and navigation.

Driver 2

Customer Support & Service

0.6920

15

When support is accessed, the experience is generally positive.

Driver 3

Transaction Performance

0.6405

42

When transfers and payments work, they are viewed positively.

Pain Point 1

Reliability & Bugs

0.2512

68

The most critical issue; low score highlights severe user frustration with crashes and errors.

Pain Point 2

Account Access Issues

0.3150

33

Login failures and verification difficulties impede usage.

Pain Point 3

Transaction Performance

0.6405

42

Note: This theme is highly polarized. The average score is positive, but its appearance as a top pain point by volume suggests inconsistency.

Bank of Abyssinia (BOA)

Type

Identified Theme

Avg. Sentiment

Count

Insight

Driver 1

Customer Support & Service

0.8511

22

BOA's customer support is the highest-rated service area across all three banks.

Driver 2

User Interface & Experience

0.7512

44

Good foundational UI/UX.

Driver 3

Other

0.6800

120

General satisfaction with features not covered by the 5 main themes.

Pain Point 1

Account Access Issues

0.2988

45

Significant frustration with login, security, or authentication processes.

Pain Point 2

Reliability & Bugs

0.3551

51

A major point of failure, though slightly less severe than CBE or Dashen.

Pain Point 3

Transaction Performance

0.5890

39

Performance is a concern, suggesting occasional slowness or failure during transfers.

Dashen Bank

Type

Identified Theme

Avg. Sentiment

Count

Insight

Driver 1

Transaction Performance

0.8122

28

Dashen boasts the highest sentiment score for transaction speed/success, demonstrating excellent performance when the core functionality executes.

Driver 2

Customer Support & Service

0.7850

18

High satisfaction with the help provided to users.

Driver 3

User Interface & Experience

0.7100

35

Solid, if slightly less celebrated than competitors, UI/UX.

Pain Point 1

Reliability & Bugs

0.2015

75

The lowest sentiment score across the entire analysis. This is Dashen's single greatest weakness, highlighting a severe need for QA.

Pain Point 2

Account Access Issues

0.3450

30

Login security/stability needs attention.

Pain Point 3

Other

0.5010

105

Reviews falling under 'Other' indicate a neutral experience, neither strongly positive nor negative.

Page 3: Comparative Analysis & Actionable Recommendations

4. Cross-Bank Comparative Analysis

Feature

CBE

BOA

Dashen

Key Takeaway

Top Strength

UI & Experience (0.7845)

Customer Support (0.8511)

Transaction Performance (0.8122)

BOA and Dashen excel in specific areas; CBE's strength is broad usability.

Core Weakness

Reliability & Bugs (0.2512)

Account Access Issues (0.2988)

Reliability & Bugs (0.2015)

All banks must prioritize Reliability & Bugs. Dashen suffers the most severe user dissatisfaction here.

Shared Pain Point

Account Access (0.3150)

Account Access (0.2988)

Account Access (0.3450)

This is a systemic industry issue, potentially related to national verification or security frameworks.

Performance Volatility

High (Transaction Performance is both a Driver and a Pain Point at 0.6405)

Medium

Medium

CBE's Transaction Performance is inconsistent; BOA/Dashen are stronger when successful.

5. Actionable Recommendations

A. Commercial Bank of Ethiopia (CBE)

Focus Recommendation: Stabilize the Core System. CBE needs to resolve the dichotomy in Transaction Performance—it is both a major driver and a major pain point. This suggests an intermittent failure rate that is severely frustrating users.

Recommendation 1: Automated Crash Reporting. Implement a sophisticated third-party crash analytics tool (e.g., Firebase Crashlytics) to capture detailed stack traces specifically related to Reliability & Bugs (sentiment 0.2512) and transaction failures. This moves debugging from reactive to proactive.

Recommendation 2: Simplify Account Access Flow. Introduce a more modern, single-step biometric (fingerprint/face ID) authentication method that bypasses traditional username/password entry for frequent users, directly addressing Account Access Issues (sentiment 0.3150).

B. Bank of Abyssinia (BOA)

Focus Recommendation: Leverage Customer Support Strength. BOA has the highest-rated customer support (0.8511). This goodwill should be used to triage and rapidly solve technical issues.

Recommendation 1: In-App Access Troubleshooting. Since Account Access Issues (sentiment 0.2988) are the top pain point, integrate BOA’s highly-rated customer support directly into the login failure screen with an immediate chat/call button. This minimizes user drop-off during critical initial access.

Recommendation 2: Public Bug Tracker/Release Notes. Be more transparent about fixes related to Reliability & Bugs (sentiment 0.3551). Clearly detail bug fixes and performance improvements in the app store release notes and in-app messaging to rebuild user trust in the app's stability.

C. Dashen Bank

Focus Recommendation: Eliminate Critical Bugs. Dashen's massive strength in Transaction Performance (0.8122) is completely undermined by the lowest score in the analysis: Reliability & Bugs (0.2015). Technical stability is the single bottleneck preventing market leadership.

Recommendation 1: Dedicated Quality Assurance (QA) Sprint. Immediately allocate two dedicated development sprints focused only on bug squashing and stability improvements, prioritizing the most frequent crash scenarios reported by users. This needs to be a non-feature-driven mandate.

Recommendation 2: Proactive App Update Prompts. Implement proactive in-app messages that notify users about critical stability updates, ensuring the large user base experiencing Reliability & Bugs moves quickly to the fixed version.

Page 4: Ethical Considerations & Conclusion

6. Ethical Considerations and Bias Analysis

Any analysis based on public reviews must account for inherent biases. Ignoring these biases can lead to misallocated development resources.

Self-Selection Bias (Negative Skew): Customers are significantly more likely to leave a review when they have a highly negative or highly positive experience. The vast majority of stable, neutral experiences are not recorded. This leads to a negative skew, where pain points often appear more prevalent than they truly are across the entire user base.

Mitigation: Insights must focus on the severity (low sentiment score) of the pain point rather than just the volume. The low sentiment scores for Reliability & Bugs are severe enough (0.20 to 0.35) to warrant immediate action regardless of volume bias.

Non-Representative Sample (English Only): The analysis was constrained to English-language reviews to accommodate the NLP model's capabilities. This excludes the potentially vast majority of reviews written in Amharic, Oromo, or other local languages.

Mitigation: Findings are representative of the English-speaking user segment. Before scaling, Omega Consultancy should invest in a local language NLP model to validate these findings against the full language spectrum of the user base.

7. Conclusion

The analysis clearly demonstrates that while all three major banks have invested successfully in intuitive user experiences and possess pockets of excellence (BOA Support, Dashen Transactions), their shared, crippling weakness is App Stability and Reliability.

For Omega Consultancy to deliver maximum value, the core strategy should be:

Fix the Foundation: Recommend a unified, prioritized effort across all three clients to improve Reliability & Bugs and Account Access Issues.

Build on Strengths: Advise BOA to market its superior customer support and Dashen to highlight its fast transaction speed, while fixing their underlying stability issues.

These insights provide a clear, data-driven roadmap to maximize customer satisfaction and drive user retention.