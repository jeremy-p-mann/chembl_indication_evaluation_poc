# Chembl Validation POC

# Goals

1. Given a chembl treatment, determine whether <medical expert>
   ["strongly disagree", "disagree", "don't know", "agree", "strongly agree"]
   indicating chembl's assert that <drug> is a treatment for <condition>, along 
   with a reason for <medical expert>'s response.
1. Compute the distribution of the responses across chembl indications.
1. Compute the std and time of each treatment evaluation.
1. Filter the indications by max clinical phase

### Later Iterations

1. Make a UI for a SME to experiment with.
1. Add data about the fda label of the drug to the prompt.
1. Determine this distribution as a function of the max_clinical_phase.
1. Write basic tests that <medical expert> is in fact a medical expert.
    - tylenol is a treatment for headache. [strongly agree]
    - warfarin is a treatment for hypertension. [strongly disagree]
    - wegutifinin is a treatment for hypertension. [don't know]


## Chores

- JSON schema of the output + unit test:
- Get a sample of N chembl indications, namely their 
- compute the cost of the model

## Installation

Before using this CLI, please make sure you have Python installed.

Next, install the required package manager:

```bash
pip install poetry
```

Create a virtual environment with:

```bash
poetry install
```

## Usage

To use this CLI, navigate to the folder containing the Python script and run
the following command:

We recommend aliasing the following command:

```bash
poetry run python3 chind_eval --help
```

This will display the help information about the available flags and their usage.

### Flags

- `-N`: The number of chembl samples to run.
- `-o`: The name of the output file storing a json representation of the model's 
  behavior.
- `-m`: The name of the model to use.

### Examples

Run on 5 samples and save them in the file `output.json`:

```bash
poetry run python3 chind_eval -N 5 -o output.json
```

Run on 1 sample and save it to the file `evaluation.json`:

```bash
python chind_eval
```
