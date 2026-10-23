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

### Lesson 3 - Identify the remaining threats to validity
Why is validity an ethical issue?
    - Because incorrect or invalud data can lead to assumptions that can harm people
    - EX loan applications, spam detection, clinical trials
    - Could lead to systemic bias

Internal validity - do your results flow from your data
External validity - Do your results generalise beyond your current data
Construct validity - Do the concepts that you use to describe your investigation ("life satisfaction")
                    map well to the data you're using.

### Task 1 - Threat Mitigation

In the paper "An Empirical Study of Bugs in Machine Learning Systems", the researchers study how
internal validity is mitigated across three large-scale open source softwares by investigating
a random selection of closed bugs in their issue trackers. Their investigation showed the number of
bugs across all three projects in different categories, but did not explain how the maintainers
of each project attempted mitigation. Here, the suggestion would be to ensure the projects lean
on software development standard testing approaches, such as rigorous unit and integration testing,
as well as "dogfooding", the process of using your own software, so as to experience buggy
behaviour themselves.

In the study claiming phones are harmful, we see a textbook example of Construct Validity, the
validity threat that has the researcher asking if the data they've collected accurately reflects
the hypothesis they're trying to research. The current researchers mitigated this issue by
relying on software-related phone usage tracking instead of user-submitted data, which is often
inaccurate due to human nature. However, they could have taken this further by relying on custom
software that takes more accurate and granular readings, which would provide the researchers with
more data to work with, such as the age and sex of the user, as well as the time of day that
subjects are using their phones and how the purpose of phone usage changes throughout the day.

