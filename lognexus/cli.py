import argparse
import os
from lognexus.core import process_logs

def main():
    parser = argparse.ArgumentParser(
        description="LogNexus: A Foundational Segmentation Tool for Noisy Drone Logs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--input_dir', '-i', type=str, default='./evidence',
                        help='Directory containing input Excel flight logs.')
    parser.add_argument('--output_dir', '-o', type=str, default='./output',
                        help='Directory to save processed logs.')
    parser.add_argument('--model_dir', '-m', type=str, default='./model',
                        help='Directory containing the trained simpletransformers model.')
    parser.add_argument('--format', '-f', type=str, choices=['xlsx', 'json'], default='xlsx',
                        help='Output format: Excel (with duplicate rows for sentences) or JSON (nested list).')
    parser.add_argument('--cuda', action='store_true',
                        help='Enable GPU acceleration for inference.')

    args = parser.parse_args()

    if not os.path.isdir(args.input_dir):
        print(f"Error: Input directory '{args.input_dir}' does not exist.")
        exit(0)

    if not os.path.isdir(args.model_dir):
        print(f"Error: Model directory '{args.model_dir}' does not exist.")
        exit(0)

    process_logs(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        model_path=args.model_dir,
        output_format=args.format,
        use_cuda=args.cuda
    )

    exit(0)

if __name__ == '__main__':
    main()