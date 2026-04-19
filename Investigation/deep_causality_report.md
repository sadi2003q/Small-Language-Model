# Deep Causality Audit

## Scope
- Source notebooks: week*_Adnan/**/*.ipynb
- Source eval records: week*_Adnan/**/*.jsonl (excluding sg_raw/sg_valid and *_dup* files)

## Model Combo Inventory
- Notebook files with parseable model signals: 71
- Notebook parse errors: 1
- Unique guide-solver pairs: 2
  - Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct (seen in 19 notebook configs)
  - meta-llama/Llama-3.2-3B-Instruct -> meta-llama/Llama-3.2-1B-Instruct (seen in 11 notebook configs)
- Unique single-model configs: 6
  - Qwen/Qwen2.5-3B-Instruct (seen in 16 notebook configs)
  - Qwen/Qwen2.5-1.5B-Instruct (seen in 6 notebook configs)
  - microsoft/Phi-3.5-mini-instruct (seen in 5 notebook configs)
  - meta-llama/Llama-3.2-3B-Instruct (seen in 3 notebook configs)
  - google/gemma-2-2b-it (seen in 1 notebook configs)
  - google/gemma-3-4b-it (seen in 1 notebook configs)

## Paired Guided vs Baseline Outcomes
- Paired question count: 15200
- Guided accuracy on paired set: 0.6119
- Baseline accuracy on paired set: 0.5280
- Guided-only-wrong cases: 2081
- Baseline-only-wrong cases: 3356
- Both-wrong cases: 3818

## Guided Regression Root Causes
- solver_instability_or_sampling: 1118
- aggregation_or_refiner_bottleneck: 916
- step_quality_issue: 47

## Top Guided Regression Exemplars
(sorted by guided confidence and vote consistency)
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=23] gt=C guided=D baseline=C conf_g=1.00 cons=0.00 cause=step_quality_issue question=A class plans an investigation to see which brand of light bulb lasts the longest. Which of these steps should come first?  Options: A) Repeat the investigation. B) Write a report of the results. C) Make a table for reco
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=30] gt=C guided=D baseline=C conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Beavers build their homes in ponds and streams. Which characteristic is least critical to building homes in an aquatic environment?  Options: A) waterproof fur B) webbed hind feet C) large, sharp teeth D) flat, wide tail
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=47] gt=A guided=D baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=The students in a class would like to make 20 paper sailboats for a race. The students will select one design and collect the materials they need to construct the boats. Which of the following is the best way for the stu
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=50] gt=B guided=D baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Scientists present the results of their investigations to others for review because  Options: A) people need to be informed about the scientific process. B) data often supports more than one explanation. C) it deters oth
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=53] gt=C guided=B baseline=C conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=A hypothesis is included in a scientific investigation because it  Options: A) makes the conclusion accurate. B) describes the variable. C) states the problem. D) reports the results.
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=59] gt=B guided=C baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Joshua studied the organisms living in a seaside ecosystem. Which do all animals at a beach need for survival?  Options: A) sand B) producers C) salt water D) sea shells
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=69] gt=B guided=A baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Coal-powered plants are designed specifically to convert  Options: A) electrical energy to heat energy. B) chemical energy to electrical energy. C) electrical energy to radiant energy. D) kinetic energy to potential ener
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | ARC_CHALLENGE | idx=7] gt=D guided=B baseline=D conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Which tool would be the most helpful in an investigation of the life cycle of a monarch butterfly?  Options: A) a sharp knife B) a magnifying glass C) a long piece of string D) a large jar with air holes in the top
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | COMMONSENSEQA | idx=24] gt=D guided=A baseline=D conf_g=1.00 cons=0.00 cause=step_quality_issue question=Where can you store you spare linens near your socks?  Options: A) hospital B) chest C) home D) dresser drawers E) cabinet
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | COMMONSENSEQA | idx=29] gt=B guided=C baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=They passed a apple tree on their way to the racetrack, the were going to watch the biggest motorsport spectacle in the world where?  Options: A) maryland B) indiana C) on tv D) park E) new jersey
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | COMMONSENSEQA | idx=51] gt=B guided=E baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=What do humans do to other humans after death?  Options: A) celebrate B) burial C) life D) rebirth E) decomposition
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | COMMONSENSEQA | idx=7] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Where is a bird likely to make it's home?  Options: A) forest B) nest C) roof D) leaves E) sky
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | COMMONSENSEQA | idx=85] gt=E guided=C baseline=E conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=What are people likely to want to do with their friends?  Options: A) own land B) own home C) talk to each other D) believe in god E) spend time
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=12] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: a sponge  Which solution is more physically correct or practical?  A) can clean a car properly B) can clean teeth properly
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=22] gt=B guided=A baseline=B conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: A spit  Which solution is more physically correct or practical?  A) cooks carrots B) cooks A whole pig
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=41] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: Add seed identifiers to new plants.  Which solution is more physically correct or practical?  A) Clip clothespins to planter rims. B) Clip binder clips to planter rims.
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=47] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: Remove hair from kitchen drain.  Which solution is more physically correct or practical?  A) Pour full 2 liter bottle of coke soda down kitchen drain. B) Pour full 2 liter bottle of club soda down kitchen drain.
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=62] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: How long will it take to cure countertops when redoing a kitchen?  Which solution is more physically correct or practical?  A) The curing process takes at least 10 days during which you will need to do your grindin
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=68] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: To remotely control your computer.  Which solution is more physically correct or practical?  A) Connect a wireless mouse to the computer and use it within the range specified B) use a remote controlled controller t
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=71] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: To make a BLT,  Which solution is more physically correct or practical?  A) place bacon, lettuce, and tomato onto a sandwich. B) place bacon, lettuce, and toast onto a sandwich.
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=84] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: table top  Which solution is more physically correct or practical?  A) can be broken by a gorilla B) can be broken by a finger
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=93] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: mold  Which solution is more physically correct or practical?  A) can cover a shovel . B) is more useful than a shovel .
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=95] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: How do you clean a sponge?  Which solution is more physically correct or practical?  A) Put a wet sponge (emphasis on wet) in the microwave and heat it on High for 2 minutes. B) Put a dry sponge (emphasis on wet) i
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=106] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: To reshape a steel buckle.  Which solution is more physically correct or practical?  A) Heat up the buckle and then heat with hammer to reshape B) To reshape a steel buckle, you have to pull it apart to desired sha
- [Qwen/Qwen2.5-3B-Instruct -> Qwen/Qwen2.5-1.5B-Instruct | PIQA | idx=108] gt=A guided=B baseline=A conf_g=1.00 cons=0.00 cause=solver_instability_or_sampling question=Goal: How to beautify a hanging basket.  Which solution is more physically correct or practical?  A) Tie skinny ribbons around the plant here and there to add color B) Hang christmas ornaments from the plant.

## Output Files
- model_combo_inventory.csv
- jsonl_mode_summary.csv
- paired_outcomes.csv
- paired_outcome_summary.csv
- guided_regression_cases.csv
- cause_distribution.csv
- json_parse_errors.csv
