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

To see help, activate your virtual environment and execute:

```bash
python3 chind_eval --help
```


This CLI has two main commands: `evaluate` and `analyze`.

## Evaluate

Evaluate a model using the following command:

```
python3 chind_eval evaluate [OPTIONS]
```

### Options

- `-N, --n_samples`: Number of samples (default: 1)
- `-o, --output_file`: URI of the output file to save the evaluation results
- `-m, --model_name`: Model to run (default: 'mock')


The output can be a csv, json or sql database uri.

### Example

```
python3 chind_eval evaluate -N 10 -o output.csv -m mock
```

## Analyze

Analyze the results of a model evaluation using the following command:

```
analyze [OPTIONS]
```

### Options

- `-i, --input`: URI of the evaluation to analyze
- `-o, --output_file`: URI to write the results of the analysis
- `-m, --model_name`: Model to analyze (default: 'mock')

The input can be a csv, json or sql database uri.

### Example

```
analyze -i input.csv -o analysis.csv -m mock
```
