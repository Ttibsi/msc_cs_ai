# Week 1:  Introduction to Big Data

Why you might want to ask questions of data
How a good process can help achieve valid answers to your questions
how to structure data to make analysis practical and possible

### Lesson 1

Valuable research questions are Relevant, Original, Feasable, Interest (personal and academic interest)
Research questions:
    * must be phrased as a question - often missed/phrased as a claim
    * Needs to be specific, not vague. Will clarify what research should target
    * Must be complete, or use comparison
    * Should be narrow enough to research within the time and a practical investigation
        * feasability

Refine and revise your questions iteratively until it's appropriate for research

Big data is often defined by the three Vs:
* Volume
* Variety
* Velocity (how fast it's all collected)

### Lesson 2  - Describing a reasonable data science process
1 - Set your research goal
    - Research questions implied in the provided text:
    * Does a country's population affect it's economic output?
    * Which country is most "typical" when it comes to economic output

2 - Data Acquisition
3 - Clean the data
    - Check it for things that are obviously wrong and try to fix them
        - Missing values
        - This that should be numbers but are actually text
        - Stray punctuation
        - Implausable values

4 - Analysis
    - quantitative analysis, produce some numbers that answer your question
    - According to wikipedia, only 5 of the top 10 countries by GDP are in
    the top 10 countries by population count, with another 2 coming in the
    top 20 by population

5 - Evaluate results
    - Do your results give you answers to base business decisions on
6 - Present your results
7 - Review

CRISP-DM - widely used methodology for data minining projects
"Cross Industry Standard Process for Data Mining"
6 phases:

- Business Understanding
- Data Understanding
- Data Prep/cleaning
- Modelling
- Evaluating
- Deployment

Data privacy
* Is about control - who is collecting it and what are you agreeing for them to collect
* Privacy = who has access and how it's collected
* Security = Proctecting data from unauthorised access,breaches, attacks
* Common privacy risks:
    - Identity theft
    - Tracking and surveillance
    - Phishing
* GDPR is the EU protection laws
*

### Lesson 3
Data comes in a wide variety of forms, each having its own characteristics, advantages
and challenges.

* Concept - The class or category we're interested in
* Concept description - A thing that is to be learned
* Instance - An example of a concept, a single datum
* Attribute - instances are characterised by their values on a predefined set of attibutes/features.
    - Attributes can depend on other attributes, ex spouse name depends on isMarried

Nominal attributes - discrete strings with no explicit relation
    - ex weather = sunny, overcast, rainy
Ordinal attributes - orderable, but with no notion of distance
    - ex hot, mild, cool
Interval attributes - values measured in fixed, equal units
    ex temperature in celcius
Ratio attributes - a value with a defined zero point
    - ex distance from a location
