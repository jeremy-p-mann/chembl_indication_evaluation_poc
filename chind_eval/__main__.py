import json

import typer

from chind_eval import get_analysis, get_evaluation_results
from chind_eval.persistence import persist_results, persist_analysis, load_previous_analysis

app = typer.Typer()


@app.command()
def evaluate(
    n_samples: int = typer.Option(1, "-N", help="Number of samples"),
    output_file: str = typer.Option(None, "-o", help="uri of the output"),
    model_name: str = typer.Option('mock', "-m", help="Model to Run"),
):
    print(f'evaluating {n_samples} samples from {model_name}')
    data = get_evaluation_results(n_samples, model_name)
    if output_file:
        print(f'persisting results to {output_file}')
        persist_results(data, output_file)
        print('Complete')
    else:
        print(data)


@app.command()
def analyze(
    input: str = typer.Option(
        None, "-i", help='uri of evaluation to analyze'),
    output_file: str = typer.Option(
        None, "-o", help='uri to write results of analysis'),
    model_name: str = typer.Option('mock', "-m", help='model to analyse'),
):
    if input:
        evaluation = load_previous_analysis(input)
    else:
        evaluation = get_evaluation_results(100, model_name)
    analysis = [get_analysis(evaluation, model_name)]
    if output_file:
        persist_analysis(analysis, output_file)
    else:
        print(analysis)


if __name__ == "__main__":
    app()
