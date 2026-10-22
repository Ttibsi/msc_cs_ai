# Week 7 - Ethics

* Explain what privacy is and why privacy is important. [MLO 5]
* State a range of ways in which privacy can be violated. [MLO 5]
* Explain ethics in relation to Data Privacy. [MLO 5]
* Identify, address and document residual threats to validity for a given analysis. [MLO 5]

### Lesson 1 - Privacy and Data Validity
Data may only be collected for "a specific, explicity, and legitimate purpose" as per GDPR.
If the data already exists, we can't use it for a different purpose. That is illegal.
Quite often companies are vague about their purposes to get around this.

"Data privacy means empowering the data subjects to make their own decisions about who
can process their data and for what purposes." - GDPR
Data privacy is about control.

Concerns
- Discrimination over the information provided in use data
- ex religious/political beliefs and membership of a trade union
- medical history is also sensetive information.
- minor criminal offenses considered spent.

Data can be sold on, which is a concern.
Data can be used to build a profile of an individual that could be used
to discriminate.
Data may not be fully anonymised, or include so many unique elements in a data profile
that it's easy to identify someone even if information such as a person's name isn't
included.

Ethical concerns on Data Mining: (Witten book - 1.7)
* Reidentification
    * 85% of americans can be reidentified from only their ZIP code, birthdate, and sex.
    * over half can be identified by just city, birthdate, sex
    * moral is that if you remove _all_ PII, you won't be left with anything useful

* Using Personal Information
    * People should be informed in simple language how their data is going to be used
    * Ethically, how far can that usage be stretched?

* Wider Issues
    * Logical and Scientific standards must also be adhered to
    * caveats need to be applied to conclusions unless they can be backed up
    * How do you decide to use the data you're given
        * Ex in a supermarket, if you know two items usually sell well together,
            should you shelve them together or further apart, to encourage more
            purchases at the same time?
        * Should the more expensive items of those types be shelved together instead
        of cheaper alternatives to encourage higher profits?

GDPR
----
* General Data Protection Regulation
* Came into effect 2018
* Six guiding principles
    - Data is processd fairly, lawfully, and transparently
    - Collected and processed for specific reasons and stored for specific periods of time,
    and is not used beyond it's original collection purpose
    - Only the data neccesary for the purpose is collected and not more
    - Collected data is accurate and reasonable steps are taken to ensure it remains accurate
    - is kept in a form that allows individuals to be identified only as long as it is
    neccesary
    - it is kept securely and protected from unlawful access, accidental loss, or damage.
* GDPR also defines rights that individuals have to access and control their data
    - right to be informed
    - right of access
    - right to rectification
    - right to erasure/ right to be forgotten
    - right to restrict processing
    - right to data portability
    - right to object
    - rights in relation to automated decision making and profiling

### Lesson 2 - What Went Wrong?
Privacy by Design
    * Proactive not reactive, preventative not remedial
    * Privacy as the default setting
    * PRivacy embedded into design
    * Full functionality - positive-sum, not zero-sum
    * End-to-end securyt - full lifetime protection
    * Visibility and transparency - keep it open
    * Respect for user provacy - keep it user-centric

These are ISO standardised. Similar legislation in other countries, enforced as part of GDPR.
Generally considered positive _but_

Criticism:
* points are considered vague and leaving any open questions when designing software architecture
* No enforcement, these are voluntary (although this is now superceded by what is part of
GDPR law)

ML Test Score
* Research paper from google
* outlining 28 different assertions to apply to a ML algorithm.
* Primarily based around testing the data, not the code
* Should be used alongside standard software testing practices, not a replacement

GDPR Privacy rights
* Right to be informed
* Right of access
* Right to rectification
* Right to erasure
* Right to restrict processing
* Right to data portability
* Right to object
