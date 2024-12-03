import argparse
import math


def eggholder(x, y):
    """
    Eggholder function to compute the objective function value.
    
    Args:
        x (float): First parameter.
        y (float): Second parameter.
    
    Returns:
        float: Value of the Eggholder function.
    """
    term1 = -(y + 47) * math.sin(math.sqrt(abs(x / 2 + (y + 47))))
    term2 = -x * math.sin(math.sqrt(abs(x - (y + 47))))
    return term1 + term2

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Evaluate the Eggholder function.")
    parser.add_argument("x", type=float, help="First parameter (x)")
    parser.add_argument("y", type=float, help="Second parameter (y)")
    args = parser.parse_args()
    
    # Compute the Eggholder function
    result = eggholder(args.x, args.y)
    
    # Print the result (stdout is captured by subprocess)
    print(result)

if __name__ == "__main__":
    main()