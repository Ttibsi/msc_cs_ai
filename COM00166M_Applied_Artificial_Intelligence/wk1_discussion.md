Turing test
The turing test has a number of limitations that have been discovered over the years, including at least two that Turing himself never realised. The computer may try to over-explain things that are implicitly obvious to humans, revealing that it has less understanding of who it's communicating with, and the Turing test encourages the machine to make mistakes, thus proving it's "humanity" and that it has less than perfect recall. 

MIT researcher LaCurtis tates that these kind of tests can be brute forced[1] by the compute power of the current day - as we now see with large language models - and that the test as it originally stands, proposed by Turing[2], does not consider intelligence a range, instead a binary option. For example, LaCurtis puts forward the difference in intelligence between a five year old and an adult.

State of AI
The advancements of the last year listed in the State of AI report 2025 predominantly are a combination of political and evolutionary, as opposed to revolutionary. China has cemented itself as in the lead with open models, whereas US companies have solidified their state as closed source. Sam Altman of OpenAI has recognised this, even stating that he doesn't want to be on the wrong side of history in this regard, although his companay are one of a handful of now-household names in the LLM sphere that are focussing on "American-first AI" - an initiative that I believe is driven (at least partially) by the state of politics in that country. I also think it's worth noting that the headline part of this presentation focusses primarily on LLMs (and their cousin's LRMs - Large Reasoning Models) without looking at other fields/applications of AI, which speaks to the direction that most research and investment is going toward.

Despite all this, there are still a number of fascinating sub-fields of AI that have caught my eye whilst reading through the report. 

How reasoning breaks - slides 22 and 23
* The research in this area shows that any extraneous detail fed into a prompt can stretch the reasoning of a Large Language Model in it's reasoning and execution/"thinking" time. 
* This is of relevance as it shows how prompts can be fragile, and points us toward prompt injection as an easy way for malicious actors to burn through AI resources. 
* Researchers can also use this discovery to point themselves towards new points of failure in LLMs and how they can evolve to be more efficient with the user input
* While we expect that modern LLMs have some form of user input validation to prevent malicious use, the legal and ethical implications predominantly stand out as to overt resource consumption and new potentials for "jailbreaking" to reveal new secrets or unethical content, harkening back to the early days of public LLM access.
* Reasoning in general appears to be one of the most publicly chased directions for LRM improvement, and research has found that chain of thought connections can help improve reasoning, but lower accurracy when trying to communicate in the same "language" as the user.

Safety by Design - slide 26
* AI usage and it's balance with safety is something that strikes me as fascinating, as new technology tends to take a while for the safety procedures to kick in ("Move fast and break things")
* The current approach builds safety-first into it's pretraining through a variety of approaches - moral education datasets, refusal criteria, harmfulness tags. All of which are decreasing the oppertunity to jailbreak a model
* The biggest issue with the current approach is the quality of the data fed in during pre-training. Sceptics suspect that unreviewed data will lead to biases in models. This is something we already see with photo processing AI, or face recognition AI having biases towards white male faces due to the training data fed in.
* There are also large quantities of data that we are aware of are used for training that ethically can't be held up to a level of quality due to the source. For example, Grok AI is an LLM trained on twitter/X, a platform infamous for hate speech (especially in recent years), politically driven statements, and a bad-faith approach to a conversation that needs a more nuanced take.
* Other ethical issues arise here with the collection of training data. While some companies are signing deals with the AI companies to provide better API access to their material -- most notably Wikipedia has done so in the last few days[3] -- a large number of websites are being hit hard by web scrapers and API requests to pull all the data out of them into the ever-growing training material.

REF:
[1]
K. LaCurts, “Criticisms of the Turing Test and Why You Should Ignore (Most of) Them,” MIT.

[2]
A. Turing, “Computing Machinery and Intelligence,” Mind, 1950.

[1]
Wikimedia Foundation, “Wikipedia celebrates 25 years of knowledge at its best – Wikimedia Foundation,” Wikimedia Foundation, Jan. 15, 2026. https://wikimediafoundation.org/news/2026/01/15/wikipedia-celebrates-25years/ (accessed Jan. 18, 2026).
