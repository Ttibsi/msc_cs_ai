# Notes

Data Cleaning
- if `age_of_casualty` is `-1`, remove row
    - There's a large enough dataset that we can afford to lose these entries and still
    have a large enough dataset to work with
    - Note that we're not explicitly doing the same for `age_band` as it will be
    reflected in the same action
- if `enhanced_casualty_severity` is -1, remove row
    - value is not yet, unknown how big the damage was

Casualty Severity Investigation
 - it appears that we can use Naive Bayes here a few times to group together different
    factors to check for question 1 - WRT identifying three variables
