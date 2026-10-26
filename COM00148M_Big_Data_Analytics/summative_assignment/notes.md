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


----
Q2 writeup on scaling
https://sqlite.org/faq.html#q5 - Can multiple applications or multiple instances of the same application access a single database file at the same time
(yes)

https://sqlite.org/wal.html
Atomic writes. SQLIte is also threadsafe to implement multiple logic at once

Otherwise, convert to mysql, you can `.dump` the schema and with minimal tweaks import it.
Adding new columns and tables is feasable.
https://sqlite.org/lang_altertable.html

SQLite is also pretty easy to "script" as you can use python to manipulate a sqlite db.
DB updates only happen on a yearly cadence, so analysts can each have their own copy to query, treating it as read-only
    - this can be enforced in python scripts to only open in RO mode
    - https://docs.python.org/3/library/sqlite3.html#how-to-work-with-sqlite-uris
    (see the first code snippet under this link - use this as reference in essay)
    - ref 2: https://www.sqlite.org/uri.html

---
# Part 3
* Public access to casualty data visualisation
    * Concern: Reidentification via a combination of semi-unique values, such as time/location of
        crash and vehicle details
    * Strategies: Ensure only data that is required is collected and verify anonymity processes.
        For public data visualisation, minimise access to individual data points
    * Data protection principles: Anonymisation, consent to use data for public visualisation 
        (GDPR right to refuse processing)

* Collection and storage of user-provided personal data
    * Concern: Users may be concerned about the purposes of the specific data being collected and may choose to opt out
    * Strategies: Should be simple to opt out, potentially via web form. User data can be easily removed from the database
        Purpose of data should be clearly communicated to individuals
    * Data protection principles: Right to Object (GDPR), Right to erasure (GDPR), data minimalisation

* Use of analytics and predictive modelling for personalised insights
    * Concern: Lack of accurate training for minorities, or unconcious bias included in training data
    * Strategies: Ensure that training data comes from a variety of sources, ensure user testing and testing data 
        also includes data from minorities.
    * Data protection principles: Communication of data usage purposes

Useful links
* https://www.gov.uk/government/publications/policy-on-protecting-personal-and-other-sensitive-information-in-fire-and-rescue-incident-and-casualty-data
* https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/
* https://ones.com/blog/navigating-ethical-minefield-risks-predictive-analytics/
