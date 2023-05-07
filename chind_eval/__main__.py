import json

import typer

from chind_eval import get_analysis, get_evaluation_results
from chind_eval.persistence import persist_results

app = typer.Typer()


@app.command()
def evaluate(
    n_samples: int = typer.Option(1, "-N", help="Number of samples"),
    output_file: str = typer.Option(None, "-o", help="Filename of the output"),
    model_name: str = typer.Option('mock', "-m", help="Model to Run"),
):
    data = get_evaluation_results(n_samples, model_name)
    if output_file:
        persist_results(data, output_file)
    else:
        print(data)


@app.command()
def analyze(
    input_file: str = typer.Option(
        None, "-i", help='evaluation to analyze'),
    output_file: str = typer.Option(
        None, "-o", help='file to write results of analysis'),
    model_name: str = typer.Option('mock', "-m", help='model to analyse'),
):
    if input_file:
        with open(input_file, "r") as in_file:
            evaluation = json.load(in_file)
    else:
        evaluation = get_evaluation_results(100, model_name)
    analysis = get_analysis(evaluation, model_name)
    if output_file:
        with open(output_file, "w") as outfile:
            json.dump(analysis, outfile)
    else:
        print(analysis)


if __name__ == "__main__":
    app()
