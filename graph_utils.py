from pathlib import Path


data_dir = None
inputdirectory=None
outputdirectory=None
out_dir=None

def set_data_dir(name):
    global inputdirectory, outputdirectory, out_dir, data_dir

    data_dir=name
    inputdirectory = Path(f"./data_input/{data_dir}")
    ## This is where the output csv files will be written
    out_dir = data_dir
    outputdirectory = Path(f"./data_output/{out_dir}")

    return inputdirectory, outputdirectory



def make_dir():
    global inputdirectory, outputdirectory, out_dir, data_dir
    inputdirectory.mkdir(parents=True, exist_ok=True)
    outputdirectory.mkdir(parents=True, exist_ok=True)
    try:
        print(next(outputdirectory.glob("*")))
        print("Graph already Present")
        return True
    except StopIteration:
        print("Graph has to be Created")
        print(outputdirectory)
        return False

def main():
    pass


if __name__ == "__main__":
    main()