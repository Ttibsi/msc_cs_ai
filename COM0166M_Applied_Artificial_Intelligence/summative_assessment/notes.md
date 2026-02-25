1a - Look at what data I have and figure out what I can do with it
    - decide on a type of learning algorithm to use and what my goal is
1b - Also do some research into papers to write about later
    - Can I influence my artifact based on others paper topics as well
2 - Setup paper cover sheet and ToC. No identifying information
    - See section IV  - Deliverables in the brief
    - cover sheet: module name/code, title of submission, total word count
3 - Start writing python code to analyse the data
    - I'll need to find a way to clean up the data too -- what cleaning will it need?
4 - Start writing essay intro
5 - lit review -- I'll need to look into papers written on this topic
    in my own work.
6 - rest of essay
7 - Exec summary

---
Papers
https://arxiv.org/abs/2512.02260
    - EcoCast: A Spatio-Temporal Model for Continual Biodiversity and Climate Risk Forecasting
https://arxiv.org/abs/2512.15748
    - Surely Large Multimodal Models (Don't) Excel in Visual Species Recognition?
https://arxiv.org/abs/2601.22783
    - Compact Hypercube Embeddings for Fast Text-based Wildlife Observation Retrieval
https://arxiv.org/abs/2503.15107
    - Interpretability of Graph Neural Networks to Assess Effects of Global Change Drivers on Ecological Networks
https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1009426
    - Machine learning approach for automatic recognition of tomato-pollinating bees based on their buzzing-sounds

---
Thoughts for topics
- I have locations and abundancae of butterflies over time. Can I classify a butterfly based on region then build a
heamap over time of where butterflies are preferring to be. I could use raylib as a visualisation tool (pyray).
    - Kmeans or naive Bayers classification
    - insects-wider-countryside spreadsheet
    - Intention is to be able to observe trends over time for butterfly thriving locations
        - do we have enough data to apply this to bees too? Can we even show two different axes?
        (no)

- Effects of agricultural schemes on pollinators
    - percentage of land covered in schemes
    - occupancy of pollinators through the years
    - trends in the abundance of butterflies
    - functional connectivity of birds
        - will need simulated data

    - can talk about plant data, but don't include as that data starts a lot later
    - can talk about how these trends may have started the next year after the scheme
        - "delayed" expansion

    - calculate effects of pollination growth over time from pollinator index
        - this can also be a column in the data

    - then I can find the best subset ("optimal") using genetic algo with a good fitness func?
