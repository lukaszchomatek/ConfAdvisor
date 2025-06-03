from paper_batch import fetch_papers_from_file

if __name__ == "__main__":
    paths = fetch_papers_from_file()
    print("Zapisano dane w plikach:")
    for path in paths:
        print(path)
